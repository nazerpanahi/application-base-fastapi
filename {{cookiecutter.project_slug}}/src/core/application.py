import os
from typing import Dict, Tuple, Callable, Optional, Pattern

from fastapi import APIRouter
from starlette.convertors import Convertor
from starlette.routing import Match, compile_path

from config.app_settings import SRC_DIR
from core.utils import get_default_parameters_values
from core.utils import import_from_app


class ApplicationHolder:
    __applications: Dict[str, "Application"] = dict()

    @classmethod
    def put(cls, application: "Application"):
        cls.__applications.update({application.name: application})

    @classmethod
    def get(cls, app_name: str):
        return cls.__applications.get(app_name)

    @classmethod
    def exists(cls, app_name: str):
        return app_name in cls.__applications.keys()


class Application:
    splitter = ':'
    urls_module = 'urls'
    Holder = ApplicationHolder

    def __init__(self, name):
        self.name = name
        if not self.Holder.exists(app_name=name):
            self.Holder.put(self)
            self.__router = None
        else:
            self.__router = self.Holder.get(name).__router

    @property
    def application_router(self):
        if self.__router is not None:
            return self.__router
        else:
            router_kwargs = {}
            for key, default in get_default_parameters_values(APIRouter.__init__):
                config = import_from_app(path=f"{self.name}.{self.urls_module}", key=key, default=default)
                router_kwargs[key] = config
                del key, default
            urlpatterns = import_from_app(path=f"{self.name}.{self.urls_module}", key='urlpatterns')
            assert isinstance(urlpatterns, list), 'urlpatterns must be a list of dictionaries'
            router = APIRouter(**router_kwargs)
            for pattern in urlpatterns:
                assert isinstance(pattern, dict), 'urlpattern must be a dictionary'
                pattern_type = 'api_route' if 'endpoint' in pattern.keys() and 'path' in pattern.keys() \
                    else 'router' if 'router' in pattern.keys() else None
                if pattern_type == 'api_route':
                    name = f"{self.name}{self.splitter}{pattern.get('name', pattern.get('endpoint').__name__)}"
                    new_pattern = dict(list(filter(lambda item: item[0] != 'name', pattern.items())))
                    router.add_api_route(name=name, **new_pattern)
                elif pattern_type == 'router':
                    pattern_router = pattern.get('router')
                    if isinstance(pattern_router, str):
                        application = self.Holder.get(app_name=pattern_router) or self.__class__(name=pattern_router)
                        pattern_router = application.application_router
                    assert isinstance(pattern_router, APIRouter), 'router does not exist'
                    pattern['router'] = pattern_router
                    router.include_router(**pattern)
                del pattern_type
            del pattern
            self.__router = router
            return router

    @classmethod
    def compile_path(cls, path: str) -> Tuple[Pattern, str, Dict[str, Convertor]]:
        path_regex, path_format, path_convertors = compile_path(path=path)
        return path_regex, path_format, path_convertors

    @classmethod
    def reverse(cls, route_name: str, **path_params: str):
        route_name, *name_parts = route_name.split(cls.splitter)
        router = cls.Holder.get(route_name).application_router
        return router.url_path_for(name=route_name, **path_params)

    @classmethod
    def resolve(cls, app_name: str, path: str, method: str = 'GET') -> Tuple[Match, Optional[Callable], Optional[Dict]]:
        # starlette.routing.Router.__call__
        scope: dict = {
            'type': 'http',
            'method': method,
            'path': path
        }
        app_name, *name_parts = app_name.split(cls.splitter)
        router = cls.Holder.get(app_name).application_router
        match: Match = Match.NONE
        endpoint: Optional[Callable] = None
        path_params: Optional[Dict] = None
        for route in router.routes:
            match, child_scope = route.matches(scope)
            if match == Match.FULL:
                match = Match.FULL
                endpoint = child_scope.get('endpoint')
                path_params = child_scope.get('path_params')
                break
            elif match == Match.PARTIAL:
                match = Match.PARTIAL
                endpoint = child_scope.get('endpoint')
                path_params = child_scope.get('path_params')
            else:
                continue
        return match, endpoint, path_params

    @classmethod
    def create_app(cls, name: str):
        path = SRC_DIR + f'/{name}'
        if not cls.app_exists(name=name):
            os.mkdir(path)
            with open(path + '/__init__.py', 'w') as f:
                f.write("")
            with open(path + '/urls.py', 'w') as f:
                f.write("from typing import List, Dict, Any\n\nprefix = ''\n\nurlpatterns: List[Dict[str, Any]] ="
                        " [\n\t# {\n\t#    'methods': ['GET'],\n\t#    'path': '/',\n\t#    'endpoint': index,\n\t# },"
                        "\n\t# {\n\t#    'router': 'other_application',\n\t# },"
                        "\n]\n".expandtabs(4))
            with open(path + '/app.py', 'w') as f:
                f.write(f"from core.application import Application\n\napp_name = '{name}'\n"
                        f"application = Application(app_name)\n".expandtabs(4))
            return True
        else:
            return False

    @classmethod
    def app_exists(cls, name: str):
        path = SRC_DIR + f'/{name}'
        return os.path.exists(path)

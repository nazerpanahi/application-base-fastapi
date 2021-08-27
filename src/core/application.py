import os
from typing import Dict

from fastapi import APIRouter

from core.utils import import_from_app_urls
from core.utils import get_default_parameters_values
from config.app_settings import SRC_DIR


class ApplicationHolder:
    __applications: Dict[str, "Application"] = dict()

    @classmethod
    def put(cls, application: "Application"):
        cls.__applications.update({application.name: application})

    @classmethod
    def get(cls, app_name: str):
        return cls.__applications.get(app_name)


class Application:
    splitter = ':'
    urls_module = 'urls'
    Holder = ApplicationHolder

    def __init__(self, name):
        self.name = name
        self.Holder.put(self)
        self.__router = None

    @property
    def application_router(self):
        if self.__router is not None:
            return self.__router
        else:
            router_kwargs = {}
            for key, default in get_default_parameters_values(APIRouter.__init__):
                config = import_from_app_urls(app=self.name, key=key, default=default)
                router_kwargs[key] = config
                del key, default
            urlpatterns = import_from_app_urls(app=self.name, key='urlpatterns')
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
    def reverse(cls, name: str, **path_params: str):
        app_name, *name_parts = name.split(cls.splitter)
        router = cls.Holder.get(app_name).application_router
        return router.url_path_for(name=name, **path_params)

    @classmethod
    def create_app(cls, name: str):
        path = SRC_DIR + f'/{name}'
        if not cls.app_exists(name=name):
            os.mkdir(path)
            with open(path + '/__init__.py', 'w') as f:
                f.write('')
            with open(path + '/urls.py', 'w') as f:
                f.write('''from typing import List, Dict, Any

prefix = ''

urlpatterns: List[Dict[str, Any]] = [
    # {
    #    'methods': ['GET'],
    #    'path': '/',
    #    'endpoint': ,
    # },
]
''')
            return True
        else:
            return False

    @classmethod
    def app_exists(cls, name: str):
        path = SRC_DIR + f'/{name}'
        return os.path.exists(path)

import importlib

from fastapi import APIRouter, FastAPI

from core.utils import get_default_parameters_values

splitter = ':'


def import_from_app_urls(app: str, key: str = 'urlpatterns', default=None):
    urls = importlib.import_module(f'{app}.urls')
    value = getattr(urls, key, default)
    return value


def get_router(app: str, *extra_keys):
    if extra_keys is None or len(extra_keys) == 0:
        extra_keys = tuple(get_default_parameters_values(APIRouter.__init__))
    router_kwargs = {}
    for extra_key in extra_keys:
        assert isinstance(extra_key, (str, tuple))
        if isinstance(extra_key, str):
            key, default = extra_key, None
        elif isinstance(extra_key, tuple) and len(extra_key) == 2:
            key, default = extra_key
        config = import_from_app_urls(app=app, key=key, default=default)
        router_kwargs[key] = config
        del key, default
    del extra_key
    urlpatterns = import_from_app_urls(app=app, key='urlpatterns')
    assert isinstance(urlpatterns, list), 'urlpatterns must be a list of dictionaries'
    router = APIRouter(**router_kwargs)
    for pattern in urlpatterns:
        assert isinstance(pattern, dict), 'urlpattern must be a dictionary'
        pattern_type = 'api_route' if 'endpoint' in pattern.keys() and 'path' in pattern.keys() \
            else 'router' if 'router' in pattern.keys() else None
        if pattern_type == 'api_route':
            name = f"{app}{splitter}{pattern.get('name', pattern.get('endpoint').__name__)}".strip('.')
            new_pattern = dict(list(filter(lambda item: item[0] != 'name', pattern.items())))
            router.add_api_route(name=name, **new_pattern)
        elif pattern_type == 'router':
            pattern_router = pattern.get('router')
            if isinstance(pattern_router, str):
                pattern_router = get_router(app=pattern_router)
            assert isinstance(pattern_router, APIRouter), 'router does not exist'
            pattern['router'] = pattern_router
            router.include_router(**pattern)
        del pattern_type
    del pattern
    return router


def reverse(app: FastAPI, name: str, **path_params: str):
    return app.url_path_for(name=name, **path_params)


def reverse2(name: str, **path_params: str):
    app_name, *name_parts = name.split(splitter)
    router = get_router(app=app_name)
    return router.url_path_for(name=name, **path_params)

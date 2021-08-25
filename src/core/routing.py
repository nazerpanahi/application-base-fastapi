import importlib

from fastapi import APIRouter


def import_from_app_urls(app: str, key: str = 'urlpatterns', default=None):
    urls = importlib.import_module(f'{app}.urls')
    value = getattr(urls, key, default)
    return value


def get_router(app: str, *extra_keys):
    if extra_keys is None or len(extra_keys) == 0:
        extra_keys = (
            ('prefix', ''),
        )
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
    router = APIRouter(**router_kwargs)
    for pattern in urlpatterns:
        assert isinstance(pattern, dict), 'url pattern must be a dictionary.'
        assert 'type' in pattern.keys(), 'url pattern dictionary must include "type" key'
        pattern_type = pattern.pop('type')
        if pattern_type == 'api_route':
            router.add_api_route(**pattern)
        elif pattern_type == 'router':
            pattern_router = pattern.get('router')
            if isinstance(pattern_router, str):
                pattern_router = get_router(app=pattern_router)
            assert isinstance(pattern_router, APIRouter), 'router does not exist'
            pattern['router'] = pattern_router
            router.include_router(**pattern)
        pattern['type'] = pattern_type
        del pattern_type
    del pattern
    return router

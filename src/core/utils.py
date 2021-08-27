import importlib
import inspect


def import_from_app_urls(app: str, key: str = 'urlpatterns', default=None):
    urls = importlib.import_module(f'{app}.urls')
    value = getattr(urls, key, default)
    return value

def get_default_parameters_values(func):
    params = list()
    for param_name, param in inspect.signature(func).parameters.items():
        if param.default is not inspect._empty:
            params.append((param_name, param.default))
    return params

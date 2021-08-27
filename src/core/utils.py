import importlib
import inspect


def import_from_app(path: str, key: str, default=None):
    mod = importlib.import_module(f'{path}')
    value = getattr(mod, key, default)
    return value

def get_default_parameters_values(func):
    params = list()
    for param_name, param in inspect.signature(func).parameters.items():
        if param.default is not inspect._empty:
            params.append((param_name, param.default))
    return params

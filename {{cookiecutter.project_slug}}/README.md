# {{cookiecutter.project_name}}

{{cookiecutter.short_description}}

## Application

An application is a python package that follow the structure below
(consider we want to create a new app called `demo_app`):

```
demo_app
 |   __init__.py
 |   urls.py
 |   app.py
```

optionally you can have a file called `endpoints.py` too.

Copy the content below into `urls.py`:

```python
from typing import List, Dict

urlpatterns: List[Dict] = [
    # {
    #     'methods': ['GET'],
    #     'path': '/',
    #     'endpoint': index,
    # },

    # {
    #     'router': 'other_application'
    # },
]
```

Copy content below into `app.py`:

```python
from core.application import Application

app_name = 'demo_app'
application = Application(app_name)
```

Alternatively you can fill the `application_name` variable and run the code below to create a sample new app:

```python
from core.application import Application

application_name = 'demo_app'
Application.create_app(name=str(application_name))
```

Now that you create a new app called `demo_app`, next you need to register the app into settings:
In the `config/app_settings.py` add this line:

```python
from typing import List
from pydantic import BaseSettings


# ...
class Settings(BaseSettings):
    # ...
    REGISTERED_APPLICATIONS: List[str] = [
        # ...
        'demo_app',
    ]
```

Now you can run `src/app.py` and see `demo_app` is added.

## More details:

### urls.py

- Application router arguments: Additional to `urlpatterns` you can define other variables too. Variables will be passed
  to `fastapi.routing.APIRouter` as keyword arguments.

  For example if you define `prefix` variable like this:
  ```python
  prefix = '/demo'
  ```
  This will be translated to  :
  ```
  APIRouter(prefix='/demo')
  ```

- URL patterns: `urlpatterns` is a list of dictionaries. Each url pattern is a dictionary that will be translated to
  keyword arguments (for `fastapi.routing.APIRoute` or `fastapi.routing.APIRouter`).
    - If you want to **include** urls from other applications, you should pass the
      `fastapi.routing.APIRouter` keyword arguments dictionary as the `urlpattern` dictionary. Note that you can pass
      another application name as a string instead of a real router for key `router`.
    - Otherwise, if you want to define a new route for current application, you should pass `fastapi.routing.APIRoute`
      keyword arguments dictionary as the `urlpattern` dictionary.

- Name Mangling: All route names will be replaced by `{application}:{route_name}`. For example consider route `/ping`
  that is located in the `demo_app` application with the name of `ping`. After name mangling, name of route `ping` will
  be replaced by `demo_app:ping`.

- Reverse: Returns an url path.

```python
from core.application import Application

path = Application.reverse(route_name='demo_app:ping') # /demo/ping
```

- Resolve: The resolve function can be used for resolving URL paths to the corresponding endpoints.

```python
from core.application import Application
from starlette.routing import Match

match, endpoint, path_params = Application.resolve(app_name='demo', path='/demo/ping', method='GET')
if match == Match.FULL:
    # call corresponding endpoint function
    endpoint(**path_params)
elif match == Match.PARTIAL:
    # methods are not match (http 405 code)
    # call corresponding endpoint function
    endpoint(**path_params)
```

## Examples

We add three demo application named `api`, `api_v1`, and `api_v2`.

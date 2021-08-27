# Application Base FastAPI

## Description
Write reusable applications and enjoy the benefits of reusable apps. 
It helps you to write an application once and use it in different fastapi based web applications.
applications can be considered as a module for a big sofware application. `Write one, Use everywhere`.

## What is an application?
An application is a python package that contains a file named `urls.py`. 

## How an application works?
In the `urls.py` file you define your api endpoints or include some 
other application endpoints by defining a variable called `urlpatterns` that is a list of
dictionaries. Other variables in the `urls.py` can be passed as an kwargs to `fastapi.APIRouter`. 
By default only `prefix` variable is checked.

## How to make a new applicaion?
- Create a new python package
- Create `urls.py` file
- In the `urls.py`:
    - Define `urlpatterns` variable as a list.
        - Add your api routes in the `urlpatterns` as a dictionary. e.g.
          ```python
          {
              'methods': ['GET'],
              'path': '/ENDPOINT',
              'endpoint': ENDPOINT
          }
          ```
        - Include your api routes from other applications in the `urlpatterns` as a dictionary. e.g.
          ```python
          {
              'router': 'OTHERAPPNAME',
          }
          ```
    - [OPTIONAL] Define `prefix` variable as a string.
- Add your application package name in the `config.app_settings.REGISTERED_APPLICATIONS`.

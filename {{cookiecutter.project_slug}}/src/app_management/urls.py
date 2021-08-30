from typing import Dict, Any

from .endpoints import *

prefix = '/app'

urlpatterns: List[Dict[str, Any]] = [
    {
        'methods': ['GET'],
        'path': '/list',
        'endpoint': app_list,
    },
    {
        'methods': ['GET'],
        'path': '/routes/{app_name:str}',
        'endpoint': app_routes,
    },
]

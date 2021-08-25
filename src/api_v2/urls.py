from typing import List, Dict
from api_v2.endpoints import router_ping

prefix = '/v2'

urlpatterns: List[Dict] = [
    {
        'type': 'api_route',
        'methods': ['GET'],
        'path': '/ping',
        'endpoint': router_ping,
    },
]

from typing import List, Dict
from api_v2.endpoints import router_ping

prefix = '/v2'

urlpatterns: List[Dict] = [
    {
        'methods': ['GET'],
        'path': '/ping',
        'endpoint': router_ping,
    },
]

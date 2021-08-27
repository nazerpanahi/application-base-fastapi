from typing import List, Dict
from api_v1.endpoints import router_ping

prefix = '/v1'

urlpatterns: List[Dict] = [
    {
        'methods': ['GET'],
        'path': '/ping',
        'endpoint': router_ping,
    },
]

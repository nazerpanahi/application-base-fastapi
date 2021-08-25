from typing import List, Dict

prefix = '/api'

urlpatterns: List[Dict] = [
    {
        'type': 'router',
        'router': 'api_v1'
    },
    {
        'type': 'router',
        'router': 'api_v2'
    }
]

from typing import List

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from starlette import status as http_status

from config.app_settings import settings
from core.application import Application


def app_list():
    return JSONResponse(content={
        "data": settings.REGISTERED_APPLICATIONS,
        "status": http_status.HTTP_200_OK,
    })


def app_routes(app_name: str):
    data: List = list()
    application = Application.Holder.get(app_name=app_name)
    if application is None:
        raise HTTPException(status_code=http_status.HTTP_200_OK, detail='invalid app name')
    for route in application.application_router.routes:
        route_data: dict = {
            'methods': list(route.methods),
            'path': str(route.path),
            'name': str(route.name),
        }
        data.append(route_data)
    return JSONResponse(content={
        'data': data,
        'status': http_status.HTTP_200_OK,
    })

import http.cookies

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import settings, AppConstants
from core.application import Application

http.cookies._is_legal_key = lambda _: True
app = FastAPI(
    title=AppConstants.title,
    description=AppConstants.description,
    version=AppConstants.version
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'] if settings.CORS_ORIGINS is None or \
                           len(list(settings.CORS_ORIGINS)) == 0 else [str(origin) for origin in settings.CORS_ORIGINS],
    allow_methods=['*'],
    allow_headers=['*'],
)

for reg_app in settings.REGISTERED_APPLICATIONS:
    application = Application(reg_app)
    app.include_router(router=application.application_router)

if settings.DEBUG:
    if __name__ == "__main__":
        import uvicorn

        uvicorn.run('app:app', host='0.0.0.0', port=8000, debug=False, reload=False)

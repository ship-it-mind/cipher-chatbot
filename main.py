from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from api.api import api_router

app = FastAPI()

app.include_router(api_router)

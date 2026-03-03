from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.base.err.base_err import BaseErr


class AppException(Exception):
    def __init__(self, code: int, message: str = None, data: any = None):
        self.code = code
        self.message = message
        self.data = data


class ExceptionHandler(object):

    def app_exception(self, request: Request, exc: AppException):
        content = {
            "code": f"{exc.code}",
            "message": f"{exc.message}",
            "data": exc.data
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)

    def http_exception(self, request: Request, exc: StarletteHTTPException):
        exc_content = jsonable_encoder(exc)
        content = {
            "code": 1000,
            "message": f"{exc.detail}",
            "data": exc_content
        }
        return JSONResponse(status_code=exc.status_code, content=content)

    def validation_exception(self, request: Request, exc: RequestValidationError):
        exc_content = jsonable_encoder(exc)
        exc_list = exc_content["_errors"]
        exc_body = exc_content["body"]
        exc_data = exc_list[0]
        loc_str = ",".join(exc_data['loc'])
        content = {
            "code": BaseErr.VALIDATION_ERROR["code"],
            "message": BaseErr.VALIDATION_ERROR["msg"] + ": " + f"{loc_str} {exc_data['msg']}",
            "data": exc_list
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)

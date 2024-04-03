import json
import logging
from datetime import datetime

from fastapi import Request
from pytz import timezone
from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, StreamingResponse
from starlette.types import Message

logger = logging.getLogger("main")
logging.basicConfig(level=logging.DEBUG, encoding='utf-8')
steam_handler = logging.FileHandler(filename='../info.log', mode='w', encoding='utf-8')
logger.addHandler(steam_handler)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_client = request.client
        req_method = request.method
        req_url = request.url
        req_headers = request.headers
        req_body = await request.body()
        await set_body(request, req_body)
        response = await call_next(request)
        res_status_code = response.status_code
        res_media_type = response.media_type
        res_headers = response.headers
        if isinstance(response, StreamingResponse):
            res_body = b''
            async for chunk in response.body_iterator:
                res_body += chunk
        else:
            res_body = response.body
        res_body = await middleware_exception_handler(
            res_body=res_body,
            res_status_code=res_status_code,
            response=response
        ) if res_status_code != 200 else res_body
        task = BackgroundTask(func=log_info,
                              req_client=req_client,
                              req_method=req_method,
                              req_url=req_url,
                              req_headers=req_headers,
                              req_body=req_body,
                              res_status_code=res_status_code,
                              res_media_type=res_media_type,
                              res_headers=res_headers,
                              res_body=res_body)
        return Response(status_code=200,
                        media_type=res_media_type,
                        headers=dict(res_headers),
                        content=res_body,
                        background=task)


def log_info(req_client, req_method, req_url, req_headers, req_body,
             res_status_code, res_media_type, res_headers, res_body):
    logging.info("-" * 100)
    logging.info(f">>> REQUEST TIME: {datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f">>> REQUEST CLIENT: {req_client}")
    logging.info(f">>> REQUEST METHOD: {req_method}")
    logging.info(f">>> REQUEST URL: {req_url}")
    logging.info(f">>> REQUEST HEADERS: {req_headers}")
    logging.info(
        f">>> REQUEST BODY: {req_body.decode('utf-8') if req_headers.get('Content-Type') == 'application/json' else req_body}")
    logging.info(f">>> RESPONSE STATUS CODE: {res_status_code}")
    logging.info(f">>> RESPONSE MEDIA TYPE: {res_media_type}")
    logging.info(f">>> RESPONSE HEADERS: {res_headers}")
    logging.info(f">>> RESPONSE BODY: {res_body.decode('utf-8')}")
    logging.info("-" * 100)


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {'type': 'http.request', 'body': body}

    request._receive = receive


async def middleware_exception_handler(res_body, res_status_code, response):
    res_body = json.dumps(
        dict(
            code=res_status_code,
            success=False,
            message=json.loads(res_body.decode('utf-8'))['detail'],
        ),
        ensure_ascii=False
    ).encode('utf-8')
    response.headers['Content-Length'] = str(len(res_body))
    return res_body

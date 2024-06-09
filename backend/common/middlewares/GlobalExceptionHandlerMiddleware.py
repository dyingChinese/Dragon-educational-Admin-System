from rest_framework.views import exception_handler

from common.handle import APIResponse


class GlobalExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        print('捕获到异常：', exception)
        # 这里处理异常
        return APIResponse(code=500500, msg='服务器内部错误')


def custom_exception_handler(exc, context):
    res = exception_handler(exc, context)
    if res:
        # 说明是drf的异常，它处理了
        if isinstance(res.data, dict):
            detail = res.data.pop('detail', 'error')
        else:
            detail = res.data[0]
        return APIResponse(code=400400, msg=detail)
    print('捕获到异常：', exc)
    # 说明是其它异常，它没有处理
    return APIResponse(code=500500, msg='服务器内部错误')

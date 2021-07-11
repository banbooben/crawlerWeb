from flask.globals import request
from flask.wrappers import Request as _Request
from common.common_functions import get_uuid


class Request(_Request):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.request_id = get_uuid()
        self._param = None

    @property
    def params(self):
        """
        根据不同类型的请求去获取对应的data
        POST, PUT -> request.data or request.form
        GET, DELETE -> request.args
        """
        if self._param is not None:
            return self._param

        data = {}
        if self.method in ("POST", "PUT"):
            data = self.get_json(force=True) if self.data.strip() else {k: v for k, v in self.form.items()}
        elif self.method in ("DELETE", "GET"):
            data = self.args
        self._param = data
        return data


def init_hook_function(app):
    @app.before_request
    def log_request_info():
        """
        打印入参
        """
        app.logger.info(request.request_id)
        app.logger.info(request.params)


def init_bp_hook_function(bp):
    @bp.before_app_request
    def log_request_info():
        """
        打印入参
        """
        bp.logger.info(request.request_id)
        bp.logger.info(request.params)

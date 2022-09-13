import contextvars
import json
import logging
from datetime import datetime

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.common.infra.gcp.firebase import get_account_info

cloud_trace_context = contextvars.ContextVar('cloud_trace_context', default='')
TRACE_HEADER = 'X-Cloud-Trace-Context'
TRACE_LOG_KEY = 'logging.googleapis.com/trace'


class CloudRunJSONFormatter(logging.Formatter):

    def __init__(self, /, *args, project_id: str | None = None, **kwargs):
        """
        JSON format logger compliant with Cloud Run Logging specifications.
        To allow Request Tracing the value of project_id is needed, which can be passed as a keyword parameter.
        If project_id is not passed as a parameter, it will be extracted using :func:`app.common.infra.gcp.firebase.get_account_info`.
        If that fails, Request Tracing will be disabled.
        Request Tracing also requires :func:app.common.infra.gcp.cloud_loggingCloudRunLoggingMiddleware`.
        """
        if project_id:
            self._project_id = project_id
        else:
            try:
                self._project_id = get_account_info()["project_id"]
            except Exception:  # If impossible, disable
                self._project_id = None

        super().__init__(*args, **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        # Use default Formatter for exceptions
        if any([record.exc_info, record.stack_info, record.exc_text]):
            return super().format(record)

        log = {
            "message": super().format(record),
            # A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits
            # Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z"
            # https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry
            "timestamp": datetime.fromtimestamp(record.created).isoformat() + "Z",
            "severity": record.levelname,
            "sourceLocation": {
                "file": record.name
            }
        }
        self._add_trace_info(log)

        return json.dumps(log)

    def _add_trace_info(self, log_dict):
        if self._project_id and (trace_context := cloud_trace_context.get()):
            trace = trace_context.split("/")
            log_dict[TRACE_LOG_KEY] = f"projects/{self._project_id}/traces/{trace[0]}"


# https://dev.to/floflock/enable-feature-rich-logging-for-fastapi-on-google-cloud-logging-j3i
class CloudRunLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if trace_header := request.headers.get(TRACE_HEADER, None):
            cloud_trace_context.set(trace_header)

        return await call_next(request)

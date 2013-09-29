import logging
import threading
import time

from django.templatetags.static import static

from wtl.streaming_log_response.response import StreamingLogHttpResponse


HTML_HEADER = """<!doctype html>
<html>
<head><meta charset="utf-8" /><link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" /><link rel="stylesheet" href="%(css_url)s" /></head>
<body><div class="container logs-page"><h1 class="page-header">Long operation in progress...</h1>
<h2>Streaming response:</h2>
"""

HTML_FOOTER = """</div></body></html>"""


class StreamingLogResponseHandler(logging.Handler):
    def __init__(self, generator, level=logging.NOTSET):
        super(StreamingLogResponseHandler, self).__init__(level)
        self.generator = generator

    def handle(self, record):
        self.generator.handle(record, self.format(record))
        return False


# TODO: log level restoring
# TODO: custom formatters
# TODO: allow different formatters for each logger
class StreamingLogResponseGenerator(object):
    thread = None
    messages = []
    handlers = {}

    def __init__(self, func, logs):
        super(StreamingLogResponseGenerator, self).__init__()
        self.messages = []
        self.setup_logging(logs)
        self.thread = threading.Thread(target=func)
        self.thread.start()

    def setup_logging(self, logs):
        self.handlers = {}
        for log_name, log_level in logs.items():
            handler = StreamingLogResponseHandler(self, log_level)
            handler.formatter = logging.Formatter('<div class="log-entry log-entry-%(levelname)s"><time>%(asctime)-15s</time> %(message)s</div>\n')
            logger = logging.getLogger(log_name)
            logger.addHandler(handler)
            logger.setLevel(log_level)
            self.handlers[logger] = handler

    def teardown_logging(self):
        for logger, handler in self.handlers.items():
            logger.removeHandler(handler)

    def handle(self, record, message):
        if record.thread == self.thread.ident:
            self.messages.append(message)

    def __iter__(self):
        yield HTML_HEADER % {'css_url': static('css/index.css')}
        for _ in range(100):
            if not self.thread.is_alive():
                break
            time.sleep(1)
            for message in self.messages:
                yield message
            self.messages = []
        yield HTML_FOOTER
        self.teardown_logging()


class StreamingLogResponseMiddleware(object):
    def process_response(self, request, response):
        if isinstance(response, StreamingLogHttpResponse):
            response.streaming_content = StreamingLogResponseGenerator(response.func, response.logs)
        return response

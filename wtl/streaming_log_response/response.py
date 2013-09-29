from django.http import StreamingHttpResponse


class StreamingLogHttpResponse(StreamingHttpResponse):
    func = None
    logs = None

    def __init__(self, func, logs, *args, **kwargs):
        # N.B: Call super-super init!
        super(StreamingHttpResponse, self).__init__(*args, **kwargs)
        self.func = func
        self.logs = logs

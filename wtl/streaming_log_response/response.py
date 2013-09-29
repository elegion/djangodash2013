from django.http import StreamingHttpResponse


class StreamingLogHttpResponse(StreamingHttpResponse):
    func = None
    logs = None

    def __init__(self, func, logs, args=None, kwargs=None, *_args, **_kwargs):
        # N.B: Call super-super init!
        super(StreamingHttpResponse, self).__init__(*_args, **_kwargs)
        self.func = func
        self.logs = logs
        self.args = args
        self.kwargs = kwargs

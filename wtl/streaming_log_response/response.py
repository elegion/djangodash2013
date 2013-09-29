from django.http import StreamingHttpResponse


class StreamingLogHttpResponse(StreamingHttpResponse):
    def __init__(self, func, logs, args=None, kwargs=None, callback=None, *_args, **_kwargs):
        # N.B: Call super-super init!
        super(StreamingHttpResponse, self).__init__(*_args, **_kwargs)
        self.func = func
        self.logs = logs
        self.args = args
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        self.kwargs = kwargs
        self.callback = callback
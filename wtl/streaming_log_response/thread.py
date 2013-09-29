import sys
from threading import Thread


# Inspired by http://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
if sys.version_info >= (3,):
    class ThreadWithReturnValue(Thread):
        def __init__(self, *args, **kwargs):
            Thread.__init__(self, *args, **kwargs)
            self._return = None

        def run(self):
            try:
                if self._target:
                    self._return = self._target(*self._args, **self._kwargs)
            finally:
                # Avoid a refcycle if the thread is running a function with
                # an argument that has a member that points to the thread.
                del self._target, self._args, self._kwargs

        def join(self, *args, **kwargs):
            Thread.join(self, *args, **kwargs)
            if self._return is None:
                return ()
            else:
                return self._return
else:
    class ThreadWithReturnValue(Thread):
        def __init__(self, *args, **kwargs):
            Thread.__init__(self, *args, **kwargs)
            self._return = None

        def run(self):
            if self._Thread__target is not None:
                self._return = self._Thread__target(*self._Thread__args,
                                                    **self._Thread__kwargs)

        def join(self, *args, **kwargs):
            Thread.join(self, *args, **kwargs)
            if self._return is None:
                return ()
            else:
                return self._return

import threading


def do_async(func, *args, **kwargs):
    """Wrapper to execute a function on a separate thread to prevent blocking I/O.

       It's best to use this with HTTP requests, for example, that
       might spend an unpredictable amount of time waiting for a
       response, but the response is not needed for the main I/O
       task.

       It's not advisable to use this for long-running, processor-intensive
       tasks, since that will lead to CPU contention that will not necessarily
       improve performance.

       :param func: The function to execute asynchronously.
    """
    t = threading.Thread(target=func, args=args, kwargs=kwargs)
    t.start()


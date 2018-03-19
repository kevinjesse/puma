import time


def timeit(method):
    def timed(*args, **kw):
        print('Starting Timer:')
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print("{method.__name__} {duration:.3f} sec"
              .format(method=method, duration=te - ts))
        return result

    return timed

import asyncio
import puma
import math

from time_func import timeit


class LoopTest:
    # test_data = [i for i in range(100)]
    test_data = [1000] * 1000000

    @staticmethod
    async def loop_test_puma(is_on_server: bool):
        def times2(x):
            return x * 2

        # TODO: Fix service.py scope problem so that exec() can do recursive function
        def factorial(n):
            def inner(m):
                return m * inner(m - 1) if m > 1 else 1
            return inner(n)

        def fac_l(n):
            total = n
            for i in range(n - 1, 0, -1):
                total *= i
            return total

        result = await puma.puma_map(mode='on_server' if is_on_server else 'normal', func=fac_l,
                                     data=LoopTest.test_data)
        print('PUMA RESULT:\n', sum(result))

    @staticmethod
    def loop_test_local(is_on_server: bool):
        def times2(x):
            return x * 2

        def factorial(n):
            def inner(m):
                return m * inner(m - 1) if m > 1 else 1
            return inner(n)

        def fac_l(n):
            total = n
            for i in range(n - 1, 0, -1):
                total *= i
            return total

        result = puma.puma_map_local(mode='on_server' if is_on_server else 'normal',
                                     func=fac_l, data=LoopTest.test_data)
        print('LOCAL RESULT:\n', sum(result))


@timeit
def run_test_puma():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(LoopTest.loop_test_puma(is_on_server=False))


@timeit
def run_test_local():
    LoopTest.loop_test_local(is_on_server=False)


if __name__ == '__main__':
    run_test_puma()
    # run_test_local()

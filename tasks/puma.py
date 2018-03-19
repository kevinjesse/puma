import inspect
import asyncio
import aiohttp
import json
import math
from itertools import accumulate, chain, repeat, tee
from typing import List


class DisSystem:
    def __init__(self, mode):
        self.mode = mode
        print('running on:', self.server_address)


    @property
    def server_address(self):
        if self.mode == 'on_server':
            return "http://localhost:8000/service/1"
        elif self.mode == 'on_mac':
            return "http://localhost:8080/service/1"
        else:
            return "http://ec2-34-203-208-233.compute-1.amazonaws.com:8000/service/1"

    def num_service(self, n: int):
        return min(int(math.sqrt(n)), 10000000)

    @property
    def num_retry(self):
        return 100

    @staticmethod
    def chunk(xs, n):
        assert n > 0
        L = len(xs)
        s, r = divmod(L, n)
        widths = chain(repeat(s+1, r), repeat(s, n-r))
        offsets = accumulate(chain((0,), widths))
        b, e = tee(offsets)
        next(e)
        return [xs[s] for s in map(slice, b, e)]

    async def _fetch(self, session, func, data: list, index: int):
        json_send = {
            'func_str': self._func2str(func),
            'func_name': func.__name__,
            'func_data': data
        }
        # print(json_send)
        async with session.get(self.server_address, data=json_send) as resp:
            print('http request #', index)
            for i in range(self.num_retry):
                if resp.status == 200:
                    r_text = await resp.text()
                    # print(r_text)
                    results = json.loads(r_text)
                    # pprint(results)
                    r_function = results.get('function', {})
                    if r_function.get('success', False) is True:
                        # print(r_function.get('result', None))
                        return r_function.get('result', None)
                    else:
                        print(r_function.get('exception', ':/'))
                        return None
                else:
                    print(resp.status, index)

            return None

    async def _bound_fetch(self, sem, session, func, data: list, index: int):
        # Getter function with semaphore.
        async with sem:
            return await self._fetch(session, func, data, index)

    async def execute(self, func, c_data: List[list], length: int):
        tasks = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            print('spawning request:', self.num_service(length))
            sem = asyncio.Semaphore(1000)
            for i in range(self.num_service(length)):
                print('ensure_future', i)
                task = asyncio.ensure_future(self._bound_fetch(sem, session, func=func, data=c_data[i], index=i))
                tasks.append(task)

            print('prepare gather')
            responses = asyncio.gather(*tasks)
            await responses
            # print(responses)
            if responses is not None:
                return list(chain.from_iterable(responses.result()))
            else:
                return None

    def _func2str(self, func):
        lines = inspect.getsourcelines(func)
        leading_spaces = len(lines[0][0]) - len(lines[0][0].lstrip())
        f_lines = [l[leading_spaces:] for l in lines[0]]
        return ("".join(f_lines)), func.__name__


async def puma_map(mode: str, func, data: list):
    system = DisSystem(mode=mode)
    print('length of data:', len(data))
    print('data:', data[0])
    c_data = DisSystem.chunk(data, system.num_service(len(data)))
    r = await system.execute(func=func, c_data=c_data, length=len(data))
    return r


def puma_map_local(mode: str, func, data: list):
    system = DisSystem(mode=mode)
    print('length of data:', len(data))
    print('data:', data[0])
    c_data = DisSystem.chunk(data, system.num_service(len(data)))
    r = []
    for data in c_data:
        for c in data:
            r.append(func(c))
    # r = [func(c) for data in c_data for c in data]
    return r

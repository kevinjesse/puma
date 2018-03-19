from timeit import default_timer as timer

def loop(size: int):
    array = [i for i in range(0, size)]


if __name__ == '__main__':
    start = timer()
    loop(10000000)
    end = timer()
    print(end - start)



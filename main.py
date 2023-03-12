import logging
from timeit import default_timer


logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')


def duration(fun):
    def inner(*args, **kwargs):
        start = default_timer()
        rez = fun(*args, **kwargs)
        logging.info(f'{default_timer()-start=} sec')

        return rez

    return inner


@duration
def main():
    print(default_timer())


if __name__ == "__main__":
    main()

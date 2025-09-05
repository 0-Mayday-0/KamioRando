from random import randint, seed
from img_data import KamioR
from icecream import ic
from asyncio import run, sleep


async def random_int(a: int, b: int) -> int:
    rand_obj: KamioR = KamioR()

    current_seed: int = await rand_obj.get_random_detect()*randint(a*randint(a,b),b*randint(a,b))
    seed(current_seed)

    return randint(a, b)

async def main():
    while True:
        ic(await random_int(1, 7000))


if __name__ == '__main__':
    run(main())
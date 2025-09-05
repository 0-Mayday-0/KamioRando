
from requests import get as rget
from requests import Response
from asyncio import run, create_task, to_thread, Task
from io import BytesIO
from PIL import Image, ImageFile
from PIL.GifImagePlugin import GifImageFile
from random import choice
from collections.abc import Generator

from icecream import ic
from time import sleep

class KamioR:
    def __init__(self) -> None:
        self.image: GifImageFile | None = None
        self.url: str = 'https://www-sk.icrr.u-tokyo.ac.jp/realtimemonitor/skev.gif'
        self.allowed_terrain: None | Generator[int, None, tuple[int, int]] = None
        #self.sizes: list[tuple[int, int]] = [(822, 743), (1656, 976)]

    def generate_terrain(self, size: tuple[int, int]) -> Generator[int, None, tuple[int, int]]:
        terrains: dict[tuple[int, int], tuple[range, range]] = {(822, 743): (range(23, 803, 3), range(250, 495, 5)),
                                                                (1656, 976): }

        while True:
            yield (choice(terrains[size]))

    async def _get_img_response(self) -> Response:
        response: Response = await to_thread(rget, self.url)

        return response

    async def get_img_bytes(self) -> bytes | None:
        response_task: Task[Response] = create_task(self._get_img_response())

        response_status: Response = await response_task

        if response_status.status_code == 200:
            return response_status.content
        return None

    async def create_image(self) -> None:
        img_data: bytes = await self.get_img_bytes()

        try:
            assert img_data
            self.image: ImageFile = Image.open(BytesIO(img_data))
            self.allowed_terrain = self.allowed_terrain if self.image.size == self.sizes[0] else [list(range(23, 803, 3)),
                                                                                                  list(range(250, 495, 5))]

        except AssertionError:
            print("Something went wrong fetching from KamiokaNDE.")

    async def get_random_detect(self) -> hex:
        await self.create_image()

        random_pixel: tuple[int, int] = (choice(self.allowed_terrain[0]), choice(self.allowed_terrain[1]))
        detection: bool = self.image.getpixel(random_pixel) != 0

        while not detection:
            random_pixel = (choice(self.allowed_terrain[0]), choice(self.allowed_terrain[1]))
            detection: bool = self.image.getpixel(random_pixel) != 0

        return self.image.getpixel(random_pixel)

    def debug_color_img(self) -> None:
        with open("debug/HIGHRES.gif", 'rb') as img_handle:
            self.image = Image.open(BytesIO(img_handle.read()))
            ic(self.image.size)

        self.allowed_terrain = self.allowed_terrain if self.image.size == self.sizes[0] else [list(range(40, 1620, 3)),
                                                                                              list(range(330, 650, 5))]
        with self.image as img_handle:
            for y in self.allowed_terrain[1]:
                for x in self.allowed_terrain[0]:
                    img_handle.putpixel((x, y), value=(255,255,255))

            img_handle.show()



async def main() -> None:
    rand: KamioR = KamioR()

    #await rand.get_random_detect()
    #rand.debug_color_img()

    rp = rand.generate_terrain((1656, 976))

    while True:
        ic(next(rp))

        sleep(0.5)


if __name__ == '__main__':
    run(main())
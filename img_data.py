
from requests import get as rget
from requests import Response
from asyncio import run, create_task, to_thread, Task
from io import BytesIO
from PIL import Image, ImageFile
from PIL.GifImagePlugin import GifImageFile
from random import choice
from collections.abc import Generator


class KamioR:
    def __init__(self) -> None:
        self.image: GifImageFile | None = None
        self.url: str = 'https://www-sk.icrr.u-tokyo.ac.jp/realtimemonitor/skev.gif'
        self.allowed_terrain: None | Generator[tuple[int, int], None, tuple[int, int]] = None
        self.sizes: list[tuple[int, int]] = [(822, 743), (1656, 976), (1209, 1018), (1658, 993)]
        self.ranges: list[tuple[range, range]] = [(range(23, 803, 3), (range(250, 495, 5))),
                                                 (range(40, 1620, 3), range(330, 650, 5)),
                                                  (range(32, 1180, 3), range(343, 675, 5)),
                                                  (range(40, 1620, 3), range(330, 650, 5))]

        self.terrains: dict[tuple[int, int], tuple[range, range]] = {sz: (rg[0], rg[1]) for sz, rg in zip(self.sizes, self.ranges)}


    def generate_terrain(self, size: tuple[int, int]) -> Generator[tuple[int, int], None, tuple[int, int]]:
        while True:
            yield choice(self.terrains[size][0]), choice(self.terrains[size][1])


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
            size = self.image.size
            self.allowed_terrain = self.generate_terrain(size)

        except AssertionError:
            print("Something went wrong fetching from KamiokaNDE.")

    async def get_random_detect(self) -> hex:
        await self.create_image()

        random_pixel: tuple[int, int] = next(self.allowed_terrain)
        detection: bool = self.image.getpixel(random_pixel) != 0

        while not detection:
            random_pixel = next(self.allowed_terrain)
            detection: bool = self.image.getpixel(random_pixel) != 0

        return self.image.getpixel(random_pixel)

    def debug_color_img(self) -> None:
        with open("debug/GRAPHED.gif", 'rb') as img_handle:
            self.image = Image.open(BytesIO(img_handle.read()))

            size = self.image.size

        with self.image as img_handle:
            for x in self.terrains[size][0]:
                for y in self.terrains[size][1]:
                    img_handle.putpixel((x, y), value=(255,255,255))

            img_handle.show()



async def main() -> None:
    rand: KamioR = KamioR()


    rand.debug_color_img()



if __name__ == '__main__':
    run(main())
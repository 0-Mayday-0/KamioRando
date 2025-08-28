
from requests import get as rget
from requests import Response
from asyncio import run, create_task, to_thread, Task
from io import BytesIO
from PIL import Image, ImageFile, ImageDraw
from PIL.GifImagePlugin import GifImageFile
from icecream import ic
from time import sleep
from random import choice


class KamioR:
    def __init__(self) -> None:
        self.image: GifImageFile | None = None
        self.url: str = 'https://www-sk.icrr.u-tokyo.ac.jp/realtimemonitor/skev.gif'
        self.allowed_terrain = [list(range(28, 799, 10)), list(range(252, 492, 10))]

    async def _get_img_response(self) -> Response:
        response: Response = await to_thread(rget, self.url)

        return response

    async def get_img_bytes(self) -> bytes | None:
        response_task: Task[Response] = create_task(self._get_img_response())

        response_status: Response = await response_task

        if response_status.status_code == 200:
            return response_status.content

    async def create_image(self) -> None:
        img_data: bytes = await self.get_img_bytes()

        try:
            assert img_data
            self.image: ImageFile = Image.open(BytesIO(img_data))

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
        with self.image as img_handle:
            draw = ImageDraw.Draw(img_handle)
            for y in self.allowed_terrain[1]:
                for x in self.allowed_terrain[0]:
                    img_handle.putpixel((x, y), value=(255,255,255))

            img_handle.show()



async def main() -> None:
    rand: KamioR = KamioR()

    while True:
        ic(await rand.get_random_detect())
        sleep(0.3)

if __name__ == '__main__':
    run(main())
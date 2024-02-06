import asyncio
import logging
import sys
import threading


from aiohttp import ClientSession
import cv2

sys.path = ['/Users/epanchincev/dev/home_infra'] + sys.path  # noqa
from api_client.local_api import local
from face_recognition_local.face_recognition import face_rec, FaceRec
from bot import bot


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s    %(levelname)s    %(message)s',
)


async def get_vcap(door_id: int) -> cv2.VideoCapture:
    async with ClientSession() as session:
        url = await local.get_video_link(session, door_id)
    
    logging.warning('Создан новый видеозахват')

    return cv2.VideoCapture(url)


class CameraBufferThread(threading.Thread):

    def __init__(
            self,
            vcap: cv2.VideoCapture,
            name: str = 'camera-buffer-cleaner-thread',
            *args, **kwargs,
        ) -> None:
        self.vcap = vcap,
        self.last_frame = None,
        self.finished = None,
        super(CameraBufferThread, self).__init__(name=name)
        self.start()

    def run(self):
        while not self.finished:
            _, self.last_frame = self.vcap.read()

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.finished = True
        self.join()


async def video_process(door_id: 1):
    vcap = await get_vcap(door_id)
    interval = 0.3
    with CameraBufferThread(vcap) as cam_buffer:
        while await asyncio.sleep(interval, result=True):
            frame = cam_buffer.last_frame
            if frame is not None:
                encodings = face_rec.get_many_faces_encodings(frame)
                if len(encodings) > 0:
                    for encoding in encodings:
                        known_face = face_rec.lookup_known_face(encoding)
                        if known_face:
                            msg = (f'Пришел {known_face.name}.'
                                   f' {known_face.last_percent}%')
                            logging.warning(msg)
                            await bot.send_message(295633219, msg)
                        else:
                            logging.warning('Пришел незнакомый человек.')

                else:
                    logging.info('Фото обработано. Лиц не найдено')




async def update(face: FaceRec):
    while await asyncio.sleep(30, result=True):
        face.load_known_faces()
        logging.warning('Обновил проверяй!')
        

async def main():
    await asyncio.gather(video_process(1), update(face_rec))


if __name__ == '__main__':
    asyncio.run(main())

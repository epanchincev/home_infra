import asyncio
from datetime import datetime
import logging
import pickle
import io
from pathlib import Path

from aiohttp import ClientSession
import numpy as np
import face_recognition

from api_client.local_api import local
from bot import bot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s    %(levelname)s    %(message)s',
)

DATA_FILE = "known_faces.dat"


class FaceRec:
    
    known_face_encodings = []
    known_face_metadata = []
    
    def __init__(self, data_file: str) -> None:
        self._data_file = Path(data_file)
        if self._data_file.is_file():
            self.load_known_faces()

    
    def save_known_faces(self):
        with open(str(self._data_file), "wb") as face_data_file:
            face_data = [self.known_face_encodings, self.known_face_metadata]
            pickle.dump(face_data, face_data_file)


    def load_known_faces(self,) -> None:
        try:
            with open(str(self._data_file), "rb") as face_data_file:
                self.known_face_encodings, self.known_face_metadata = pickle.load(
                    face_data_file
                )
        except FileNotFoundError:
            pass
            

    def register_new_face(self, face_encoding: tuple, name: str) -> None:
        """
        Add a new person to our list of known faces
        """
        # Add the face encoding to the list of known faces
        self.known_face_encodings.append(face_encoding)
        # Add a matching dictionary entry to our metadata list.
        # We can use this to keep track of how many times a person has visited, when we last saw them, etc.
        self.known_face_metadata.append({
            "first_seen": datetime.now(),
            "last_seen": datetime.now(),
            "seen_count": 1,
            "seen_frames": 1,
            "last_percent": 0,
            "name": name,
        })
        
    def lookup_known_face(self, face_encoding: np.array) -> dict | None:
        metadata = None
        
        if len(self.known_face_encodings) == 0:
            return
            
        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if face_distances[best_match_index] < 0.5:
            # If we have a match, look up the metadata we've saved for it (like the first time we saw it, etc)
            metadata = self.known_face_metadata[best_match_index]

            # Update the metadata for the face so we can keep track of how recently we have seen this face.
            metadata["last_seen"] = datetime.now()
            metadata["seen_frames"] += 1
            metadata["seen_count"] += 1
            metadata["last_percent"] = int((1 - face_distances[best_match_index]) * 100)

            logging.info(f'Обнаружен {metadata["name"]}')

        return metadata
    

face = FaceRec(DATA_FILE)


async def update(face: FaceRec):
    while await asyncio.sleep(30, result=True):
        face.load_known_faces()
        logging.warning('Обновил проверяй!')
        
        
async def upgrade(face: FaceRec) -> None:
    await asyncio.sleep(12)
    file = Path('C:\\Dev\\home_infra\\app\\face_recognition\\photo.jpg')
    img = face_recognition.load_image_file(file)
    faces = face_recognition.face_encodings(img)
    face.register_new_face(faces[0], 'Alexey')
    face.save_known_faces()
    logging.warning('Добавил Алексея')
    await asyncio.sleep(12)
    file = Path('C:\\Dev\\home_infra\\app\\face_recognition\\rami.jpg')
    img = face_recognition.load_image_file(file)
    faces = face_recognition.face_encodings(img)
    face.register_new_face(faces[0], 'rami')
    logging.warning('Добавил rami')
    face.save_known_faces()

async def check_face(intercom_id: int):
    async with ClientSession() as session:
        while True:
            start_time = datetime.now()
            snapshot = await local.get_snapshot(session, intercom_id)
            snapshot = io.BytesIO(snapshot)
            snapshot = face_recognition.load_image_file(snapshot)
            faces_encoding = face_recognition.face_encodings(snapshot)
            if len(faces_encoding) > 0:
                for face_encoding in faces_encoding:
                    known_face = face.lookup_known_face(face_encoding)
                    if known_face:
                        logging.info((f'Домофон {intercom_id}. \033[32mПришел {known_face["name"]},' 
                                      f'совпадение {known_face[["last_percent"]]}%\033[0m'))
                        await bot.send_message(
                            295633219, 
                            (f'Домофон {intercom_id}. Пришел {known_face["name"]},' 
                             f'совпадение {known_face[["last_percent"]]}%'),
                        )
                        await local.open_door(session, intercom_id)
                    else:
                        logging.warning(f'Домофон {intercom_id} \033[31mЛицо отсутвует в БД\033[0m')
            else:
                logging.info(f'Домофон {intercom_id}. \033[33mЛица не найдены\033[0m')
            duration = (datetime.now() - start_time)
            logging.info((f'Домофон {intercom_id} '
                          f'- {(duration.microseconds / 1_000_000):.2f} секунд'))
            await asyncio.sleep(1)
            

async def main() -> None:
    await asyncio.gather(*[check_face(i) for i in range(1, 5)], update(face))
    
if __name__ == '__main__':
    asyncio.run(main())
    


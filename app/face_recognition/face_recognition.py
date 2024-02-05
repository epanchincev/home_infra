from datetime import datetime
import io

import pickle
from pathlib import Path

import numpy as np
import face_recognition

from app.core.config import settings
from app.schemas import FaceRecognitionRead

class NotOnlyOneFaceRecognition(Exception):
    pass

class FaceRec:
    
    known_face_encodings = []
    known_face_metadata = []
    
    def __init__(self, data_file: str) -> None:
        self._data_file = Path(data_file)
        self.known_face_encodings = []
        self.known_face_metadata = []

        if self._data_file.is_file():
            self.load_known_faces()

    
    def save_known_faces(self) -> None:
        with self._data_file.open("wb") as face_data_file:
            face_data = (self.known_face_encodings, self.known_face_metadata)
            pickle.dump(face_data, face_data_file)


    def load_known_faces(self) -> None:
        try:
            with self._data_file.open("rb") as face_data_file:
                self.known_face_encodings, self.known_face_metadata = pickle.load(
                    face_data_file
                )
        except FileNotFoundError:
            pass
        
    def get_face_encodings(self, image: bytes) -> np.array:
        image = io.BytesIO(image)
        image = face_recognition.load_image_file(image)
        faces = face_recognition.face_encodings(image)
        if len(faces) != 1:
            raise NotOnlyOneFaceRecognition(
                f'На фото должно быть одно лицо. Распознано {len(faces)}'
            )
        return faces.pop()
            

    def register_new_face(
        self,
        image: bytes,
        name: str,
        from_id: int,
    ) -> FaceRecognitionRead:
        """
        Добавляет новое лицо. В БД лиц.
        """
        face = self.get_face_encodings(image)
        face_meta = FaceRecognitionRead(
                name=name,
                from_id=from_id,
                first_seen=datetime.now(),
                last_seen=datetime.now(),
                seen_count=1,
                last_percent=0,
            )
        self.known_face_encodings.append(face)
        self.known_face_metadata.append(face_meta)
        self.save_known_faces()
        
        return face_meta
        
    def lookup_known_face(self, face_encoding: np.array) -> dict | None:
        metadata = None
        
        if len(self.known_face_encodings) == 0:
            return
            
        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        best_match_distance = face_distances[best_match_index]
        
        if best_match_distance < 0.5:
            metadata = self.known_face_metadata[best_match_index]
            metadata.last_seen = datetime.now()
            metadata.seen_count += 1
            metadata.last_percent = int((1 - best_match_distance) * 100)

        return metadata
    
    def get_all_faces(self) -> list[FaceRecognitionRead]:
        self.load_known_faces()
        return self.known_face_metadata
    
    def get_face(self, id: int) -> FaceRecognitionRead:
        return self.get_all_faces()[id]


face_rec = FaceRec(settings.face_data)

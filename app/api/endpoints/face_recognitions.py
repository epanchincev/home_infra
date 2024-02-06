from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.core.user import current_user
from app.face_recognition_local import face_rec
from app.schemas import FaceRecognitionRead

router = APIRouter()


@router.post(
    '/',
    response_model=FaceRecognitionRead,
    dependencies=[Depends(current_user)]
)
async def add_face_to_recognition_process(
    image: UploadFile = File(...),
    name: str = Form(...),
    from_id: int | None = Form(None),
) -> FaceRecognitionRead:
    """Добавить лицо в распознавание"""
    image = await image.read()
    return face_rec.register_new_face(image, name, from_id)


@router.get(
    '/',
    response_model=list[FaceRecognitionRead],
    dependencies=[Depends(current_user)]
)
async def get_all_faces() -> list[FaceRecognitionRead]:
    return face_rec.get_all_faces()

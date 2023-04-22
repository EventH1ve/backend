from fastapi import APIRouter
from fastapi_sqlalchemy import db
from schemas.venue import ContactPerson
from models.venue import ContactPerson as ModelContactPerson


router = APIRouter()


@router.post('/')
async def registerContactPerson(contactPerson: ContactPerson):
    contactModel = ModelContactPerson(**contactPerson.dict())

    db.session.add(contactModel)
    db.session.commit()

    return {
        "success": True,
        "message": "Contact person registered."
    }
from typing import List
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


@router.get('/', response_model=List[ContactPerson])
async def listContactPersons(skip: int = 0, limit: int = 10):
    contactPersons = db.session.query(ModelContactPerson).offset(skip).limit(limit).all()
    return contactPersons


@router.get('/{id}', response_model=ContactPerson)
async def getContactPersonById(id: int):
    contactPerson = db.session.query(ModelContactPerson).filter(ModelContactPerson.id == id).first()
    return contactPerson if contactPerson else {}

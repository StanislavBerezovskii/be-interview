from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sqlalchemy import select


class CRUDBase:
    """A base class used for all CRUD operations"""
    def __init__(self, model):
        self.model = model

    def get(self, obj_id: int, session: Session):
        """Returns one object by ID from the database"""
        db_obj = session.execute(select(self.model).where(self.model.id == obj_id))
        return db_obj.scalars().first()

    def get_all(self, session: Session):
        """Returns all objects of the class from the database"""
        db_objs = session.execute(select(self.model))
        return db_objs.scalars().all()

    def create(self, obj_in, session: Session, *args, **kwargs):
        """
        Creates a new object in the database.
        Allows for additional arguments for the location model creation
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(self, db_obj, obj_in, session: Session):
        """Updates an existing object in the database"""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def remove(self, db_obj, session: Session):
        """Removes an object from the database"""
        session.delete(db_obj)
        session.commit()
        return db_obj

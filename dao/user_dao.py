from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
from db import models


class UserDao:

    def create_user(self, user: models.User, db: Session):
        db.add(user)
        db.commit()
        db.close()


user_dao = UserDao()

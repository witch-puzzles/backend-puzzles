from fastapi import Depends

from app.core.database import get_database
from sqlalchemy.orm import Session

database: Session = Depends(get_database)

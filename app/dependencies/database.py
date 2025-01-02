from fastapi import Depends
from typing import Annotated

from app.core.database import get_database
from sqlalchemy.orm import Session

database = Annotated[Session, Depends(get_database)]

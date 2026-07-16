from app.database import engine
from app.database import Base

from app.models.user import User
from app.models.resume import Resume
from app.models.interview import Interview


Base.metadata.create_all(
    bind=engine
)


print("Database Tables Created Successfully")
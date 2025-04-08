from pydantic import BaseModel
from datetime import datetime
from db.models import Priority
from typing import Optional


class UploadTask(BaseModel):
    title: str
    description: str
    priority: Optional[Priority] = None
    due_date: datetime
    repeat_rule: str

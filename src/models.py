from datetime import datetime
from typing import Optional, TypedDict


class TodoItemDict(TypedDict):

    id: int                     
    title: str                   
    description: str             
    completed: bool              
    priority: str             
    tags: list[str]             
    created_at: datetime        
    updated_at: datetime        
    due_date: Optional[datetime] 

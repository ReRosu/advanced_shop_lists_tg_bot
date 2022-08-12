from pydantic import BaseModel


class BugReportInDb(BaseModel):
    id: int
    message: str
    user_id: int
    is_done: bool


class AddBugReportInDb(BaseModel):
    message: str
    user_id: int


from datetime import datetime
from beanie import Document


class LoanExtension(Document):
    loan_id: str
    extension_days: int
    original_due_date: datetime
    extended_due_date: datetime
    extension_no: int

    class Settings:
        name = "LoanExtension"
import pydantic

class Message(pydantic.BaseModel):
    message: str
    
    def __init__(self, message: str):
        self.message = message

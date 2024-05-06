from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    authjwt_secret_key: str=os.getenv("SECRET_KEY")

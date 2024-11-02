from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    AWS_REGION = os.getenv("AWS_REGION")
    # Otras configuraciones

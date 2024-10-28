from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
API_KEY = os.getenv("API_KEY")  # Correct way to retrieve the API key


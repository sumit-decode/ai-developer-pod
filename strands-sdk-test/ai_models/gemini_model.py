from strands.models.gemini import GeminiModel
import os
from dotenv import load_dotenv

load_dotenv()

gemini_model: GeminiModel = GeminiModel(
    model_id="gemini-2.5-flash",
    client_args={
        "api_key": os.getenv("GOOGLE_API_KEY")
    }
)
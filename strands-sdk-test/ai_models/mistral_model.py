from strands.models.mistral import MistralModel
import os
from dotenv import load_dotenv

load_dotenv()

mistral_model: MistralModel = MistralModel(
    model_id="devstral-latest",
    api_key=os.getenv("MISTRAL_API_KEY"),
    max_tokens=8192,
    temperature=0.7,
)

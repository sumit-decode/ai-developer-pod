from strands.models.ollama import OllamaModel

ollama_model: OllamaModel = OllamaModel(
    model_id = "gemma:2b",
    host="http://localhost:11434"
)


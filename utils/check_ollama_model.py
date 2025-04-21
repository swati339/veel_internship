import ollama
import logging

def model_exist(model_name: str) -> bool:
    
    # Check if a model is installed locally using Ollama.
    
    try:
        local_models = ollama.list()["models"]  
        installed_names = [model["model"].split(":")[0] for model in local_models]
        return model_name in installed_names
    except Exception as e:
        logging.error(f"Error checking installed models: {e}")
        return False

print(model_exist("qwen"))
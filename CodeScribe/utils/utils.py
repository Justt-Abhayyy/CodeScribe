import os
from pathlib import Path

def get_prompt(prompt_name: str) -> str:
    # Assuming prompts are in CodeScribe/prompts and this is CodeScribe/utils/utils.py
    # We go up one level from utils to CodeScribe, then into prompts
    current_dir = Path(__file__).parent
    prompt_path = current_dir.parent / "prompts" / f"{prompt_name}.txt"
    
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

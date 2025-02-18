import os
from pathlib import Path
from replicate.client import Client

replicate = Client(
    api_token=os.getenv('REPLICATE_API_TOKEN'),
    headers={
        "User-Agent": "my-app/1.0"
    }
)

DATA_DIR_GENERATED = Path.cwd() / "generated"
DATA_DIR_GENERATED.mkdir(exist_ok=True)

def generate_thumbnail(prompt):
    return replicate.run(
        "recraft-ai/recraft-v3",
        input={
            "size": "1024x1024",
            "style": "any",
            "prompt": prompt
        }
    )

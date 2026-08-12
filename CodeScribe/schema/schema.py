from pydantic import RootModel, BaseModel
from typing import Dict, Optional

from CodeScribe.config.constants import LiteLLMConfig

class LLMConfig(BaseModel):
    model: str = LiteLLMConfig.DEFAULT_MODEL
    provider: Optional[str] = None

class FileSummaries(RootModel[Dict[str, str]]):
    pass

class ReadmeResponse(BaseModel):
    final_readme: str

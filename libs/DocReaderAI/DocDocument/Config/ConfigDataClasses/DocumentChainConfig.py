from dataclasses import dataclass
from typing import List, Dict

from langchain.prompts import PromptTemplate


@dataclass
class DocumentChainConfig:
    prompt_template: Dict[str, str]
    prompt_inputs: List[str]
    temperature: float
    model_name: str
    verbose: bool
    chain_document_type: str
    chain_kwargs: Dict[str, PromptTemplate]
    return_sources: bool

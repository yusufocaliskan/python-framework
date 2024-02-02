from typing import Any

from pydantic import BaseModel, Field

AGENT_INDEX_STR = "next agent to run"
REASON_STR = "reason to select this agent"


class GuidanceChainParser(BaseModel):
    agent_index: int = Field(description=AGENT_INDEX_STR)
    agent_name: str = Field(description="Name of chosen agent without space for example; 'ConversationAgent', "
                                        "'DocumentAgent'")
    reason: str = Field(description=REASON_STR)
    document_uuid: Any = Field(description="Related document uuid to user question.")

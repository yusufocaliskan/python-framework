from DocDocument.Config.Config import config
from Model.Agents.BaseAgent import BaseAgent


class ConversationAgent(BaseAgent):
    """Consists of Conversation and Feedback chain.
    ConversationChain is responsible from general conversations with user.
    FeedbackChain is responsible from returning feedback to user based on conversation
    """

    def __init__(self, chain_names=config["agents"]["ConversationAgent"]["chains"]):
        super().__init__(chain_params=[{"chain_name": chain_name}
                                       for chain_name in chain_names])

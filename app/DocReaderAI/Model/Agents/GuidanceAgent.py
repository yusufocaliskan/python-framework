# Imports
from tenacity import retry, stop_after_attempt

from DocDocument.Config.Config import config
from Model.Agents.BaseAgent import BaseAgent
from Model.Parsers.Parsers import GuidanceChainParser


class GuidanceAgent(BaseAgent):
    """Guidance Agent for AI teacher.
    Responsible from selecting other agents in AI teacher
    """

    def __init__(self, chain_names=config["agents"]["GuidanceAgent"]["chains"]):
        super().__init__(chain_params=[{"chain_name": chain_name} for chain_name in chain_names])

        # Definitions for all agents.
        # We embed this to prompt
        self._pdf_definitions = None

    @property
    def pdf_definitions(self):
        # If pdf_definition is None or "" string, we need to return a placeholder to use in GuidanceChain prompt
        if self._pdf_definitions is None or self._pdf_definitions == "":
            return "No definition given"

        return self._pdf_definitions

    @pdf_definitions.setter
    def pdf_definitions(self, value):
        self._pdf_definitions = value

    @retry(stop=stop_after_attempt(3))
    def choose_next_agent(self) -> (int, str):
        """Chooses next agent to run for AI teacher

        Raises:
            Exception: ValueError

        Returns:
            (int, str): agent index, agent name
        """

        try:
            _, responses, _ = self.run_chains(
                chains_params={}
            )  # type: (_, list[GuidanceChainParser],_)

            agent_index = responses[0].agent_index
            agent_name = responses[0].agent_name
            document_uuid = responses[0].document_uuid

            # Check if agent name has white space or not (we do not want white space)
            if not agent_name.isspace():
                agent_name = config["AGENTS_NAMES"][agent_index]
        except Exception as e:
            print(e)
            raise ValueError

        return agent_index, agent_name, document_uuid

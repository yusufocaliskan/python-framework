import random
from dataclasses import dataclass
from textwrap import dedent
from typing import Union, Dict, Any

from icecream import ic

from DocDocument.Config.Config import config
from Model.Agents.BaseAgent import BaseAgent
from Model.Agents.ConversationAgent import ConversationAgent
from Model.Agents.DocumentAgent import DocumentAgent
from Model.Agents.GuidanceAgent import GuidanceAgent
from Model.Memory.Memory import BaseMemory
from Model.PDFWorker.PDFWorker import PDFWorker


# Dataclass to convert agent choice when needed
@dataclass
class AgentIndex:
    min: int
    max: int


class DocDocumentMemory(BaseMemory):
    """DocDocument conversation memory"""

    def __init__(self):
        super().__init__()


class DocDocument:
    def __init__(self, pdf_worker: PDFWorker, user_uuid: Any, use_only_document_agent: bool = False):
        # Assign teacher name
        self._ai_name: str = "DocDocument"

        # Assign User UUID
        self.__user_uuid = user_uuid

        # Create memory
        self._memory: BaseMemory = DocDocumentMemory()

        # Last user input
        self._user_input: Union[str, None] = None

        # User name
        self._user_name = "User"

        self._number_of_agents = None

        # Assign pdf_worker to be able to use in the future
        self._pdf_worker = pdf_worker

        # Guidance Agent to choose between agents
        self.__guidance_agent = GuidanceAgent()
        self.assign_attributes_to_agent(agent=self.__guidance_agent)

        self.__agents: Dict[str, Dict] = {}

        # Whether to use only use document agent
        self._use_only_document_agent = use_only_document_agent

        if not use_only_document_agent:
            self.__conversation_agent = ConversationAgent()
            self.assign_attributes_to_agent(agent=self.__conversation_agent)
            self.__agents["ConversationAgent"] = {"agent": self.__conversation_agent,
                                                  "definition": "* If the user wants to communicate without specific "
                                                                "inquiries, route the user to the ConversationAgent"}

        self.__document_agent = DocumentAgent(
            pdf_worker=self._pdf_worker, user_uuid=self.__user_uuid)
        self.assign_attributes_to_agent(self.__document_agent)
        self.__agents["DocumentAgent"] = {
            "agent": self.__document_agent,
            "definition": dedent(f"""
            * If the user explicitly requests information from a pdf below,route the user to the DocumentAgent
                {pdf_worker.combine_pdf_definitions(self.__user_uuid)}""")
        }

    @property
    def user_name(self):
        return self._user_name

    @property
    def memory(self):
        return self._memory

    @user_name.setter
    def user_name(self, value):
        self._user_name = value

    @property
    def user_input(self):
        return self._user_input

    @user_input.setter
    def user_input(self, value: str):
        """User input set method. Changes user input class variable.
        Also add memory a new message by user

        Args:
            value (str): _description_
        """
        self._user_input = value
        self._memory.append(by=self._user_name, message=value)

    @property
    def number_of_agents(self):
        self._number_of_agents = len([*self.__agents])
        return self._number_of_agents

    @property
    def agents(self):
        return self.__agents

    def __str__(self):
        text = f"{self._ai_name}\n" + "\n".join(
            [
                f"{index + 1}. {agent_name}"
                for index, agent_name in enumerate([*self.__agents])
            ]
        )
        return text

    def assign_attributes_to_agent(self, agent: BaseAgent):
        agent.ai_name = self._ai_name
        agent.memory = self._memory
        agent.question = self._user_input

    def start(self):
        """Returns a random starting conversation string from config file. Also
        adds chosen conversation to memory.

        Returns:
            str: random starting conversation for AI teacher
        """
        # Choose a random starting text from config file and change AI name to
        # decide one
        start_text = random.choice(
            config["PossibleStartingConversations"]
        ).format(ai_name=self._ai_name)

        # Add to memory
        self.add_to_memory(by=self._ai_name, message=start_text)

        return start_text

    def choose_next_agent(self) -> (int, str):
        """Determines next agent to answer user prompt according to conversation history.
        Uses GuidanceAgent to select next agent.

        Returns:
            (int, str): agent_index in AGENTS array, agent name
        """

        # Calls for GuidanceAgent which is responsible from selecting next agent to
        # answer user prompt, according to conversation history.
        guidance_agent = self.__guidance_agent  # type: GuidanceAgent

        guidance_agent.pdf_definitions = self._pdf_worker.combine_pdf_definitions(
            self.__user_uuid)
        guidance_agent.question = self._user_input
        agent_index, agent_name, uuid = guidance_agent.choose_next_agent()

        # If we only use document agent, we just need to ignore others
        return agent_index, agent_name, uuid

    def run_agent_by_name(self, agent_name: str, **kwargs) -> str:
        """Run agent by name.
        The Name of the agent must be same with config file naming

        Args:
            agent_name (str): Name of agent

        Returns:
            str: Answer of agent
        """
        # Change text variable in the agent
        self.__agents[agent_name]["agent"].question = self._user_input

        _, responses, _ = self.__agents[agent_name]["agent"].run_chains(
            **kwargs)

        message = "\n".join(responses)
        self.add_to_memory(by=self._ai_name, message=message,
                           agent_name=agent_name)
        return message

    def add_to_memory(self, by: str, message: str, **kwargs: Any):
        """Appends to a memory array.

        Args:
            by (str): Message owner. Can be user or teacher
            message (str): Message string
            **kwargs (dict): Keyword arguments. See below

            Keyword arguments:
                agent_name (str): Name of agent used to produce a message. Defaults to ""
                timestamp (float): Timestamp value. Defaults to current time.
        """

        # Append a message to memory
        self._memory.append(
            by=by,
            message=message,
            agent_name=kwargs.get("agent_name", None),
            timestamp=kwargs.get("timestamp", None),
        )

    def main_loop(self):
        print(
            f"{self._ai_name}: {self.start()}\n------------------------------------------------")
        while True:
            self.user_input = input("User Input: ")
            print("----------------------------------------------------------------")
            _, agent_name, document_uuid = self.choose_next_agent()
            ic(_, agent_name, document_uuid)
            if document_uuid:
                answer = self.run_agent_by_name(agent_name=agent_name,
                                                document_uuid=document_uuid,
                                                user_uuid=self.__user_uuid)
            else:
                answer = self.run_agent_by_name(agent_name=agent_name)
            print(
                f"{self._ai_name}: {answer}\n------------------------------------------------"
            )

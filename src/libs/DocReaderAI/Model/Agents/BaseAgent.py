# Imports
from typing import List, Dict, Union, Tuple, Any

from DocDocument.Config.Config import config
from Model.Chains.ChainFactory import ChainFactory


class BaseAgent:
    """Parent agent class.
    Other agents inherit from this class
    """

    def __init__(self, chain_params: List[Dict[str, Union[str, dict]]]):
        self._chains = {
            chain_param["chain_name"]: ChainFactory.create_chain(**chain_param) for chain_param in chain_params
        }

        # Name of the AI using this agent. We use this information in prompt templates
        self._ai_name: Union[str, None] = None

        # Memory of the AI using this agent. We use this information in prompt templates
        self._memory: Union[str, None] = None

        # Name of the agent. Generally we use this information to separate different agents
        self._agent_name = self.__class__.__name__

        # Lastly run chain to follow chain usage
        self._last_run_chain: Union[str, None] = None

        # Question variable in Human section. It is last user input
        self._question: Union[str, None] = None

    @property
    def agent_name(self):
        return self._agent_name

    @property
    def chains(self):
        return self._chains

    @property
    def ai_name(self):
        return self._ai_name

    @ai_name.setter
    def ai_name(self, value):
        self._ai_name = value

    @property
    def memory(self):
        return self._memory

    @memory.setter
    def memory(self, value):
        self._memory = value

    @property
    def question(self):
        return self._question

    @question.setter
    def question(self, value):
        self._question = value

    def __str__(self):
        return self._agent_name

    def run_chain(
            self, chain_name: str, chain_params: Dict[str, Union[str, float, bool]]
    ) -> str:
        """Runs a chain with given name

        Args:
            chain_name (str): Name of the chain we would like to run
            chain_params (Dict[str, Union[str, float, bool]]): Parameters for given chain

        Returns:
            str: Answer of chosen chain
        """

        # Change last run chain
        self._last_run_chain = self._chains[chain_name]

        # Create inputs dictionary to feed to LLM
        inputs = {
            input_name: getattr(self, f"{input_name}")
            if "inputs" not in chain_params or bool(chain_params["inputs"])
            else chain_params["inputs"]
            for input_name in config["chains"][chain_name]["prompt_inputs"]
        }
        # Return answer from LLM
        if "parameters" in chain_params:
            return self._last_run_chain.run(inputs=inputs, **chain_params["parameters"])[0]
        else:
            return self._last_run_chain.run(inputs=inputs)[0]

    def run_chains(
            self,
            chains_params: Dict[str, Dict[str, Dict[str, Any]]] = None,
    ) -> Tuple[List[str], List[str], List[str]]:
        """Runs all chains in the agent and returns answers from them.

        Args:
            chains_params: Dictionary of all chains inputs and parameters. If not given, runs all chains according to
                         class variables. See below for more info

        Returns:
            (List[str], List[str], List[str]): List of all answers with in order,
                                               List of answers of chains,
                                               List of all chains

        Example input:
        {
            -chain name-: {
                "inputs": {-chain inputs-},
                "parameters": {-chain parameters-},
            },
            -chain name-: {
                "inputs": {-chain inputs-},
                "parameters": {-chain parameters-},
            },
        }
        """

        # Temp variables
        answers = []

        # For loop to iterate over chains in the agent
        for chain_name, chain in self._chains.items():
            # Appending chain name to list
            answers.append(chain_name)

            # Create chain parameters input
            chain_params = (
                chains_params[chain_name] if (chains_params is not None) and (chain_name in chains_params) else {}
            )

            # Run chain
            answer = self.run_chain(chain_name=chain_name, chain_params=chain_params)

            # Append answer from chain
            answers.append(answer)

        # Get only response strings
        responses = answers[1::2]

        # Get only chain names
        chains = answers[::2]

        # Return
        return answers, responses, chains

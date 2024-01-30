import os
from importlib import import_module

from langchain.chains.base import Chain

from DocDocument.Config.Config import config


def get_chain_names() -> list[str]:
    """
    Get chain names under Chains.Chains directory
    Returns:

    """
    return [cls.replace(".py", "")
            for cls in os.listdir("Model/Chains/Chains")
            if cls.endswith(".py") and not cls.startswith("__")]


class ChainFactory:
    @staticmethod
    def create_chain(chain_name: str, **kwargs) -> Chain:
        """
        Create and return a chain based on chain_name
        Args:
            chain_name (str): Name of the chain. Must be same name with python files under Model.Chains.Chains
            **kwargs (dict): Chain constructor parameters
        See Also:
            DocumentChain Arguments:
                chain_name (str): Name of the chain. Must be same with config file.
                retrievers (BaseRetriever): Vectorestore retrievers object
                model_name (str): Initial model name of the chain. Defaults to config file
                temperature (float): Initial temperature value of the chain. Defaults to config file
                verbose (bool): Initial verbose value of the chain. Defaults to config file
                chain_type (str): Document chain type. Options are ["stuff", "map_reduce"]
                chain_kwargs (dict): Kwargs for document chain.
                return_sources (bool): Whether to return related sources used while answering.

            GeneralChain Arguments:
                chain_name: Name of the chain. Must be same with config file.
                model_name: Initial model name of the chain. Defaults to config file
                temperature: Initial temperature value of the chain. Defaults to config file
                verbose: Initial verbose value of the chain. Defaults to config file
                use_parser: Initial parser requirement bool. Defaults to config file.

        Returns:
            (Chain): Chain with given name

        """

        # Get possible chain names to check
        possible_chains = get_chain_names()

        # Get chain type
        chain_type: str = config["chains"][chain_name]["chain_type"]

        if chain_type not in possible_chains:
            raise ValueError(f"{chain_type} does not exist.")
        else:
            # Import module from folder
            module = import_module("Model.Chains.Chains." + chain_type)

            # Return instance of chain
            return getattr(module, chain_type)(chain_name, **kwargs)

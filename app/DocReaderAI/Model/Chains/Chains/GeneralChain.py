from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel

from DocDocument.Config.Config import config, OPEN_AI_API_KEY
from Model.Chains.BaseChains.BaseGeneralChain import BaseGeneralChain


class GeneralChain(object):
    """DocumentChain class to be used in Teach AI Agents' chains. All chains in the application
    inherits this class.
    """

    def __init__(self, chain_name: str, **kwargs):
        """Constructor of DocumentChain class.

        Args:
            :param chain_name: Name of the chain. Must be same with config file.
            :param **kwargs: Keyword arguments. See below

            Keyword arguments:
                model_name: Initial model name of the chain. Defaults to config file
                temperature: Initial temperature value of the chain. Defaults to config file
                verbose: Initial verbose value of the chain. Defaults to config file
                use_parser: Initial parser requirement bool. Defaults to config file.
        """
        self._chain_name = chain_name
        self._chain_config = config["chains"][chain_name]

        # Kwargs parameters with default values
        self._model_name = kwargs.get("model_name", self._chain_config["model_name"])
        self._temperature = kwargs.get("temperature", self._chain_config["temperature"])
        self._verbose = kwargs.get("verbose", self._chain_config["verbose"])
        self._use_parser = kwargs.get("use_parser", self._chain_config["use_parser"])

    def run(self, inputs, **kwargs) -> (BaseModel, LLMChain):
        """Runs the chain according to inputs and keyword arguments

        Args:
            inputs (dict): Required inputs for chain's prompt template.
            **kwargs (dict): Keyword arguments. See below

            Keyword arguments:
                model_name(str): Initial model name of the chain. Defaults to config file
                temperature(float): Initial temperature value of the chain. Defaults to config file
                verbose(bool): Initial verbose value of the chain. Defaults to config file

        Returns:
            (response, chain) (tuple): Response is string answer from chain. DocumentChain is the used chain object
        """

        # Creating LLM
        llm = ChatOpenAI(
            model_name=kwargs.get("model_name", self._model_name),
            openai_api_key=OPEN_AI_API_KEY,
            temperature=kwargs.get("temperature", self._temperature),
        )

        # Create chain from BaseDocumentChain
        chain = BaseGeneralChain.runChain(
            llm=llm,
            chain_name=self._chain_name,
            verbose=kwargs.get("verbose", self._verbose),
            use_parser=self._use_parser,
        )
        #
        # # Getting answer with inputs from created chain
        # if self._use_parser:
        #     answer = chain.predict_and_parse(**inputs)
        # else:
        #     answer = chain.run(**inputs)
        answer = chain.run(**inputs)
        # Return both answer and chain itself
        return answer, chain

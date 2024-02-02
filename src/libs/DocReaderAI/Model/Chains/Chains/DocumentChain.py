from typing import Dict, Any

from dacite import from_dict
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.schema.document import Document
from langchain.schema.retriever import BaseRetriever

from DocDocument.Config.Config import config, OPEN_AI_API_KEY
from DocDocument.Config.ConfigDataClasses.DocumentChainConfig import DocumentChainConfig
from Model.Chains.BaseChains.BaseDocumentChain import BaseDocumentChain


class DocumentChain(object):
    """
    DocumentChain class to be used in Teach AI Agents' chains. All chains in the application
    inherits this class.
    """

    def __init__(self, chain_name: str, retriever: BaseRetriever, **kwargs):
        """Constructor of DocumentChain class.

        Args:
            chain_name (str): Name of the chain. Must be same with config file.
            retrievers (Dict[BaseRetriever]): List of Chroma vectorstore retrievers
            **kwargs (dict): Keyword arguments. See below

            Keyword arguments:
                model_name (str): Initial model name of the chain. Defaults to config file
                temperature (float): Initial temperature value of the chain. Defaults to config file
                verbose (bool): Initial verbose value of the chain. Defaults to config file
                chain_type (str): Document chain type. Options are ["stuff", "map_reduce"]
                chain_kwargs (dict): Kwargs for document chain.
                return_sources (bool): Whether to return related sources used while answering.
                
        """
        self._chain_name = chain_name
        self._chain_config = from_dict(data_class=DocumentChainConfig, data=config["chains"][chain_name])

        # Kwargs parameters with default values
        self._model_name = kwargs.get("model_name", self._chain_config.model_name)
        self._temperature = kwargs.get("temperature", self._chain_config.temperature)
        self._verbose = kwargs.get("verbose", self._chain_config.verbose)
        self._chain_type = kwargs.get("chain_type", self._chain_config.chain_document_type)
        self._chain_kwargs = kwargs.get("chain_kwargs", self._chain_config.chain_kwargs)
        self._return_sources = kwargs.get("return_sources", self._chain_config.return_sources)

        # Creating LLM
        llm = ChatOpenAI(
            model_name=kwargs.get("model_name", self._model_name),
            openai_api_key=OPEN_AI_API_KEY,
            temperature=kwargs.get("temperature", self._temperature),
        )

        # Create chain from BaseDocumentChain
        self._chain = BaseDocumentChain.create(llm=llm,
                                               chain_name=self._chain_name,
                                               retriever=retriever,
                                               return_sources=self._chain_config.return_sources,
                                               verbose=self._chain_config.verbose)

    def run(self, inputs, **kwargs) -> (str, str, RetrievalQAWithSourcesChain):
        """Runs the chain according to inputs and keyword arguments

        Args:
            inputs (dict): Required inputs for chain's prompt template.
            **kwargs (dict): Keyword arguments. See below

            Keyword arguments:
                model_name(str): Initial model name of the chain. Defaults to config file
                temperature(float): Initial temperature value of the chain. Defaults to config file
                verbose(bool): Initial verbose value of the chain. Defaults to config file
                retriever (BaseRetriever): Retriever for document we want to work on.

        Returns:
            (response, chain) (tuple): Response is string answer from chain. DocumentChain is the used chain object
        """

        # Change retriever according to chosen document
        retriever: Any = kwargs.get("retriever", None)

        if retriever:
            self._chain.retriever = retriever

            # Getting answer with inputs from created chain
        response = self._chain.execute(**inputs)  # type: dict

        answer = response["answer"]
        source_documents = ""

        if self._chain_config.return_sources:
            for (index, source) in enumerate(response["source_documents"], start=1):  # type: (int, Document)
                source_documents += (f"{index}. Document from Page {source.metadata['page']}\n"
                                     f"-------------------------------------------------------\n"
                                     f"Content:\n"
                                     f"{source.page_content.strip()}\n")

        # Return both answer, source_documents and chain itself
        return answer, source_documents, self._chain

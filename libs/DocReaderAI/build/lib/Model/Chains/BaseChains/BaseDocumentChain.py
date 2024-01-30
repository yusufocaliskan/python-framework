from typing import Dict, Any

from dacite import from_dict
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.prompts import PromptTemplate
from langchain.schema.language_model import BaseLanguageModel
from langchain.schema.retriever import BaseRetriever

from DocDocument.Config.Config import config
from DocDocument.Config.ConfigDataClasses.DocumentChainConfig import DocumentChainConfig


class BaseDocumentChain(RetrievalQAWithSourcesChain):
    """
        Child Class of RetrievalQAWithSourcesChain. Can run by execute function.
    """

    def execute(self, **inputs: dict[str, str]) -> dict[str, Any]:
        """
        Run the document chain
        Args:
            inputs (Dict[str, str]): Prompt inputs

        Returns:
            response (Dict[str, Any]): Response to given inputs with prompt template
        """

        return self.__call__(inputs=inputs)

    @classmethod
    def create(
            cls,
            llm: BaseLanguageModel,
            chain_name: str,
            retriever: BaseRetriever,
            return_sources: bool,
            verbose: bool = False) -> RetrievalQAWithSourcesChain:
        # Read config and get information according to chain name
        chain_config = from_dict(data_class=DocumentChainConfig, data=config["chains"][chain_name])

        # Check if inputs have "summaries" and "question" input keys.
        # If do not (which is normal behaviour), add them
        for element in ["summaries", "question"]:
            if element not in chain_config.prompt_inputs:
                chain_config.prompt_inputs.append(element)

        # Combined prompt template
        prompt_string = "\n".join(chain_config.prompt_template.values())

        # Prompt template of chain
        prompt = PromptTemplate(
            template=prompt_string,
            input_variables=chain_config.prompt_inputs
        )

        # Assigning prompt to chain_kwargs
        chain_config.chain_kwargs["prompt"] = prompt

        # Create Combine Documents Chains
        combine_documents_chain = load_qa_with_sources_chain(llm=llm,
                                                             chain_type=chain_config.chain_document_type,
                                                             verbose=verbose,
                                                             **chain_config.chain_kwargs
                                                             )

        # Return RetrievalQAWithSourcesChain instance with given inputs
        return cls(combine_documents_chain=combine_documents_chain,
                   retriever=retriever,
                   return_source_documents=return_sources)

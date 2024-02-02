from langchain.chains.llm import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema.language_model import BaseLanguageModel

from DocDocument.Config.Config import config
from Model.Parsers import Parsers


class BaseGeneralChain(LLMChain):
    """Child class of LLMChain. Have a class method to return a LLMChain object with
    given inputs
    """

    @classmethod
    def runChain(
            cls,
            llm: BaseLanguageModel,
            chain_name: str,
            verbose: bool = False,
            use_parser: bool = False,
    ) -> LLMChain:
        """
        Class method to return a LLMChain object with given inputs.

        :param llm: BaseLLM object to use for LLMChain.
        :param chain_name: Name of the chain to run.
        :param verbose: Verbose value of the chain.
        :param use_parser: Whether to use parser or not.
        :return: LLMChain
        """

        # Read config and get information according to chain name
        chain_config = config["chains"][chain_name]
        messages = [
            SystemMessagePromptTemplate.from_template(
                chain_config["prompt_template"]["system_prompt_template"]
            ),
            HumanMessagePromptTemplate.from_template(
                chain_config["prompt_template"]["human_prompt_template"]
            ),
        ]
        prompt_input = chain_config["prompt_inputs"]

        if use_parser:
            parser_cls = getattr(Parsers, chain_name + "Parser")
            parser = PydanticOutputParser(pydantic_object=parser_cls)

            # Prompt template of chain
            prompt = ChatPromptTemplate(
                messages=messages,
                input_variables=prompt_input,
                output_parser=parser,
                partial_variables={
                    "format_instructions": parser.get_format_instructions()
                },
            )

            # Returns a LLMChain object which can be used to get response from OpenAI ChatGPT.
            return cls(prompt=prompt, llm=llm, verbose=verbose, output_parser=parser)
        else:
            # Prompt template of chain
            prompt = ChatPromptTemplate(messages=messages, input_variables=prompt_input)

        # Returns a LLMChain object which can be used to get response from OpenAI ChatGPT.
        return cls(prompt=prompt, llm=llm, verbose=verbose)

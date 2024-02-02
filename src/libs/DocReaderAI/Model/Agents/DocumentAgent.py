from typing import Union, Tuple, List

from DocDocument.Config.Config import config
from Model.Agents.BaseAgent import BaseAgent
from Model.PDFWorker.PDFWorker import PDFWorker


class DocumentAgent(BaseAgent):

    def __init__(self, pdf_worker: PDFWorker, user_uuid: str, chain_names=config["agents"]["DocumentAgent"]["chains"]):
        super().__init__(chain_params=[{"chain_name": chain_name,
                                        "retriever": pdf_worker.get_retriever_no_filter()}
                                       for chain_name in chain_names])
        self._pdf_worker = pdf_worker
        self._summaries: Union[str, None] = None

    @property
    def summaries(self):
        return self._summaries

    def run_chains(self, **kwargs) -> Tuple[List[str], List[str], List[str]]:
        # Get retriever
        user_uuid: str = kwargs.get("user_uuid", None)
        document_uuid: str = kwargs.get("document_uuid", None)

        if user_uuid and document_uuid:
            retriever = self._pdf_worker.get_retriever(user_uuid=user_uuid, document_uuid=document_uuid)
            chains_params = {
                "DocumentChain": {
                    "parameters": {
                        "retriever": retriever
                    }
                }
            }

            answers, responses, chains = super().run_chains(chains_params=chains_params)
            return answers, responses, chains

# IMPORTS
from .Model.PDFWorker.PDFWorker import PDFWorker
from .Model.AI.DocDocument import DocDocument
import os


class DocReaderAI:

    pdf_worker = PDFWorker()
    theAgent = ''

    def __init__(self):
        path = os.getcwd()

        self.pdf_worker.add_pdf(pdf_path=path+"/libs/DocReaderAI/DocDocument/Document/hasan_ozkul.pdf",
                                pdf_definition="Hasan Özkul's resume",
                                user_uuid=1,
                                document_uuid=1)

        # print(pdf_worker.get_retriever_by_document_uuid(1))
        self.pdf_worker.add_pdf(pdf_path=path+"/libs/DocReaderAI/DocDocument/Document/RamazanBurakKorkmaz_16072023.pdf",
                                pdf_definition="Ramazan Burak Korkmaz's resume",
                                user_uuid=1,
                                document_uuid=2)

    def addFile(self, filePath, defs, userId, docId):
        self.pdf_worker.add_pdf(pdf_path=filePath,
                                pdf_definition=defs,
                                user_uuid=userId,
                                document_uuid=docId)

    # Add some files
    def setFiles2TheAgentsMind(self, userId):
        self.theAgent = DocDocument(
            pdf_worker=self.pdf_worker, user_uuid=userId)

    # Ask question to the agent
    def getAnswer(self,  question):
        return self.theAgent.procressQuestions(question=question)

# IMPORTS
from Model.PDFWorker.PDFWorker import PDFWorker
from Model.AI.DocDocument import DocDocument
import os


class DocReaderAI:
    def __init__(self):
        path = os.getcwd()
        pdf_worker = PDFWorker()

        pdf_worker.add_pdf(pdf_path=path+"/libs/DocReaderAI/DocDocument/Document/hasan_ozkul.pdf",
                           pdf_definition="Hasan Özkul's resume",
                           user_uuid=1,
                           document_uuid=1)

        # print(pdf_worker.get_retriever_by_document_uuid(1))
        pdf_worker.add_pdf(pdf_path=path+"/libs/DocReaderAI/DocDocument/Document/RamazanBurakKorkmaz_16072023.pdf",
                           pdf_definition="Ramazan Burak Korkmaz's resume",
                           user_uuid=1,
                           document_uuid=2)

        doc_document = DocDocument(pdf_worker=pdf_worker, user_uuid=1)
        doc_document.main_loop()

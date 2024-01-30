# create the length function
from dataclasses import dataclass
from typing import List, Any, Dict

import tiktoken
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma

from DocDocument.Config.Config import OPEN_AI_API_KEY

# OpenAIEmbeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPEN_AI_API_KEY)


@dataclass
class PDFFile:
    path: str
    chunks: List[Document]
    pdf_definition: str
    index: int
    ids: list


def tiktoken_len(text):
    """Calculate the length of a text in tokens using the 'cl100k_base' tokenizer.

    Args:
        text (str): The input text.

    Returns:
        int: The length of the text in tokens.
    """

    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)


# PDFWorker CLASS
def load_pdf_file(pdf_path: str, pdf_definition: str, user_uuid: Any, document_uuid: Any):
    """Load a PDF file and return a list of Document objects.

    Args:
        pdf_path (str): The path to the PDF file.
        pdf_definition (str): Short definition of pdf content
        document_uuid (Any): Unique id of this pdf
        user_uuid (Any): Unique id of user who uploads this pdf

    Returns:
        List[Document]: A list of Document objects representing the pages of the PDF.
    """

    # Load and convert pdf file to langchain Documents
    pdf_docs = PyPDFLoader(pdf_path).load()

    # Adding Definition and UUID to metadata
    for doc in pdf_docs:
        doc.metadata["pdf_definition"] = pdf_definition
        doc.metadata["uuid"] = f"{user_uuid}_{document_uuid}"
    return pdf_docs


def create_chunks(pdf_file: List[Document], chunk_size=1000, chunk_overlap=200):
    """
    Split a list of Document objects into smaller chunks.

    Args:
        pdf_file (List[Document]): The list of Document objects representing the pages of the PDF.
        chunk_size (int, optional): The size of each chunk in tokens. Default to 1000.
        chunk_overlap (int, optional): The overlap between adjacent chunks in tokens. Defaults to 200.

    Returns:
        List[Document]: A list of Document objects representing the chunks of the document.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        # Set a tiny chunk size, just to show.
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=tiktoken_len,
    )

    return text_splitter.split_documents(pdf_file)


def create_ids(user_uuid: Any, document_uuid: Any, chunk_len: int):
    """Create unique IDs for each chunk of a document.

    Args:
        user_uuid (Any): User unique id.
        document_uuid (): Document unique id. We distinguish pdf files of same user this way.
        chunk_len (int): Length of chunks list.

    Returns:
        List[str]: A list of unique IDs for each chunk.
    """

    return [f"{user_uuid}_{document_uuid}_{i}" for i in range(0, chunk_len, 1)]


def get_texts_and_metadata(chunks: List[Document]):
    texts = [c.page_content for c in chunks]
    metadata = [c.metadata for c in chunks]
    return texts, metadata


class PDFWorker:
    # PDF Dictionary
    __pdfs: Dict[str, Dict[str, PDFFile]]

    def __init__(self,
                 collection_name: str = "PDFWORKER",
                 k: int = 3):
        """Initialize the PDFWorker class.

        Args:
            collection_name (str): Redis index name. Defaults to "PDFWORKER"
            k (int): The number of nearest neighbors to retrieve.
        """
        self.__collection_name: str = collection_name
        self.__chroma_db = Chroma(collection_name, embeddings)
        self.__pdfs = {}

    @property
    def pdfs(self):
        return self.__pdfs

    def add_pdf(self,
                pdf_path: str,
                pdf_definition: str,
                user_uuid: Any,
                document_uuid: Any,
                chunk_size=400,
                chunk_overlap=50):

        if user_uuid in self.__pdfs.keys() and document_uuid in self.__pdfs[user_uuid].keys():
            return

        # Load documents
        docs = load_pdf_file(pdf_path=pdf_path,
                             pdf_definition=pdf_definition,
                             user_uuid=user_uuid,
                             document_uuid=document_uuid)

        # Create chunks from pdf documents
        chunks = create_chunks(pdf_file=docs,
                               chunk_size=chunk_size,
                               chunk_overlap=chunk_overlap)

        ids = self.__chroma_db.add_documents(documents=chunks)

        # Assign related information to dictionary
        try:
            self.__pdfs[user_uuid][document_uuid] = PDFFile(path=pdf_path,
                                                            index=len(self.__pdfs.keys()) + 1,
                                                            ids=ids,
                                                            chunks=chunks,
                                                            pdf_definition=pdf_definition)
        except KeyError:
            self.__pdfs[user_uuid] = {}
            self.__pdfs[user_uuid][document_uuid] = PDFFile(path=pdf_path,
                                                            index=len(self.__pdfs.keys()) + 1,
                                                            ids=ids,
                                                            chunks=chunks,
                                                            pdf_definition=pdf_definition)

    def delete_pdf(self, user_uuid: Any, document_uuid: Any):
        try:
            self.__chroma_db.delete(self.__pdfs[user_uuid][document_uuid].ids)
        except ValueError as exception:
            print(exception)

    def search(self, query):
        return self.__chroma_db.similarity_search(query=query)

    def get_retriever_no_filter(self):
        return self.__chroma_db.as_retriever(search_type="similarity")

    def get_retriever(self, user_uuid: Any, document_uuid: Any):
        return self.__chroma_db.as_retriever(search_type="similarity",
                                             search_kwargs={'filter': {'uuid': f"{user_uuid}_{document_uuid}"}})

    def combine_pdf_definitions(self, user_uuid: Any) -> str:
        temp = ""
        for (key, value) in self.__pdfs[user_uuid].items():
            temp += (f"{value.index}. Document: "
                     f"     * UUID ({type(key).__name__}) = {key}"
                     f"     * Definition: {value.pdf_definition}\n")

        return temp

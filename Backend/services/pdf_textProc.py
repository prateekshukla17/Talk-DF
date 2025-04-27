import os
import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import retrieval_qa
from langchain.chat_models import ChatOpenAI

class pdf_processing:
    def __init__(self):
        self.upload_dir = "uploads"
        self.vector_dir = "vectorstore"

        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.vector_dir, exist_ok=True)

        self.embeddings = OpenAIEmbeddings()

        self.llm = ChatOpenAI(model_name = "gpt-3.5-turbo",temperature = 0)



    def extract_text(self, file_path):
        text = ""

        try:
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
                return text
        except Exception as e:
            print(f'Error  opening the file{e}')
            return None
    

    def createVectorEmbeddings(self,document_id, text):
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap=200,length_function=len)
            chunks = text_splitter.split_text(text=text)

            vectorStore_path = os.path.join(self.vector_dir,f"doc_{document_id}")

            vectorStore = Chroma.from_texts(
                text = chunks,
                embeddings = self.embeddings,
                persist_directory = vectorStore_path
            )

            vectorStore.persist()
            return vectorStore_path
        except Exception as e:
            print(f"Error Creating a vector Store:{e}")
            return None
        
    def load_vector_store(self,vectorstore_id):
        try:
            vectorStore = Chroma(
                persist_directory = vectorstore_id,
                embedding_function = self.embeddings
            )

            return vectorStore
        except Exception as e:
            print(f'Error Loading a vector store : {e}')
            return None

    
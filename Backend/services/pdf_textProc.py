import os  
import fitz # a library for working with pdf files
import warnings
from dotenv import load_dotenv # Loads environment variables from a .env file.
from langchain.text_splitter import RecursiveCharacterTextSplitter  #Splits text into smaller chunks for processing.
from langchain_community.embeddings import HuggingFaceEmbeddings #Generates embeddings using a Hugging Face model.
from langchain_community.vectorstores import FAISS #Vector database to store embeddings
from langchain.chains import create_retrieval_chain # retrieval-based chain for question answering.
from langchain.chains.combine_documents import create_stuff_documents_chain #Combines documents into a chain for processing.
from langchain_core.prompts import ChatPromptTemplate #Defines a prompt template for chat-based interactions.
from langchain_ollama.llms import OllamaLLM #Language Model used


warnings.filterwarnings("ignore")

load_dotenv()

class pdf_processing:
    def __init__(self):   
        self.upload_dir = "uploads"
        self.vector_dir = "vectorstore"

        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.vector_dir, exist_ok=True)

        self.embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-xl")
        self.llm = OllamaLLM(model="llama3.2:3b")
        #self.llm = HuggingFaceHub(repo_id="google/gemma-3-1b-pt", model_kwargs={"temperature":0.5, "max_length":512})


    def extract_text(self, file_path): # 
        """
        Extracts text content from a PDF file.
        Args:
            file_path (str): The path to the PDF file to be processed.
        Returns:
            str: The extracted text from the PDF file if successful.
            None: If an error occurs during the extraction process.
        Raises:
            Exception: Logs an error message if the file cannot be opened or processed.
        """
        text = ""

        try:
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
                return text
        except Exception as e:
            print(f'Error  opening the file{e}')
            return None
    

    def createVectorEmbeddings(self, text):
        """
        Creates vector embeddings for the given text using FAISS and a text splitter.
        This function splits the input text into manageable chunks using a 
        RecursiveCharacterTextSplitter, then generates vector embeddings for 
        these chunks using the FAISS library.
        Args:
            text (str): The input text to be processed into vector embeddings.
        Returns:
            FAISS: A FAISS vector store containing the embeddings of the text chunks.
            None: Returns None if an exception occurs during the process.
        Raises:
            Exception: Logs and handles any exceptions that occur during the 
            creation of the vector store.
        """
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
            chunks = text_splitter.split_text(text=text)

            vectorStore = FAISS.from_texts(
                texts=chunks,
                embedding=self.embeddings
            )

            return vectorStore
        except Exception as e:
            print(f"Error Creating a vector Store: {e}")
            return None

    def getConversationChainTwo(self,vectorStore):
        """
        Creates a conversational chain using a vector store and a language model.
        Args:
            vectorStore: An object that provides a retriever interface for searching 
                         relevant documents or context based on input queries.
        Returns:
            A chain object that combines a retrieval  and a question-answering 
            chain for conversational purposes. If an error occurs during creation, 
            returns None.
        Raises:
            Exception: Logs and handles any exceptions that occur during the chain creation process.
        """
        try:
            retriever = vectorStore.as_retriever(search_kwargs={"k": 3})
            llm = self.llm
            system_prompt = (
            "Use the given context to answer the question. "
            "If you don't know the answer, say you don't know. "
            "Use three sentence maximum and keep the answer concise. "
            "Context: {context}"
            )
            prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
            )
            question_answer_chain = create_stuff_documents_chain(llm, prompt)
            chain = create_retrieval_chain(retriever,question_answer_chain)

            return chain
        except Exception as e:
            print(f"Error Creating the chain: {e}")
            return None
        

    
    def handle_userInput(self,conversatioChain,question):
        """
        Handles user input by starting a conversational chain to process a question and return an answer.
        Args:
            conversatioChain (object): The conversational chain object used to process the input question.
            question (str): The user's question to be processed.
        Returns:
            dict: A dictionary containing the answer to the question. If an error occurs, the dictionary
                  contains an error message under the "answer" key.
        Raises:
            Exception: Logs and returns an error message if the conversational chain fails to process the input.
        """
        try:
            qa_chain = conversatioChain

            result = qa_chain.invoke({"input":question})
            # raw_answer = result["answer"]
            # cleaned_answer = re.sub(r"<think>.*?</think>", "", raw_answer, flags=re.DOTALL).strip()
            """""
            Cleaned_answer to get rid of the "thinking response", when using a reasoning model like
            Deepseek r-1
            """


            return {
                "answer": result["answer"]
            }
        except Exception as e:
            print(f'Error answering the question:{e}')
            return {"answer":f'Error Processing your question:{str(e)}'}
    
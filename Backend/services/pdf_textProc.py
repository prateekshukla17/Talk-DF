import os
import fitz
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

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
    

    def createVectorEmbeddings(self, text):
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

    # def getConversationChain(self,vectorStore):
    #     try:
    #         memory = ConversationBufferMemory(memory_key='chat_history',return_messages=True)
    #         conversation_chain = ConversationalRetrievalChain.from_llm(
    #         llm=self.llm,
    #         retriever=vectorStore.as_retriever(search_kwargs={"k": 3}),
    #         memory=memory
    #     )
    #         return conversation_chain
    #     except Exception as e:
    #         print(f'Error Creating the convo chain :{e}')
    #         return None
    

    def getConversationChainTwo(self,vectorStore):
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
        try:
            qa_chain = conversatioChain

            result = qa_chain.invoke({"input":question})
            # raw_answer = result["answer"]
            # cleaned_answer = re.sub(r"<think>.*?</think>", "", raw_answer, flags=re.DOTALL).strip()



            return {
                "answer": result["answer"]
            }
        except Exception as e:
            print(f'Error answering the question:{e}')
            return {"answer":f'Error Processing your question:{str(e)}'}
    
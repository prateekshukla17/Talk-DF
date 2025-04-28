import os
import fitz
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain_community.vectorstores import FAISS

load_dotenv()
class pdf_processing:
    def __init__(self):
        self.upload_dir = "uploads"
        self.vector_dir = "vectorstore"

        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.vector_dir, exist_ok=True)

        self.embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-xl")
        self.llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})


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
        
    # def get_conversation_chain(self, vectorstore):
    #     llm = self.llm
    #     memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    #     conversation_chain = ConversationalRetrievalChain(
    #         llm=llm,
    #         retriever=vectorstore.as_retriever(search_kwargs={"k":3}),
    #         memory=memory,
    #         return_source_documents=True
    #     )
    #     return conversation_chain
    # def get_retrieval_chain(self, vectorstore):
    #     print('now in the get retrieval chain')
    #     llm = self.llm
    #     retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    #     prompt = PromptTemplate.from_template(
    #         "Answer the question based on the context provided. \n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
    #     )
    #     combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    #     retrieval_chain = create_retrieval_chain(
    #         retriever=retriever,
    #         combine_docs_chain=combine_docs_chain,
    #     )
    #     print('retrieval chain created')

    #     return retrieval_chain

    # def handle_question(self, vectorstore, question):
    #     try:
    #         retrieval_chain = self.get_retrieval_chain(vectorstore)
    #         result = retrieval_chain.invoke({"question": question})
            
    #         return {
    #             "answer": result["answer"],
    #             "sources": [doc.page_content[:200] + "..." for doc in result["source_documents"]]
    #         }
    #     except Exception as e:
    #         print(f'Error handling the question: {e}')
    #         return None

        
    # def answer_question(self,vectorstore,question):
    #     try:
    #         retriever = vectorstore.as_retriever(search_kwargs={"k":3})

    #         qa_chain = retrieval_qa.from_chain_type(
    #             llm = self.llm,
    #             chain_type = 'stuff',
    #             retriever = retriever,
    #             return_source_documents = True
    #         )

    #         result = qa_chain({"query":question})
            
    #         return {
    #             "answer": result["result"],
    #             "sources": [doc.page_content[:200] + "..." for doc in result["source_documents"]]
    #         }
    #     except Exception as e:
    #         print(f'Error answering the question: {e}')
    #         return None
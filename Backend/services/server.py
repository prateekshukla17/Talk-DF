from fastapi import FastAPI,File,UploadFile,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from pdf_textProc import pdf_processing #importing the pdf_processing class
app = FastAPI()


# # Enable CORS to allow requests from all origins (for frontend-backend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any domain
    allow_credentials=True,
    allow_methods=["*"], # Allow all HTTP methods
    allow_headers=["*"], # Allow all headers
)

pdf_handler = pdf_processing()   #Instance from the pdf_processing class 
vector_store = None
conversation_chain = None
UPLOAD_DIR = pdf_handler.upload_dir


@app.post("/process")
async def process_pdf(file:UploadFile=File(...)):
    #Global variables for sharing vector store and convo chain acrross multiple endpoints
    global vector_store, conversation_chain

    try:
        # Save uploaded PDF to server
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path,"wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
        
        # Extract text from the uploaded PDF
        text = pdf_handler.extract_text(file_path)
        if not text:
            raise HTTPException(status_code=400, detail="Failed to extract text from PDF.")
        
         # Creating vector embeddings from the extracted text
        vector_store = pdf_handler.createVectorEmbeddings(text)
        if not vector_store:
            raise HTTPException(status_code=500, detail="Failed to create vector embeddings.")
        else:
            print('Vecstore Created sucessfully') #Just for debugging 

        # Starting the conversation chain using the vector store
        conversation_chain = pdf_handler.getConversationChainTwo(vector_store)
        if not conversation_chain:
            raise HTTPException(status_code=500, detail="Failed to the convo chain")
        else:
            print('ConvoChain Created') #Just for debugging

          # Return success response
        return {"message": "ConvoChain and vector store created successfully."}
    except Exception as e:
        # Catch all server-side errors
        raise HTTPException(status_code=500, detail=str(e))

# Request model for receiving user's question
class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(payload: QuestionRequest):
    global conversation_chain

    # Check if conversation chain has been intialised
    if not conversation_chain:
        raise HTTPException(status_code=400,detail="No Chains available")
    
    try:
        # Processing the request and generating the response
        response = pdf_handler.handle_userInput(conversation_chain,payload.question)
        if not response:
            raise HTTPException(status_code=500,details='Failed with response')
        else:
            # Return the generated answer
            print(response['answer']) #Just for Debugging
        answer = response['answer']
        return {"answeris":answer}
    except Exception as e:
         # Handle any unexpected errors
        raise HTTPException(status_code=500,detail=str(e))

from fastapi import FastAPI, Request,File,UploadFile,HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from pdf_textProc import pdf_processing
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pdf_handler = pdf_processing()
vector_store = None
conversation_chain = None
UPLOAD_DIR = pdf_handler.upload_dir


@app.post("/process")
async def process_pdf(file:UploadFile=File(...)):
    global vector_store, conversation_chain

    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path,"wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
        
        text = pdf_handler.extract_text(file_path)
        if not text:
            raise HTTPException(status_code=400, detail="Failed to extract text from PDF.")
        vector_store = pdf_handler.createVectorEmbeddings(text)

        if not vector_store:
            raise HTTPException(status_code=500, detail="Failed to create vector embeddings.")
        else:
            print('Vecstore Created sucessfully')

        conversation_chain = pdf_handler.getConversationChainTwo(vector_store)
        if not conversation_chain:
            raise HTTPException(status_code=500, detail="Failed to the convo chain")
        else:
            print('ConvoChain Created')
        
        return {"message": "ConvoChain and vector store created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(payload: QuestionRequest):
    global conversation_chain

    if not conversation_chain:
        raise HTTPException(status_code=400,detail="No Chains available")
    
    try:
        response = pdf_handler.handle_userInput(conversation_chain,payload.question)
        if not response:
            raise HTTPException(status_code=500,details='Failed with response')
        else:
            print(response['answer'])
        answer = response['answer']
        return {"answeris":answer}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

from pdf_textProc import pdf_processing
from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":
    pdf_bot = pdf_processing()


    pdf_path = input("Enter the path to your PDF file: ").strip()


    text = pdf_bot.extract_text(pdf_path)
    print(text)
    if not text:
        print("Failed to extract text from PDF.")
        exit()
    

    vectorstore = pdf_bot.createVectorEmbeddings(text)
    print('vectorStore Created')
    if not vectorstore:
        print("Failed to create vectorstore.")
        exit()

    
    convoChain = pdf_bot.getConversationChainTwo(vectorstore)
    if not convoChain:
        print('Failed To Create the ConvoChain')
        exit()
    else:
        print('Sucessfully created convoChain')



    print("\n PDF processed! ask questions about it.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        response = pdf_bot.handle_userInput(convoChain, question)
        if response:
            print(f"\nBot: {response['answer']}\n")
        else:
            print("Something went wrong when answering. Try again!")

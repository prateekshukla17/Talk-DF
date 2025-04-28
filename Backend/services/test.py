from pdf_textProc import pdf_processing
from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":
    pdf_bot = pdf_processing()


    pdf_path = input("Enter the path to your PDF file: ").strip()


    text = pdf_bot.extract_text(pdf_path)
    if not text:
        print("Failed to extract text from PDF.")
        exit()

    # Step 3: Create vector store
    document_id = "001"  # You can use timestamp or unique IDs here too
    vectorstore = pdf_bot.createVectorEmbeddings(text)
    if not vectorstore:
        print("Failed to create vectorstore.")
        exit()


    # Step 5: Start chatting with the PDF
    print("\n✅ PDF processed! You can now ask questions about it.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        response = pdf_bot.handle_question(vectorstore, question)
        if response:
            print(f"\nBot: {response['answer']}\n")
            print(f"Sources:")
            for idx, source in enumerate(response['sources'], 1):
                print(f"  [{idx}] {source}")
            print("\n" + "-"*50 + "\n")
        else:
            print("Something went wrong when answering. Try again!")

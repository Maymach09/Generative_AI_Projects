from langchain_community.llms import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA

def read_pdf(pdf_url):
    try:
        # Read PDF using PyPDF2
        loader = PyPDFLoader(file_path=pdf_url)
        pages = loader.load_and_split()
        print("Pages read successfully:", pages)  # Add this line for debugging
        return pages
    except Exception as e:
        print("Error reading PDF:", e)  # Add this line for debugging
        return {"error": f"Error reading PDF: {e}"}


def split_pages_into_chunks(pages):
    # Split the text using Character Text Split such that it should not increse token size
    doc_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap  = 100,
        length_function = len,
    )
    chunks = doc_splitter.split_documents(pages)

    return chunks

#Function to define vectordb
def create_vector_db(document_chunks, embeddings):
    vectordb = Chroma.from_documents(
        documents=document_chunks,
        embedding=embeddings,
    )
    return vectordb

def create_retreival_qa(llm, retriever):
    qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    output_key='Answer'
    )
    return qa_chain

def chatbot(pdf_url, input):
    try:
        pages = read_pdf(pdf_url)
    except Exception as e:
        return {"error": f"Error reading PDF: {e}"}
    # Call the function to split document into pages
    document_chunks = split_pages_into_chunks(pages)

    # Initialize OpenAI embedding
    embeddings = OpenAIEmbeddings()

    # Call the function to Create vectordb
    vectordb = create_vector_db(document_chunks, embeddings)

    # Retrieve relevant chunks and store them in a variable
    retriever = vectordb.as_retriever()

    llm = OpenAI(temperature=0.2, max_tokens=1000)

    #  # Combine the prompt, document URL, and question
    # full_prompt = f"{prompt}\nDocument: {pdf_url}\nQuestion: {input}"

    chain = create_retreival_qa(llm,retriever)
    output = chain(input)

    return output["Answer"]
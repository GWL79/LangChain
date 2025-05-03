import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
load_dotenv()
if __name__ == "__main__":
    print("Ingesting")
    loader = TextLoader(r"C:\Users\wlgan\LangChain\intro_to_vector_dbs\mediumblog1.txt", encoding="UTF-8")
    document = loader.load() #load documents
    #print(document)

    print("Splitting")
    text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 0)
    texts = text_splitter.split_documents(documents=document) #split document into chunks
    embeddings = OpenAIEmbeddings(openai_api_key = os.environ["OPENAI_API_KEY"]) #embedding model

    print("Ingesting")
    PineconeVectorStore.from_documents(texts, embeddings, index_name = os.environ["INDEX_NAME"])
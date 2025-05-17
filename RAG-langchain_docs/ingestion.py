from dotenv import load_dotenv
from langchain_community.document_loaders import ReadTheDocsLoader #good for documentation
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import os
load_dotenv()

def ingest_docs():
    embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")
    loader = ReadTheDocsLoader(r"C:\Users\wlgan\LangChain\RAG-langchain_docs\latest", encoding="UTF-8")
    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 300,chunk_overlap = 10)
    documents = text_splitter.split_documents(documents= raw_documents)
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")
        doc.metadata.update({"source":new_url})
    print(f"Going to add {len(documents)} to Pinecone")
    print(len(documents)/2)
    res = [] 
    for i in range(0, len(documents), 50):  # Slice list in steps of n
        print(i)
        PineconeVectorStore.from_documents(documents=documents[i:1+50], embedding=embeddings, index_name = os.environ["INDEX_NAME"] )#initialize vector store with documents and embeddings
    #PineconeVectorStore.from_documents(documents=documents[int((len(documents)/2)):], embedding=embeddings, index_name = os.environ["INDEX_NAME"] )#initialize vector store with documents and embeddings


if __name__ == "__main__":
    ingest_docs()
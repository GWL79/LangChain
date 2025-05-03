from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


from dotenv import load_dotenv
import os

load_dotenv()


if __name__ == "__main__":
    print(os.environ["INDEX_NAME"])
    print("Retrieving")
    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI()
    query = "What is Pinecone in machine learning"

    vector_store = PineconeVectorStore(index_name = os.environ["INDEX_NAME"], embedding=embeddings)

    retrieval_qa_chat = hub.pull("langchain-ai/retrieval-qa-chat")
    """
        Answer any use questions based solely on the context below:

        <context>
        {context}
        </context>
    """
    combine_docs_chain = create_stuff_documents_chain(llm=llm, prompt=retrieval_qa_chat)
    retrieval_chain = create_retrieval_chain(retriever=vector_store.as_retriever(), combine_docs_chain= combine_docs_chain)
    result = retrieval_chain.invoke(input = {"input": query})
    print(result["answer"])
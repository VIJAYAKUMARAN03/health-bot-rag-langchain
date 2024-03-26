from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import Html2TextTransformer
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import nest_asyncio

from googlesearch import search

# from model import get_response

nest_asyncio.apply()

def searchLinks(query):
    # Specify the number of results you want (maximum 10 for free usage)
    num_results = 4

    # Perform the Google search and fetch the links
    links = list(search(query, num_results=num_results))    

    # Print the links
    for link in links:
        print(link)
    
    return links

def faiss(query):

    articles = searchLinks(query)

    # Scrapes the blogs above
    loader = AsyncChromiumLoader(articles)
    docs = loader.load()

    # Converts HTML to plain text
    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(docs)

    # Chunk text
    text_splitter = CharacterTextSplitter(chunk_size=200,
                                        chunk_overlap=10)
    chunked_documents = text_splitter.split_documents(docs_transformed)

    # Load chunked documents into the FAISS index
    db = FAISS.from_documents(chunked_documents,
                            HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2'))


    # Connect query to FAISS index using a retriever
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={'k': 10}
    )

    return db

def get_response(query):
    db = faiss(query)
    docs = db.similarity_search(query)
    txt = ""
    for doc in docs:
        txt += doc.page_content
        print(doc.page_content)
        print("-------------")
    txt = txt.replace('**','\n')
    txt = txt.replace('*',' ')
    txt = txt.replace('#','')
    txt = txt.replace('\\','')
    txt = txt.replace('?',' ')
    return txt

# def search(query):
#     # embeddings = get_embeddings(query)
#     db = faiss(query)
#     retriever = db.as_retriever()
#     return get_response(retriever,query)

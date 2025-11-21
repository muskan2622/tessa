"""
Vector Store for RAG
Manages vector embeddings and semantic search
"""
from typing import List, Dict, Any, Optional
import os
from langchain.vectorstores import Pinecone, Weaviate, Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    """Vector store for document embeddings and retrieval"""
    
    def __init__(self, store_type: str = "pinecone"):
        """
        Initialize vector store
        
        Args:
            store_type: Type of vector store ("pinecone", "weaviate", "chroma")
        """
        self.store_type = store_type
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.vector_store = None
        self._initialize_store()
    
    def _initialize_store(self):
        """Initialize the vector store based on type"""
        if self.store_type == "pinecone":
            import pinecone
            pinecone.init(
                api_key=os.getenv("PINECONE_API_KEY"),
                environment=os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
            )
            index_name = os.getenv("PINECONE_INDEX_NAME", "tessa-documents")
            self.vector_store = Pinecone.from_existing_index(
                index_name=index_name,
                embedding=self.embeddings
            )
        elif self.store_type == "weaviate":
            # TODO: Initialize Weaviate client
            pass
        elif self.store_type == "chroma":
            persist_directory = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
            self.vector_store = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings
            )
        else:
            raise ValueError(f"Unknown vector store type: {self.store_type}")
    
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]] = None):
        """
        Add documents to vector store
        
        Args:
            documents: List of document texts
            metadatas: List of metadata dictionaries
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        texts = text_splitter.split_text("\n\n".join(documents))
        
        # Add to vector store
        if metadatas:
            # Match metadata to chunks (simplified - in production, handle chunking properly)
            chunk_metadatas = []
            for i, text in enumerate(texts):
                doc_idx = i // (len(texts) // len(metadatas))
                chunk_metadatas.append(metadatas[min(doc_idx, len(metadatas) - 1)])
            self.vector_store.add_texts(texts, metadatas=chunk_metadatas)
        else:
            self.vector_store.add_texts(texts)
    
    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform similarity search
        
        Args:
            query: Search query
            k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of relevant documents with metadata
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        
        if filter:
            docs = self.vector_store.similarity_search(
                query,
                k=k,
                filter=filter
            )
        else:
            docs = self.vector_store.similarity_search(query, k=k)
        
        results = []
        for doc in docs:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
        
        return results
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 5
    ) -> List[tuple]:
        """
        Perform similarity search with scores
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of (document, score) tuples
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        
        return self.vector_store.similarity_search_with_score(query, k=k)


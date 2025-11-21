"""
RAG Pipeline
Retrieval Augmented Generation for document Q&A
"""
from typing import List, Dict, Any, Optional
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
import logging

from models.rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


class RAGPipeline:
    """RAG pipeline for document question answering"""
    
    def __init__(self, vector_store: VectorStore):
        """
        Initialize RAG pipeline
        
        Args:
            vector_store: Initialized vector store instance
        """
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            model=os.getenv("LLM_MODEL", "gpt-4"),
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.qa_chain = self._create_qa_chain()
    
    def _create_qa_chain(self) -> RetrievalQA:
        """Create QA chain with custom prompt"""
        prompt_template = """Use the following pieces of context to answer the question about real estate title documents.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
        Context: {context}
        
        Question: {question}
        
        Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        chain_type_kwargs = {"prompt": PROMPT}
        
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.vector_store.as_retriever(),
            chain_type_kwargs=chain_type_kwargs,
            return_source_documents=True
        )
    
    async def answer_question(
        self,
        question: str,
        search_kwargs: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Answer a question using RAG
        
        Args:
            question: User question
            search_kwargs: Additional search parameters
            
        Returns:
            Dictionary with answer and source documents
        """
        try:
            if search_kwargs:
                # Update retriever with search kwargs
                retriever = self.vector_store.vector_store.as_retriever(
                    search_kwargs=search_kwargs
                )
                self.qa_chain.retriever = retriever
            
            result = await self.qa_chain.ainvoke({"query": question})
            
            return {
                "answer": result["result"],
                "source_documents": [
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata
                    }
                    for doc in result.get("source_documents", [])
                ]
            }
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {e}")
            return {
                "answer": "I'm sorry, I encountered an error processing your question.",
                "source_documents": []
            }
    
    def add_documents_for_qa(self, documents: List[str], metadatas: List[Dict[str, Any]] = None):
        """Add documents to vector store for Q&A"""
        self.vector_store.add_documents(documents, metadatas)


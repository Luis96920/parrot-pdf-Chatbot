from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import PromptTemplate
import os

# Global variable to store the model instance
llm_model = None

def get_llm_model():
    global llm_model
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    model_path = '#YOUR llm path'
    if llm_model is None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model path does not exist: {model_path}")
        print("Loading LLM model...")
        llm_model = LlamaCpp(
            model_path=model_path,
            n_threads=12,  # Keep this if it matches your CPU's thread count
            n_gpu_layers=-1,  # This tells it to use as many GPU layers as possible
            n_batch=512,  # Increased for potentially faster processing, adjust if you hit memory limits
            n_ctx=2048,  # Reduced context size for faster processing
            temperature=0,  # Keep deterministic for speed
            verbose=False,  # Turn off verbose mode for slight speed improvement
            callback_manager=callback_manager,
            top_p=1.0,  # Disable top_p sampling for speed
            top_k=1,  # Effectively disable top_k sampling for speed
            use_mmap=True,  
            use_mlock=True,
            rope_scaling_type=1,  # Use "dynamic" scaling type
            rope_freq_base=10000,  # Default value, but explicitly set for potential fine-tuning
            rope_freq_scale=1.0,  # Default value, can be adjusted for different behavior
            f16_kv=True  # Use half-precision for key/value cache, saves memory and might be faster
        )
    return llm_model

def Agent(question, chat_history):
    try:
        # Load and process documents
        loader = DirectoryLoader("media", glob="*.pdf", loader_cls=PyPDFLoader)
        data = loader.load()
        
        text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200)
        text_chunks = text_splitter.split_documents(data)
        
        # Create vector store
        embeddings_model = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')
        vectordb = Chroma.from_documents(text_chunks, embedding=embeddings_model, persist_directory="./VectorDB")
        retriever = vectordb.as_retriever(search_type="mmr",search_kwargs={'k': 5, 'fetch_k': 50})
        llm = get_llm_model()
        
        system_template = """
        Answer the question based solely on the context provided below. 
        If the question cannot be answered using the given information, respond with "I don't know."
        
        Given the following conversation history and a follow-up question:
        1. Review the conversation history for context.
        2. Analyze the follow-up question in relation to the conversation.
        3. Rephrase the follow-up question as a standalone question that captures the full context.
        4. Ensure the rephrased question is clear, specific, and can be understood without prior context.
        5. In your answer, include both the original follow-up question and your rephrased version.

        Format your response as follows:
        Original follow-up question: [Insert original question here]
        Rephrased standalone question: [Insert your rephrased question here]
        Answer: [Provide your answer here, or "I don't know" if the information is not in the context]

        Remember:
        - Use only the information provided in the context.
        - Do not add any assumptions or external knowledge.
        - If the question cannot be answered from the context, state "I don't know."
        - Maintain the original intent and key elements of the follow-up question in your rephrasing.
        Context: '{context}'
        Chat History:'{chat_history}'
        Question:'{question}'  
        """
        PROMPT = ChatPromptTemplate.from_messages(
            messages=[
                SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=["context", "chat_history", "question"],template=system_template)),
                HumanMessagePromptTemplate.from_template("{question}")
                ])
        
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            verbose=True,
            retriever=retriever,
            return_source_documents=True,
            get_chat_history=lambda h: h,
            combine_docs_chain_kwargs={"prompt": PROMPT},
        )
        
        REDIS_URL = "redis://172.22.217.232:6379"
        session_id = "12"
        chat_history_redis = RunnableWithMessageHistory(
            chain,
            lambda session_id: RedisChatMessageHistory(session_id, url=REDIS_URL),
            input_messages_key="question",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
        result = chat_history_redis.invoke({"question": question},{"configurable": {"session_id": session_id}})
        chat_history = result['answer']
        return (result['answer'],chat_history)    
    except Exception as e:
        return f"Error: {e}"
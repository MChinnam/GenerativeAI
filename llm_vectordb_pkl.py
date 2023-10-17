from langchain import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma,FAISS
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAIChat
import pickle

key=''

llm = OpenAI(openai_api_key=key, temperature=0.5)

# Load text from a file
# with open("/Users/fission/Documents/LLM/resume4.txt", 'r') as f:
#     text = f.read()

# Create a TextLoader instance and load the text
docs = TextLoader("/Users/fission/Documents/LLM/exl_jd.txt")
documents=docs.load()


# # Create an instance of OpenAIEmbeddings
embedding = OpenAIEmbeddings(openai_api_key=key)

# # Split the text into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# docs = text_splitter.split_documents(docs)

# # Load the documents into Chroma


import os
if os.path.exists("exl_jd.pkl"):
    with open("exl_jd.pkl", 'rb') as f:
        vectordb = pickle.load(f) 
        print("Reading from disk")
        
else:
    #vectordb = Chroma.from_documents(texts,embedding=embedding)    
    vectordb=FAISS.from_documents(texts,embedding=embedding)    
    with open("exl_jd.pkl",'wb') as f:
        pickle.dump(vectordb,f)
        print("computing embedinegs")
    
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = text_splitter.split_documents(documents)

# qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=vectordb.as_retriever(),)
# query = "what is the notice period company looking?"
# print(qa.run(query))

#####
template = """The provided context is a company Job description, use the given context generate the answer if dont know the answer, simply say Sorry I'm not aware of it. 
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectordb.as_retriever(),
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)
#result = qa_chain({"query": "what is the company name"})
#result["result"]
#print(result["result"])


from langchain.prompts import PromptTemplate

template1 = """Giving the company job description as context, from the given jobdescription extract the 
information Job title, Company name, job location, 
education qualification, mandatory skills, experience required, salary offering  and the result should be in JSON format. 
If you don't know the answer, don't try to answer; just give it as N/A.
jobescription: {jondescription}

"""

template2="""
               I want you to act as an recruitment bot,for an recruitment company.
                use the given jobdescription as a context and generate the question and answers from it. Answers should be in json format. 
                jobescription: {jondescription}
        """


campaign_prompt = PromptTemplate(
    input_variables=["jondescription"],
    template=template1
)

# Initialize the language model and chain
campaign_chain = LLMChain(llm=llm, prompt=campaign_prompt)

# Run the marketing campaign idea generation chain
op=campaign_chain.run({'jondescription':documents[0].page_content})

print(op)

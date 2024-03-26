
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM


model_name='mistralai/Mistral-7B-Instruct-v0.1'
hf_token = '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'


model_config = transformers.AutoConfig.from_pretrained(
   model_name, token=hf_token, trust_remote_code=True
)


tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, token=hf_token)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"


#################################################################
# Load pre-trained config
#################################################################
model = AutoModelForCausalLM.from_pretrained(
   model_name,
   # quantization_config=bnb_config,
)

# Save the model
model.save_pretrained("./mistral_model")
model.save_model("./mistral_model1")

# Optionally, you can save the tokenizer as well
tokenizer.save_pretrained("./tokenizer_model")
tokenizer.save_model("./tokenizer_model1")

from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from langchain.chains import LLMChain

text_generation_pipeline = transformers.pipeline(
    model=model,
    tokenizer=tokenizer,
    task="text-generation",
    temperature=0.0,
    repetition_penalty=1.1,
    return_full_text=True,
    max_new_tokens=300,
)

prompt_template = """
### [INST]
Instruction: Answer the question based on the below given context
Here is context to help:

{context}

### QUESTION:
{question}

[/INST]
 """

mistral_llm = HuggingFacePipeline(pipeline=text_generation_pipeline)

# Create prompt from prompt template
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)

# Create llm chain
llm_chain = LLMChain(llm=mistral_llm, prompt=prompt)


def get_response(retriever,query):
    rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
        | llm_chain
    )
    ans = rag_chain.invoke(query)['text']
    txt = ans[(txt.index('[/INST]') + 9):].replace('\n','')#.replace('\','')0
    return txt
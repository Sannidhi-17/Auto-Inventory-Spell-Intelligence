import openai
import os
from dotenv import load_dotenv
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import re
load_dotenv()

# -------------------------------
# Method - 1: OPEN AI MODEL
# -------------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

def genai_correct(input_text):
    prompt = f"""
    You are an automotive parts expert.
    You need to check the spell and correct the spell if its
    wrong according to the automotive parts.
    User typed: "{input_text}"

    Please return correct word. 
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [{"role": "user", "content": prompt}],
        temperature=0
    )
    corrected_name = response.choices[0].message.content

    return corrected_name.strip()


# -------------------------------
# Method - 2: Transformer based model
# -------------------------------
spell_corrector = pipeline("text-generation", model="google/flan-t5-small")

def transformer_based_check(input_text):
    prompt = f"correct spelling: {input_text}"
    result = spell_corrector(prompt)
    return result[0]['generated_text']

# -------------------------------
# Method - 3: LLAMA Model
# -------------------------------
model_name = "meta-llama/Llama-2-7b-chat-hf"

# Load these ONCE at the top of your script
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto", 
    torch_dtype=torch.float16 
)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def llama_correct(input_text):
    prompt = f"""Target: {input_text}\nCorrect the spelling using Indian/British English. One word only.

            Answer:"""
    output = generator(prompt, max_new_tokens=10) 
    text =  output[0]['generated_text']
    match = re.search(r"Answer:\s*(\w+)", text)
    if match:
        print(match.group(1))
    print(f"Input: {input_text} -> Output: {match.group(1)}")
    return match.group(1)
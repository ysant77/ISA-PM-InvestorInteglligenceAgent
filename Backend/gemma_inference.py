import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, AutoConfig
from constants import modelName
from utils import extract_model_responses
from neuro_fuzzy_inference import get_prediction_label

bnbConfig = BitsAndBytesConfig(
    load_in_4bit = True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

model = AutoModelForCausalLM.from_pretrained(
    modelName,
    device_map = {"": 0},
    quantization_config=bnbConfig
)

tokenizer = AutoTokenizer.from_pretrained(modelName)

system_prompt = """
As a highly intelligent assistant and successor of google gemma model, your primary goal is to provide accurate, relevant, and context-aware responses to
user queries based on the provided information. Ensure your answers are factual, free from bias, and avoid promoting violence, hate speech, or any form
of discrimination. Focus on assisting the user effectively and safely. Also do not include user's query in response again
"""

def get_completion(query: str, model, tokenizer) -> str:
  device = "cuda:0"

  prompt_template = """
  <start_of_turn>user
  {system_prompt}
  {query}
  <end_of_turn>\n<start_of_turn>model


  """
  prompt = prompt_template.format(system_prompt=system_prompt, query=query)

  encodeds = tokenizer(prompt, return_tensors="pt", add_special_tokens=True)

  model_inputs = encodeds.to(device)


  generated_ids = model.generate(**model_inputs, early_stopping=True, max_new_tokens=400, do_sample=False, pad_token_id=tokenizer.eos_token_id)
  # decoded = tokenizer.batch_decode(generated_ids)
  decoded = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
  model_response = decoded.split("<start_of_turn>model\n\n")[-1].strip()

  return model_response

user_input = "What are the risks of investing in Apple's stock?"#str(input('Enter your query '))
model_output = get_completion(user_input, model, tokenizer)

responses = extract_model_responses(model_output)
output = [res.strip() for res in responses if res.startswith("model")]
output = [ele.replace("model", "").strip() for ele in output]

response = output[0]
query_args = response.strip().split(':')

if query_args[0] == 'stock_risk':
  label = get_prediction_label(query_args[1].strip())
  print(label)


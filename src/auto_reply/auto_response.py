from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

#User input just a string
def generate_response(user_input):
    inputs = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    response = model.generate(inputs, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    #Returns the chat bots response without user input
    return tokenizer.decode(response[0], skip_special_tokens=True).replace(user_input, "")

#Example, if you want specific answers you need to ask specific questions
"""user_input = "What is your favorite food and why do you like that?"
output = generate_response(user_input)
print(output)"""
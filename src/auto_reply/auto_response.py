from transformers import AutoModelForCausalLM, AutoTokenizer
import re

class Auto_Response:
    '''
    Class to generate a response to a given text
    '''
    def __init__(self) -> None:
        '''
        Initialize class properties
        '''
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

    def generate_response(self, user_input):
        inputs = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors='pt')
        response = self.model.generate(inputs, max_length=1000, pad_token_id=self.tokenizer.eos_token_id)

        response = self.tokenizer.decode(response[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
        return response.replace(user_input, "", 1)
    
    def generate_responses(self, user_input):
        chat_prompts = ['Provide a positive answer to the query: ', 'Provide a negative answer to the query: ', 'Provide an ambiguous answer to the query: ']
        answers = []
        for prompt in chat_prompts:
            answers.append(self.generate_response(prompt + user_input))
        return answers
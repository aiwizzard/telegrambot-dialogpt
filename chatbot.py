from transformers import AutoModelWithLMHead, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelWithLMHead.from_pretrained("microsoft/DialoGPT-medium")

class Chatbot():
    def __init__(self) -> None:
        self.user_history_dict = dict()

    def add_to_history(self, msg, response, user_id):
        if user_id not in self.user_history_dict:
            self.user_history_dict[user_id] = []
        self.user_history_dict[user_id].append(msg)
        self.user_history_dict[user_id].append(response)
        
    def create_response(self, text, history=[]):
        chat_history_ids = None
        for _text in history:
            input_ids = tokenizer.encode(_text + tokenizer.eos_token, return_tensors='pt')
            if chat_history_ids is None:
                chat_history_ids = input_ids
            else:
                chat_history_ids = torch.cat([chat_history_ids, input_ids], dim=-1)

        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if len(history) > 0 else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

        # pretty print last ouput tokens from bot
        return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    def chat(self, user_id, msg=''):
        if user_id not in self.user_history_dict:
            self.user_history_dict[user_id] = []
        response = self.create_response(msg, self.user_history_dict[user_id])
        self.add_to_history(msg, response, user_id)

        return response

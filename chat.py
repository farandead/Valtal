import random
import json
import torch
from model import Neuralnet
from nltk_utils import bag_of_words,tokenize,stem
# from spellchecker import Spellchecker

# spell = Spellchecker()

# def correct_spelling(sentence):
#     words = sentence.split()
#     corrected_words = [spell.correction(word) for word in words]
#     return ' '.join(corrected_words)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  

with open('intents.json', 'r') as f:
    intents = json.load(f)

FILE = 'data.ph'
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size =data["hidden_size"]
output_size =data["output_size"]
    
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]
    
model = Neuralnet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()
    
bot_name = "PAWZZZ"

def get_response(msg):    
    sentence_to_save = msg    
    sentence = tokenize(msg)
    

    x = bag_of_words(sentence,all_words)
    x = x.reshape(1,x.shape[0])
    x = torch.from_numpy(x).to(device)

            
    output = model(x)
    _, predicted = torch.max(output,dim=1)
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0] [predicted.item()]
    if prob.item() > 0.90:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent["responses"])
    else:
        return "I cannot understand your question :( Can you try asking another question ?"
          
                
            

    

                
    

    
            
    
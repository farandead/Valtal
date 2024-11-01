import json
from nltk_utils import tokenize,stem,bag_of_words
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset,DataLoader
from model import Neuralnet

class ChatDataset(Dataset):
    def __init__(self, x_train, y_train):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train
            
    def __getitem__(self,index):
        return self.x_data[index] , self.y_data[index]
        
    def __len__(self):
        return self.n_samples
        
        
    
def main():
    with open('intents.json', 'r') as f:
        intents = json.load(f)
        
        
    all_words = []
    tags = []
    xy = []

    for intent in intents['intents']:
        tag = intent['tag']
        tags.append(tag)
        for pattern in intent['patterns']:
            w = tokenize(pattern)
            # cause all_words is an array and w is gonna be an array too which it will make it an array of arrays if we use append instead of extend
            all_words.extend(w)
            xy.append((w,tag))
            
    ignore_words = ['?','!',',','.']
    all_words = [stem(w) for w in all_words if w not in ignore_words] 
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))
    # print(tags)
            
    x_train = []
    y_train = []

    for (pattern_sentence,tag ) in xy:
        bag = bag_of_words(pattern_sentence,all_words)
        x_train.append(bag)
        
        label = tags.index(tag)
        y_train.append(label)  
        
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    # hyperparamters
    batch_size = 8  
    hidden_size = 8
    output_size = len(tags)
    # bag of words length we can either use the len of all words or 
    input_size = len(x_train[0])
    # print(input_size, len(all_words))
    # print(output_size,len(tags))
    learning_rate = 0.001
    num_epochs = 1000





    dataset = ChatDataset(x_train,y_train)
    train_loader = DataLoader(dataset=dataset,batch_size=batch_size, shuffle=True,num_workers=0)


    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  
    model = Neuralnet(input_size, hidden_size, output_size).to(device)

    #loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimzer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        for (words, labels) in train_loader:
            # print(words, labels)  # Add this line
            words = words.to(device)
            labels = labels.to(device).long()

            # Forward pass
            outputs = model(words)
            loss = criterion(outputs, labels)

            # Backward and optimize
            optimzer.zero_grad()
            loss.backward()
            optimzer.step()
        
        if (epoch + 1) % 100 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
                
    print(f'final loss, loss={loss.item():.4f}')
    
    data = {
        "model_state": model.state_dict(),
        "input_size": input_size,
        "output_size": output_size,
        "hidden_size": hidden_size,
        "all_words": all_words,
        "tags": tags
    }
    
    
    FILE = "data.ph"
    torch.save(data,FILE)
    
    print(f'training complete. file saved to {FILE}')
   
if __name__ == '__main__':
    main()
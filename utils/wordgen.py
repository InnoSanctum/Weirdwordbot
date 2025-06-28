import random
import csv

vocab = []

def build_vocab():
    global vocab
    with open('data/vocab.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            vocab.append((row['Word'], row['Description']))
          
def get_fake_word():
    return random.choice(vocab)

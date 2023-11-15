from google_images_search import GoogleImagesSearch
from io import BytesIO
from PIL import Image


import tkinter as tk
import io
import random
import string
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
import requests
from PIL import Image, ImageTk
nltk.download('popular', quiet=True)


with open('chatbotEng.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chatbot")

        self.label = tk.Label(master, text="ROBO: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")
        self.label.pack()

        self.user_input = tk.Entry(master)
        self.user_input.pack()

        self.chat_log = tk.Text(master)
        self.chat_log.pack()

        self.submit_button = tk.Button(master, text="Submit", command=self.submit)
        self.submit_button.pack()

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()

    def submit(self):
        user_response = self.user_input.get()
        self.user_input.delete(0, tk.END)
        self.chat_log.insert(tk.END, "You: " + user_response + "\n")
        user_response=user_response.lower()
        if(user_response!='bye'):
            if(user_response=='thanks' or user_response=='thank you' ):
                self.chat_log.insert(tk.END, "ROBO: You are welcome..\n")
            else:
                if(greeting(user_response)!=None):
                    self.chat_log.insert(tk.END, "ROBO: "+greeting(user_response) + "\n")
                else:
                    self.chat_log.insert(tk.END, "ROBO: " + response(user_response) + "\n")
                    sent_tokens.remove(user_response)
                    self.search_image(user_response)
        else:
            self.chat_log.insert(tk.END, "ROBO: Bye! take care..\n")

    def search_image(self, query):
        # Google Image Search API credentials
        gis = GoogleImagesSearch('AIzaSyCo4WDXIcal8uSjVvNHdyDM4unwCwF220E','f4208521453734899')

        # Search for images based on user input
        gis.search({'q': query, 'num': 1})

        # Display the first image to the GUI
        for result in gis.results():
            image_url = result.url
            image_response = requests.get(image_url)
            image_data = image_response.content
            photo = ImageTk.PhotoImage(Image.open(io.BytesIO(image_data)).resize((300, 200), resample=Image.LANCZOS))
            if hasattr(self, 'label'):
                self.label.configure(image=photo)
                self.label.image = photo
            else:
                self.label = tk.Label(image=photo)
                self.label.image = photo
                self.label.pack()

root = tk.Tk()
my_gui = ChatbotGUI(root)
root.mainloop()


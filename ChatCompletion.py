import openai
import json
from PyQt5.QtCore import QThread,pyqtSignal



class chatCompletion(QThread):
    responseChanged = pyqtSignal(str)
    with open("API_key.txt","r") as key:
        API_key = key.read() 

    def __init__(self, context, maxtkns,temp):
        super().__init__()
        self.context = context
        self.tokens = maxtkns
        self.temp = temp
        self._response = None

    def run(self):
        with open("BetsyApp/API_key.txt","r") as key:
            API_key = key.read() 
            print(API_key)
        openai.api_key = API_key
        with open(self.context) as f:
            messages = json.load(f)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=self.temp,
            max_tokens=self.tokens,
            stream = True
            )
        
        for chunk in completion:
            try:
                chunk_message = chunk['choices'][0]['delta']['content']
                print(chunk_message)
            except:
                pass
        self.responseChanged.emit(self._response)


    @property
    def response(self):
        return self._response
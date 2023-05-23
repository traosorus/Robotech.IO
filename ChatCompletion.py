import openai
import json
from PyQt5.QtCore import QThread,pyqtSignal



class chatCompletion(QThread):
    responseChanged = pyqtSignal(str)
    with open("API_key.txt","r") as key:
        API_key = key.read() 
    def __init__(self, context, maxtkns,temp, destination):
        super().__init__()
        self.context = context
        self.tokens = maxtkns
        self.temp = temp
        self.destination = destination
        destination.append("\nBetsy: ")
        self.chunk_message = None
        self.answer = ""
    def run(self):
        with open("API_key.txt","r") as key:
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
                self.chunk_message = chunk['choices'][0]['delta']['content']
                # move the cursor to the end of the text
                cursor = self.destination.textCursor()
                cursor.movePosition(cursor.End)

                # insert the new word
                cursor.insertText(self.chunk_message)
                self.answer = self.answer + str(self.chunk_message)              
            except:
                self.answer = " \n \n ERREUR LORS DE LA COMPLETION ESSAYEZ RENVOYER LE MESSAGE SI LE PROBLÉME PERSISTE VERIFIEZ 'ETAT DE LA CONNECTION ET REDEMARREZ L'APPLICATION "

        self.responseChanged.emit(self.chunk_message)
    @property
    def response(self):
        return self.chunk_message
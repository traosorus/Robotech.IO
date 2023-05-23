import openai  # for OpenAI API calls
import json  # for measuring time duration of API calls
# a ChatCompletion request
#initialisation OpenAI
class chatCompletion :
    def __init__(self, context, maxtkns,temp,destination):
        
        self.context = context
        self.tokens = maxtkns
        self.temp = temp
        destination.append("\nBetsy: ")
        with open("API_key.txt","r") as key:
                API_key = key.read() 
                openai.api_key = API_key
        with open(self.context) as f:
            messages = json.load(f)
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0,
            stream=True  # this time, we set stream=True
        )

        for chunk in response:
            try:
                chunk_message = chunk['choices'][0]['delta']['content']
                # move the cursor to the end of the text
                cursor = destination.textCursor()
                cursor.movePosition(cursor.End)

                # insert the new word
                cursor.insertText(chunk_message)
               
                print(chunk_message)
                
            except:
                pass
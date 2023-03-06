
class Display:
    def __init__(self):
        self.text = "Welcome"
        self.refresh()
    
    def clear(self):
        self.text =""
        self.refresh()

    def append(self, char):
        self.text += char
        self.refresh()
        
    def write(self, text):
        self.text = text
        self.refresh()
    
    def refresh(self):
        print(self.text)
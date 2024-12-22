class AbstractState :
    NAME = ''
    
    def __init__(self, device) :
        self.device = device
        pass
    
    def enter(self) :
        pass
    
    def exit(self) :
        pass
    
    def print(self) :
        print(">>", self.NAME)
    
    def exec(self) :
        pass
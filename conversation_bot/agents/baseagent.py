from abc import ABC , abstractmethod

class baseagent(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def invoke(self , query):


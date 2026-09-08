
class Option:
    def __init__(self, name: str, handler: callable):
      self.name    = name
      self.handler = handler
      
    def execute(self):
        return self.handler()
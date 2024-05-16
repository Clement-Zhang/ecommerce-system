class Account():
    def __init__(self, id: int, username: str,):
        self.id = id
        self.username = username
    
    def __str__(self):
        return f"Account: id {self.id}, username ({self.username})"
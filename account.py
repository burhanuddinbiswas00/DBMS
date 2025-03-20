from threading import Lock

class Account:
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance
        self.lock = Lock()

    def __repr__(self):
        return f"Account(id={self.id}, balance={self.balance})"

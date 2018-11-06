class MSGBoard():
    def __init__(self, name):
        self.name = name
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def get_message(self, reverse_index=1):
        self.messages[reverse_index * -1]

    def get_messages(self, count, start_at=None):
        if not start_at:
            return self.messages[count * -1:]
        else:
            return self.messages[start_at:start_at + count]

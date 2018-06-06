
class PassCardIllegalException(Exception):
    def __init__(self):
        self.message = "Passing Cards not in your hand!"

    def __str__(self):
        return self.message


class IllegalMoveException(Exception):
    def __init__(self):
        self.message = "Playing Card not in your hand!"

    def __str__(self):
        return self.message

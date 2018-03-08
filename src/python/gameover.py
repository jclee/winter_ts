
class EndGameException(Exception):
    pass

class GameOverException(EndGameException):
    pass

class GameWinException(EndGameException):
    pass

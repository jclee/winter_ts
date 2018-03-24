
class EndGameException(Exception):
    pass

class GameLoseException(EndGameException):
    pass

class GameQuitException(EndGameException):
    pass

class GameWinException(EndGameException):
    pass

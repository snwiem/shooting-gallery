import logging

from app.game import Game

logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
    game = Game()
    game.run()
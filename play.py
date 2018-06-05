# -*- coding: utf-8 -*-
from game import Game
from agent import AgentRandom
from agent import MediumAgent

if __name__ == '__main__':
    game = Game(
        [MediumAgent('Iron Man'), AgentRandom('Superman'),
         AgentRandom('Batman'), AgentRandom('Spiderman')]
    )

    game.set_game()
    scores = game.play()

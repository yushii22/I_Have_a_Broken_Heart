# -*- coding: utf-8 -*-
from game import Game
from agent import AgentRandom, AgentMedium, MyAgent

import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    scores = [0] * 4
    for _ in range(1000):
        game = Game(
            [AgentMedium('Iron Man'), AgentRandom('Superman'),
             AgentRandom('Batman'), AgentRandom('Spiderman')]
        )

        game.set_game()
        for i, score in enumerate(game.play()):
            scores[i] += score

    print(scores)

# -*- coding: utf-8 -*-


if __name__ == "__main__":
    Onegame = Game()
    result = Onegame.start()
    print("\n".join(["player %d : %d" %(idx,r) for idx,r in enumerate(result) ]))

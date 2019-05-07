from game import *


def main():
    play_game = Game(rand=random.randint(1, 4))
    play_game.play()


if __name__ == '__main__':
    main()

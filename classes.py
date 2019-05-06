from livewires import games, color
import random

games.init(screen_width=480, screen_height=640, fps=50)


class Car(games.Sprite):
    image = games.load_image('img/car2.png')

    def __init__(self, game, x, y):
        super(Car, self).__init__(image=Car.image,
                                  x=x,
                                  y=y)
        self.game = game
        self.score = games.Text(value=0,
                                size=40,
                                right=games.screen.width - 10,
                                color=color.white,
                                top=5
                                )
        games.screen.add(self.score)

    def update(self):

        if self.left < 0:
            self.left = 0

        if self.right > games.screen.width:
            self.right = games.screen.width

        if self.top < 0:
            self.top = 0

        if self.bottom > games.screen.height:
            self.bottom = games.screen.height

        if games.keyboard.is_pressed(games.K_RIGHT):
            self.x += 3
        if games.keyboard.is_pressed(games.K_LEFT):
            self.x -= 3
        if games.keyboard.is_pressed(games.K_UP):
            self.y -= 2
        if games.keyboard.is_pressed(games.K_DOWN):
            self.y += 2

        self.check_collision()

    def check_collision(self):
        for obstacle in self.overlapping_sprites:
            obstacle.collision()
            self.end_game()

    def end_game(self):
        end_msg = games.Message(value='Вы проиграли!',
                                size=90,
                                color=color.red,
                                x=games.screen.width / 2,
                                y=games.screen.height / 2,
                                lifetime=5 * games.screen.fps,
                                after_death=games.screen.quit
                                )
        games.screen.add(end_msg)


class Arrangement(games.Sprite):
    image = games.load_image('img/barrier.png')

    def __init__(self, y=-200, speed=4, odds_change=200):
        super(Arrangement, self).__init__(image=Arrangement.image,
                                          x=games.screen.width / 2,
                                          y=y,
                                          dx=speed)
        self.odds_change = odds_change
        self.time_til_drop = 0

    def update(self):
        if self.left < 0 or self.right > games.screen.width:
            self.dx = -self.dx
        elif random.randrange(self.odds_change) == 0:
            self.dx = -self.dx
        self.check_drop()

    def check_drop(self):
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            new_obstacle = Obstacles(x=self.x)
            games.screen.add(new_obstacle)

            self.time_til_drop = random.randint(95, 100)


class Obstacles(games.Sprite):

    rand = random.choice(['img/car3.png', 'img/car4.png', 'img/car5.png', 'img/car6.png', 'img/car7.png',
                         'img/barrier.png'])
    image = games.load_image(rand)
    speed = 3

    def __init__(self, x, y=0):
        super(Obstacles, self).__init__(image=Obstacles.image,
                                     x=x,
                                     y=y,
                                     dy=Obstacles.speed)

    # def update(self):


    def collision(self):
        self.destroy()


class Game:
    def __init__(self):
        self.car = Car(game=self,
                       x=games.screen.width / 2,
                       y=570)
        games.screen.add(self.car)

    def play(self):
        road_image = games.load_image('img/background.jpg', transparent=False)
        games.screen.background = road_image
        the_arrangement = Arrangement()
        games.screen.add(the_arrangement)
        games.screen.mainloop()

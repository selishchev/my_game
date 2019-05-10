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
            the_explosion = Explosion(self.x, self.y)
            games.screen.add(the_explosion)
            self.end_game()
            self.stop()

    @staticmethod
    def end_game():
        end_msg = games.Message(value='Вы проиграли!',
                                size=90,
                                color=color.red,
                                x=games.screen.width / 2,
                                y=games.screen.height / 2,
                                lifetime=3 * games.screen.fps,
                                after_death=games.screen.quit
                                )
        games.screen.add(end_msg)


class Explosion(games.Animation):

    images = []

    def __init__(self, x, y):
        for i in range(1, 46):
            Explosion.images.append('animation/explosion' + str(i) + '.png')
        super(Explosion, self).__init__(images=Explosion.images,
                                        x=x,
                                        y=y,
                                        repeat_interval=5, n_repeats=1)


class Arrangement(games.Sprite):
    image = games.load_image('img/car8.png')

    def __init__(self, y=-200, speed=5, odds_change=200):
        super(Arrangement, self).__init__(image=Arrangement.image,
                                          x=games.screen.width / 2,
                                          y=y,
                                          dx=speed)
        self.odds_change = odds_change
        self.time_til_drop = 0
        self.score = games.Text(value=0,
                                size=40,
                                right=games.screen.width - 15,
                                color=color.white,
                                top=5
                                )
        games.screen.add(self.score)

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
            new_obstacle = Obstacles(x=self.x, rand1=random.randint(3, 8), speed1=random.randrange(2, 4))
            games.screen.add(new_obstacle)
            self.score.value += 1
            self.time_til_drop = random.randint(90, 100)


class Obstacles(games.Sprite):

    rand = random.choice(['img/car3.png', 'img/car4.png', 'img/car5.png', 'img/car6.png', 'img/car7.png',
                         'img/car8.png'])
    image = games.load_image(rand)
    speed = 3

    def __init__(self, x, rand1, speed1, y=-100):
        super(Obstacles, self).__init__(image=games.load_image('img/car'+str(rand1)+'.png'),
                                        x=x,
                                        y=y,
                                        dy=speed1)

    def collision(self):
        self.destroy()


class Game:

    def __init__(self, rand):
        games.music.load('music/theme'+str(rand)+'.mp3')
        games.music.play(-1)
        self.car = Car(game=self,
                       x=games.screen.width / 2,
                       y=570)
        games.screen.add(self.car)

    @staticmethod
    def play():
        road_image = games.load_image('img/background.jpg', transparent=False)
        games.screen.background = road_image
        the_arrangement = Arrangement()
        games.screen.add(the_arrangement)
        games.screen.mainloop()

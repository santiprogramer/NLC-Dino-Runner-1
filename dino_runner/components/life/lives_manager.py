from dino_runner.components.life.lives import Lives


class LivesManager():
    def __init__(self):
        self.lives = []

    def draw(self, screen):
        for live in self.lives:
            live.draw(screen)

    def refill_lives(self):
        pos_x = 10
        for i in range(0, 3):
            self.lives.append(Lives(pos_x))
            pos_x += 30

    def delete_lives(self):
        self.lives.pop()

    def lives_counter(self):
        return len(self.lives)
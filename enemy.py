class Enemy:
    def __init__(self, x, y, health, damage):
        self.x = x
        self.y = y
        self.health = health
        self.damage = damage

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


class Canon(Enemy):
    pass


class Spike(Enemy):
    pass


class Walker(Enemy):
    pass


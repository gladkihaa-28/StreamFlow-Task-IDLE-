import random


class Random:
    def randint(self, min, max):
        return random.randint(min, max)

    def random(self):
        return random.random()

    def randrange(self, max, min=None, step=None):
        if min is None:
            return random.randrange(max)
        if step is None:
            return random.randrange(min, max)
        else:
            return random.randrange(min, max, step)

    def randsort(self, sp):
        random.shuffle(sp)
        return sp

    def randchoice(self, sp):
        return random.choice(sp)
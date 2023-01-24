#*******************************
class Monster(object):
    eats = 'food'

    def __init__(self, name):
        self.name = name

    def speak(self):
        print(self.name + " speaks")

    def eat(self, meal):
        if meal == self.eats:
            print("Yum!")
        else:
            print("BLECH!")

myMonster = Monster('Spooky Snack')
myMonster.speak()
myMonster.eat('food')
#*********************************
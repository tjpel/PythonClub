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

#*************************************************************
#myMonster = Monster('Spooky Snack')
#myMonster.speak()
#myMonster.eat('food')

class FrankenBurger(Monster):
    eats = 'hamburger patties'

    def speak(self):
        print("My name is " + self.name + "Burger.")

#Create an instance of Frankenburger with the name Veggie
myFrankenBurger = FrankenBurger("Veggie")
myFrankenBurger.speak()
myFrankenBurger.eat("Pickles")

class CrummyMummy(Monster):
    eats = 'chocolate chips'

    def speak(self):
        print("My name is " + self.name + "Mummy.")

#Have kids try to do this themselves?
class WereWatermellon(Monster):
    eats = 'watermelon juice'

    def speak(self):
        print("My name is Were" + self.name + ".")
#*******************************************************************
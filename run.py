from src.game import Game

print("Welcome to Veggie Garden, your own space to grow, harvest and sell vegetables!")
print("1: New Game")
print("2: Resume Game")
valid_input = False
while not valid_input:
    user_input = input("What would you like to do? (1 or 2): ")
    if user_input == "1" or user_input == "2":
        valid_input = True
    else:
        print("Invalid input. Please choose 1 or 2.")

if user_input == "1":
    game = Game(True)
else:
    game = Game(False)


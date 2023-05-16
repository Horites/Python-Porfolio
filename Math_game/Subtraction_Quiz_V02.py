import random

while True:  # is needed to repeat the program
    # 1. Generate two random single-digit integers
    number1 = random.randint(0, 9)
    number2 = random.randint(0, 9)

    # 2. If number1 < number2, swap number1 with number2
    if number1 < number2:
        number1, number2 = number2, number1  # Simultaneous assignment

    # 4. Prompt the student to answer "what is number1 - number2?"
    answer = int(input("What is " + str(number1) + " - " + str(number2) + "? "))

    # 5. Grade the answer and display the result
    print(f"{number1} - {number2} = {answer} is {number1 - number2 == answer}")

    if number1 - number2 == answer:
        print("You are correct!")
    else:
        print("Your answer is wrong.")
        print(number1, "-", number2, "is", number1 - number2)

    # This will allow the user to decide if they want to play again
    play_again = input("Play again? (y/n): ")
    if play_again.lower() != "y":
        break

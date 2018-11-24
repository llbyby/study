from random import randint


def isEqual(num1, num2):
    if num1 < num2:
        print("Too small~~")
        return False
    if num1 > num2:
        print("Too big~~")
        return False
    if num1 == num2:
        print("Bingo!")
        return True


bingo = False
num = randint(1, 10)
counter = 0
print("Guess what number?")
while not bingo:
    answer = None
    try:
        answer = int(input("Answer:"))
    except:
        pass
    if type(answer) == int:
        counter = counter + 1
        bingo = isEqual(answer, num)
    else:
        print("Please input number!")
print("You tried " + str(counter) + " times!")

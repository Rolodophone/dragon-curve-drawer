import colorsys
import turtle
# import threading


def main():
    iterations, distance, speed, extraSpeed, colourmode, variation = config()

    # if advancedMode and simultaneousDragoning:
    #     for i in range(numOfDragons):
    #         newT = turtle.Turtle()
    #         newTS = newT.getscreen()
    #         newT.speed = speed
    #         newTS.colormode(1.0)
    #         newT.hideturtle()
    #
    #         threading.Thread(target=lambda: drawDragon(newT, iterations, distance, colourmode, variation, startXs[i], startYs[i], rotations[i])).start()
    # else:
    newT = turtle.Turtle()
    newTS = newT.getscreen()
    newT.speed = speed
    newTS.delay(0)
    newTS.tracer(n=extraSpeed)
    newTS.colormode(1.0)
    newT.hideturtle()

    drawDragon(newT, iterations, distance, colourmode, variation)

    input("Press enter to exit")


def config():
    # I couldn't get threading to work with the turtle to draw simultaneously so I disabled this functionality

    # ans = input("Multi-dragon mode (y/n)? ")
    # if ans == "y":
    #     advancedMode = True
    # elif ans == "n":
    # advancedMode = False
    # else:
    #     print("Invalid input\n\n\n")
    #     config()
    #
    # if advancedMode:
    #     numOfDragons = int(input("How many dragons? "))
    #     ans = input("Draw simultaneously (y/n)? ")
    #     if ans == "y":
    #         simultaneousDragoning = True
    #     elif ans == "n":
    #         simultaneousDragoning = False
    #     else:
    #         print("Invalid input\n\n\n")
    #         config()
    # else:
    # numOfDragons = 1
    # simultaneousDragoning = False

    # if (advancedMode):
    #     print("\nFor all dragons...")
    iterations = int(input("How many iterations? "))
    distance = int(input("Side length in pixels? "))
    speed = int(input("Speed (0-10)? "))
    extraSpeed = int(input("Draw how many lines at a time (1+)? "))
    colourmode = input("Colour mode (none/global rainbow/local rainbow)? ")
    variation = input("Variation (none/onoff)? ")
    if not (colourmode == "none" or colourmode == "global rainbow" or colourmode == "local rainbow") or not (variation == "none" or variation == "onoff"):
        print("Invalid input\n\n\n")
        config()

    # ts = turtle.Turtle().getscreen()
    #
    # if advancedMode:
    #     startXs = []
    #     startYs = []
    #     rotations = []
    #     for i in range(numOfDragons):
    #         print("\nFor dragon #{}...".format(i+1))
    #
    #         ans = input("Starting x position? ")
    #         if ans == "default":
    #             startXs.append(ts.window_width() / 2)
    #         else:
    #             startXs.append(int(ans))
    #
    #         ans = input("Starting y position? ")
    #         if ans == "default":
    #             startYs.append(ts.window_height() / 2)
    #         else:
    #             startYs.append(int(ans))
    #
    #         ans = input("Starting rotation? ")
    #         if ans == "default":
    #             rotations.append(0)
    #         else:
    #             rotations.append(ans)
    #
    # else:
    #     startXs = [ts.window_width() / 2]
    #     startYs = [ts.window_height() / 2]
    #     rotations = [0]

    return iterations, distance, speed, extraSpeed, colourmode, variation  #, startXs, startYs, rotations


def drawDragon(t, iterations, distance, colourmode, variation):
    # t.goto(startX, startY)
    # t.setheading(rotation)
    t.forward(distance)

    oddLine = True

    movesToCopy = []

    for i in range(iterations):
        newMovesToCopy = list(movesToCopy)

        if colourmode == "global rainbow":
            t.color(colorsys.hsv_to_rgb((i / iterations), 0.8, 0.8))

        if i != 0:
            t.right(90)
            newMovesToCopy.insert(0, -1)
            t.forward(distance)

        for i, move in enumerate(movesToCopy):
            if colourmode == "local rainbow":
                t.color(colorsys.hsv_to_rgb((i / len(movesToCopy)), 0.8, 0.8))

            if variation == "onoff":
                if oddLine:
                    oddLine = False
                    t.penup()
                else:
                    oddLine = True
                    t.pendown()


            if move == 1:
                t.right(90)
                newMovesToCopy.insert(0, -1)

            elif move == -1:
                t.left(90)
                newMovesToCopy.insert(0, 1)

            t.forward(distance)

        movesToCopy = list(newMovesToCopy)


main()

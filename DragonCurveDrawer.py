import colorsys
import json
import turtle
import threading
import queue
import sys
import time


def main():
    iterations, distance, delay, speed, extraSpeed, colourMode, variation, startXs, startYs, rotations, simultaneousDrawing, numOfDragons \
        = config()

    commandQueue = queue.Queue(1)
    threads = []

    for i in range(numOfDragons):
        newT = turtle.Turtle()
        newTS = newT.getscreen()
        newT.speed = speed
        newTS.delay(delay)
        newTS.tracer(n=extraSpeed)
        newTS.colormode(1.0)
        newT.hideturtle()

        thread = threading.Thread(target=lambda:
            drawDragon(newT, iterations, distance, colourMode, variation, startXs[i], startYs[i], rotations[i], commandQueue))
        thread.daemon = True  # if main thread dies early (e.g. close button pressed), drawing threads will die
        thread.start()
        threads.append(thread)

    processQueue(commandQueue)

    # wait until drawing is finished
    for thread in threads:
        thread.join()


def processQueue(commandQueue):
    while not commandQueue.empty():
        commandQueue.get()()  # invoke command

    time.sleep(0.1)
    processQueue(commandQueue)

    print("Finished drawing.")


def config():
    fileName = None

    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    else:
        ans = input("Load config from file (y/N)? ")
        if ans == "y":
            fileName = input("Enter file name, including extension: ")

    if fileName is not None:
        with open(fileName, "r") as file:
            d = json.load(file)

        return d["iterations"], d["distance"], d["delay"], d["speed"], d["extraSpeed"], d["colourMode"], d["variation"], d["startXs"], \
            d["startYs"], d["rotations"], d["simultaneousDrawing"], d["numOfDragons"]

    ans = input("Multi-dragon mode (y/N)? ")
    if ans == "y":
        advancedMode = True
    else:
        advancedMode = False

    if advancedMode:
        numOfDragons = int(input("How many dragons? "))
        ans = input("Draw simultaneously (Y/n)? ")
        if ans == "n":
            simultaneousDrawing = False
        else:
            simultaneousDrawing = True
    else:
        numOfDragons = 1
        simultaneousDrawing = False

    if advancedMode:
        print("\nFor all dragons...")

    iterations = int(input("How many iterations? "))
    distance = int(input("Side length in pixels? "))
    delay = int(input("Delay? "))
    speed = int(input("Speed (0-10)? "))
    extraSpeed = int(input("Draw how many lines at a time (1+)? "))
    colourMode = input("Colour mode (none/global rainbow/local rainbow)? ")
    variation = input("Variation (none/onoff)? ")

    if not (colourMode == "none" or colourMode == "global rainbow" or colourMode == "local rainbow") or not (variation == "none" or variation == "onoff"):
        print("Invalid input")
        exit()

    if advancedMode:
        startXs = []
        startYs = []
        rotations = []
        for i in range(numOfDragons):
            print("\nFor dragon #{}...".format(i+1))
            startXs.append(int(input("Starting x position? ")))
            startYs.append(int(input("Starting y position? ")))
            rotations.append(int(input("Starting rotation? ")))

    else:
        startXs = [960]
        startYs = [540]
        rotations = [0]

    return iterations, distance, delay, speed, extraSpeed, colourMode, variation, startXs, startYs, rotations, \
        simultaneousDrawing, numOfDragons


def drawDragon(t: turtle.Turtle, iterations: int, distance: int, colourMode: str, variation: str, startX: int, startY: int, rotation: int,
               commandQueue: queue.Queue):
    commandQueue.put(lambda: t.goto(startX, startY))
    commandQueue.put(lambda: t.setheading(rotation))
    commandQueue.put(lambda: t.forward(distance))

    oddLine = True

    movesToCopy = []

    for i in range(iterations):
        newMovesToCopy = list(movesToCopy)

        if colourMode == "global rainbow":
            commandQueue.put(lambda: t.color(colorsys.hsv_to_rgb((i / iterations), 0.8, 0.8)))

        if i != 0:
            commandQueue.put(lambda: t.right(90))
            newMovesToCopy.insert(0, -1)
            commandQueue.put(lambda: t.forward(distance))

        for i, move in enumerate(movesToCopy):
            if colourMode == "local rainbow":
                commandQueue.put(lambda: t.color(colorsys.hsv_to_rgb((i / len(movesToCopy)), 0.8, 0.8)))

            if variation == "onoff":
                if oddLine:
                    oddLine = False
                    commandQueue.put(lambda: t.penup())
                else:
                    oddLine = True
                    commandQueue.put(lambda: t.pendown())

            if move == 1:
                commandQueue.put(lambda: t.right(90))
                newMovesToCopy.insert(0, -1)

            elif move == -1:
                commandQueue.put(lambda: t.left(90))
                newMovesToCopy.insert(0, 1)

            commandQueue.put(lambda: t.forward(distance))

        movesToCopy = list(newMovesToCopy)


if __name__ == "__main__":
    main()
    input("Press enter to exit.")  # keep window open when turtle finishes

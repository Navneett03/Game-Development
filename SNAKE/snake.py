from turtle import *
import time
import random
from os import path
import threading
from playsound import playsound

# Set color mode to RGB
colormode(255)

# Game delay and initial score
delay = 0.1
score = 0

# Set up the game window
wn = Screen()
wn.bgcolor('forestgreen')
wn.title("SNAKE GAME")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turn off the screen updates

# High score file path
HS_FILE = "highscore.txt"
dir = path.dirname(__file__)

# Read the high score from the file
with open(path.join(dir, HS_FILE), 'r') as f:
    try:
        highscore = int(f.read())
    except:
        highscore = 0

# Create the snake's head
head = Turtle('square')
head.speed(0)
head.color('black')
head.up()
head.dir = "stop"

# List to store the snake's body segments
snake_body = []

# Create the score display
pen = Turtle()
pen.speed(0)
pen.hideturtle()
pen.color('blue')
pen.up()
pen.goto(0, 260)
font = ("Courier", 24, "bold")
pen.write("SCORE: {}    HIGH SCORE: {}".format(score, highscore), align="center", font=font)

# Create the food
food = Turtle('circle')
food.speed(0)
food.color('red')
food.up()
food.goto(0, 150)

# Functions to control the snake's direction
def go_up():
    if head.dir != "down":
        head.dir = "up"

def go_down():
    if head.dir != "up":
        head.dir = "down"

def go_right():
    if head.dir != "left":
        head.dir = "right"

def go_left():
    if head.dir != "right":
        head.dir = "left"

# Function to move the snake
def move():
    if head.dir == "up":
        head.sety(head.ycor() + 20)
    if head.dir == "down":
        head.sety(head.ycor() - 20)
    if head.dir == "right":
        head.setx(head.xcor() + 20)
    if head.dir == "left":
        head.setx(head.xcor() - 20)

# Function to play the fruit sound
def play_fruit_sound():
    threading.Thread(target=playsound, args=("fruit.mp3",), daemon=True).start()

# Set up the keyboard bindings
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_right, "Right")
wn.onkeypress(go_left, "Left")

# Initial color index
color_index = 0

# Game loop
run_game = True    
while run_game:
    wn.update()

    # Check for collision with the wall
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        playsound("death.mp3", block=False)
        time.sleep(0.5)
        head.goto(0, 0)
        head.dir = "stop"

        # Hide the snake body segments
        for segment in snake_body:
            segment.hideturtle()
        snake_body.clear()

        # Reset the score display
        pen.clear()
        pen.write("SCORE: {}    HIGH SCORE: {}".format(score, highscore), align="center", font=font)
        run_game = False

    # Check for collision with food
    if head.distance(food) <= 20:
        color_index += 1
        color_choice = color_index % 3
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        food.goto(x, y)

        # Create a new body segment
        new_segment = Turtle('square')
        new_segment.speed(0)
        if color_choice == 1:
            new_segment.color('red')
        elif color_choice == 2:
            new_segment.color('blue')
        else:
            new_segment.color('black')
        new_segment.up()
        snake_body.append(new_segment)

        # Increase the score
        score += 10
        if score > highscore:
            highscore = score

        # Update the score display
        pen.clear()
        pen.write("SCORE: {}    HIGH SCORE: {}".format(score, highscore), align="center", font=font)

        # Play fruit sound
        play_fruit_sound()

    # Move the body segments in reverse order
    for index in range(len(snake_body) - 1, 0, -1):
        x = snake_body[index - 1].xcor()
        y = snake_body[index - 1].ycor()
        snake_body[index].goto(x, y)

    # Move the first body segment to where the head is
    if len(snake_body) > 0:
        x = head.xcor()
        y = head.ycor()
        snake_body[0].goto(x, y)

    # Move the snake
    move()

    # Check for collision with the snake's body
    for segment in snake_body:
        if segment.distance(head) < 20:
            playsound("death.mp3", block=False)
            time.sleep(0.5)
            head.goto(0, 0)
            head.dir = "stop"

            # Reset the score display
            pen.clear()
            pen.write("SCORE: {}    HIGH SCORE: {}".format(score, highscore), align="center", font=font)

            # Hide the snake body segments
            for segment in snake_body:
                segment.hideturtle()
            snake_body.clear()
            run_game = False   

    time.sleep(delay)

# Hide the food
food.hideturtle()
wn.update()
pen.goto(0, 50)

# Display game over or new high score message
if score >= highscore:
    pen.color('cyan')
    pen.write("NEW HIGH SCORE!", align='center', font=("Arial", 30, "bold"))
    with open(path.join(dir, HS_FILE), 'w') as f:
        f.write(str(highscore))
else:
    pen.color('red')
    pen.write("GAME OVER", align='center', font=("Arial", 30, "bold"))

wn.mainloop()
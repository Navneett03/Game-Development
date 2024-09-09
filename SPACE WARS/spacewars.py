from turtle import *
import time
import random
from os import path
import threading
from playsound import playsound

# Function to play sound asynchronously
def play_sound(file):
    threading.Thread(target=playsound, args=(file,), daemon=True).start()

# Set up the game window
wn = Screen()
wn.bgcolor('black')
wn.bgpic("space.gif")
wn.title("SPACE WARS")
wn.setup(width=0.99, height=0.91, startx=0, starty=0)
wn.tracer(0)

# Game variables
score = 0
lives = 3
delay = 0.05

# High score file path
HS_FILE = "high.txt"
dir = path.dirname(__file__)

# Read the high score from the file
with open(path.join(dir, HS_FILE), 'r') as f:
    try:
        highscore = int(f.read())
    except:
        highscore = 0

# Display the high score
highscore_display = Turtle()
highscore_display.ht()
highscore_display.up()
highscore_display.goto(200, 310)
highscore_display.color('green')
highscore_display.write("HighScore: {}".format(highscore), align='center', font=('Courier', 20, 'bold'))

# Draw the game border
border_drawer = Turtle()
border_drawer.up()
border_drawer.ht()
border_drawer.speed(0)
border_drawer.goto(-400, -300)
border_drawer.pensize(7)
border_drawer.color('brown')
border_drawer.down()
for _ in range(2):
    border_drawer.forward(800)
    border_drawer.left(90)
    border_drawer.forward(600)
    border_drawer.left(90)

# Create the title display
title_display = Turtle()
title_display.ht()
title_display.color('forestgreen')
title_display.up()
title_display.goto(-540, 0)
title_display.left(90)
title_display.write("SPACE", align='center', font=('Arial', 50, 'italic'))
title_display.goto(525, 0)
title_display.write("WARS", align='center', font=('Arial', 50, 'italic'))

# Lists to store enemies and allies
enemies = []
allies = []

# Display the score and lives
score_display = Turtle()
score_display.ht()
score_display.up()
score_display.goto(-200, 310)
score_display.color('white')
score_display.write("SCORE: {}     LIVES: {}".format(score, lives), align='center', font=('Courier', 20, 'normal'))

# Function to initialize an enemy
def create_enemy(name, x, y):
    name.shape('circle')
    name.color('red')
    name.up()
    name.speed(0)
    name.goto(x, y)
    name.seth(90)

# Function to initialize an ally
def create_ally(name, x, y):
    name.shape('square')
    name.color('blue')
    name.up()
    name.speed(0)
    name.goto(x, y)
    name.seth(270)

# Function to move an enemy
def move_enemy(enemy, speed):
    enemy.forward(speed)
    random_direction = random.randint(0, 360)
    if enemy.xcor() > 390:
        enemy.setx(390)
        enemy.left(random_direction)
    if enemy.xcor() < -390:
        enemy.setx(-390)
        enemy.left(random_direction)
    if enemy.ycor() > 290:
        enemy.sety(290)
        enemy.left(random_direction)
    if enemy.ycor() < -290:
        enemy.sety(-290)
        enemy.left(random_direction)

# Function to detect collisions between objects
def collision(obj1, obj2, dist):
    if obj1.distance(obj2) <= dist:
        obj1.goto(random.randint(-350, 350), random.randint(-250, 250))

# Initialize enemies
for _ in range(8):
    enemy = Turtle()
    x = random.randint(-350, 350)
    y = random.randint(100, 250)
    create_enemy(enemy, x, y)
    enemies.append(enemy)

# Initialize allies
for _ in range(8):
    ally = Turtle()
    x = random.randint(-350, 350)
    y = random.randint(-250, -100)
    create_ally(ally, x, y)
    allies.append(ally)

# Initialize missile
missile = Turtle()
def initialize_missile(missile):
    missile.shape('triangle')
    missile.color('yellow')
    missile.speed(0)
    missile.shapesize(0.5, outline=None)
    missile.ht()
    missile.up()
    missile.status = "ready"

# Function to fire a missile
def fire_missile(missile, player):
    missile.goto(player.xcor(), player.ycor())
    missile.showturtle()
    missile.seth(player.heading())
    play_sound("missile.mp3")
    if missile.status == "ready":
        missile.status = "firing"

# Function to get the missile ready to fire
def ready_to_fire():
    fire_missile(missile, player)

# Function to move the missile when fired
def move_missile(missile, speed):
    if missile.status == "firing":
        missile.forward(speed)
    if missile.xcor() >= 390 or missile.xcor() <= -390 or missile.ycor() >= 290 or missile.ycor() <= -290:
        missile.ht()
        missile.status = "ready"
        missile.goto(500, 0)

initialize_missile(missile)

# Initialize the player's spaceship
player = Turtle('triangle')
player.seth(90)
player.color('white')
player.up()
player.shapesize(1.2)

# Player's movement speed
player_speed = 3

# Functions to control the player
def turn_left():
    player.left(45)

def turn_right():
    player.right(45)

def accelerate():
    global player_speed
    player_speed += 1
    if player_speed >= 15:
        player_speed = 15

def decelerate():
    global player_speed
    player_speed -= 1
    if player_speed <= -15:
        player_speed = -15

# Set up keyboard bindings
wn.listen()
wn.onkeypress(turn_left, "Left")
wn.onkeypress(turn_right, "Right")
wn.onkeypress(accelerate, "Up")
wn.onkeypress(decelerate, "Down")
wn.onkey(ready_to_fire, "space")

# Main game loop
game_running = True
while game_running:
    wn.update()
    player.forward(player_speed)
    time.sleep(delay)

    # Check for player collision with walls
    if player.xcor() >= 390:
        player.setx(390)
        player.left(60)
    if player.xcor() <= -390:
        player.setx(-390)
        player.left(60)
    if player.ycor() >= 290:
        player.sety(290)
        player.left(60)
    if player.ycor() <= -290:
        player.sety(-290)
        player.left(60)

    # Move the missile
    move_missile(missile, 20)

    # Move enemies and check for collisions
    for enemy in enemies:
        move_enemy(enemy, 8)
        if enemy.distance(player) <= 20:
            enemy.goto(random.randint(-350, 350), random.randint(-250, 250))
            lives -= 1
            score -= 50
            score_display.clear()
            score_display.write("SCORE: {}     LIVES: {}".format(score, lives), align='center', font=('Courier', 20, 'normal'))
            play_sound("crash.mp3")
        if enemy.distance(missile) <= 20:
            play_sound("explosion.mp3")
            enemy.goto(random.randint(-350, 350), random.randint(-250, 250))
            score += 100
            score_display.clear()
            score_display.write("SCORE: {}     LIVES: {}".format(score, lives), align='center', font=('Courier', 20, 'normal'))
            missile.status = "ready"
            missile.goto(1000, 0)

    # Move allies and check for collisions
    for ally in allies:
        move_enemy(ally, 8)
        if ally.distance(player) <= 20:
            ally.goto(random.randint(-350, 350), random.randint(-250, 250))
            score -= 50
            score_display.clear()
            score_display.write("SCORE: {}     LIVES: {}".format(score, lives), align='center', font=('Courier', 20, 'normal'))
            play_sound("crash.mp3")
        if ally.distance(missile) <= 20:
            play_sound("explosion.mp3")
            ally.goto(random.randint(-350, 350), random.randint(-250, 250))
            score += 50
            score_display.clear()
            score_display.write("SCORE: {}     LIVES: {}".format(score, lives), align='center', font=('Courier', 20, 'normal'))
            missile.status = "ready"
            missile.goto(1000, 0)

    # Check if lives are depleted
    if lives <= 0:
        game_running = False

# End game and update high score if necessary
wn.update()
if score > highscore:
    highscore = score
    highscore_display.clear()
    highscore_display.write("HighScore: {}".format(highscore), align='center', font=('Courier', 20, 'bold'))
    highscore_display.goto(0, 0)
    highscore_display.color('cyan')
    highscore_display.write("New High Score",align='center',font=('Courier',50,'bold'))
    with open(path.join(dir,HS_FILE),'w') as f:
        f.write(str(highscore))
else:
    highscore_display.goto(0,0)
    highscore_display.color('red')
    highscore_display.write("Game Over",align='center',font=('Courier',50,'bold'))
    
wn.mainloop()
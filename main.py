import turtle
import time
import random

# Screen setup
wn = turtle.Screen()
wn.title("Space Invaders")
wn.bgcolor("black")
wn.setup(width=600, height=700)
wn.tracer(0)

# Register a triangle shape for the player
turtle.register_shape("triangle", ((-10, -10), (10, -10), (0, 10)))

# Create the player
player = turtle.Turtle()
player.shape("triangle")
player.color("white")
player.penup()
player.goto(0, -300)
player.setheading(90)

# Create the bullet
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("red")
bullet.shapesize(0.2, 1)
bullet.penup()
bullet.hideturtle()
bullet_speed = 20
bullet_state = "ready"

# Create a grid of aliens
aliens = []
alien_speed = 10

rows = 3
cols = 7
start_x = -210
start_y = 250
spacing_x = 70
spacing_y = 50

for row in range(rows):
    for col in range(cols):
        alien = turtle.Turtle()
        alien.shape("circle")
        alien.color("green")
        alien.penup()
        x = start_x + col * spacing_x
        y = start_y - row * spacing_y
        alien.goto(x, y)
        aliens.append(alien)

# Movement functions
def move_left():
    x = player.xcor()
    if x > -280:
        player.setx(x - 20)

def move_right():
    x = player.xcor()
    if x < 280:
        player.setx(x + 20)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 10)
        bullet.showturtle()

def is_collision(t1, t2):
    return t1.distance(t2) < 20

# Keyboard bindings
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# Main game variables
last_move_time = time.time()
game_over = False
victory = False

# Main game loop with error handling
try:
    while not game_over:
        wn.update()

        # Bullet movement
        if bullet_state == "fire":
            y = bullet.ycor()
            bullet.sety(y + bullet_speed)

            # If bullet goes off screen
            if bullet.ycor() > 300:
                bullet.hideturtle()
                bullet_state = "ready"

        # Move aliens down every second
        current_time = time.time()
        if current_time - last_move_time > 1:
            last_move_time = current_time
            for alien in aliens:
                alien.sety(alien.ycor() - 20)

                # Check if aliens reach the player
                if alien.ycor() < -270:
                    game_over = True
                    victory = False
                    break

        # Bullet collision with aliens
        for alien in aliens[:]:  # Iterate over a copy
            if is_collision(bullet, alien):
                bullet.hideturtle()
                bullet_state = "ready"
                alien.goto(1000, 1000)  # Move off-screen
                aliens.remove(alien)

                # ✅ Check for win condition
                if len(aliens) == 0:
                    game_over = True
                    victory = True

except turtle.Terminator:
    print("Turtle graphics window was closed. Exiting gracefully.")

# End of game
player.hideturtle()
bullet.hideturtle()
for alien in aliens:
    alien.hideturtle()

# Show Game Over or You Won message
message = turtle.Turtle()
message.color("white")
message.penup()
message.hideturtle()
message.goto(0, 0)

if victory:
    message.write("🎉 YOU WON! 🎉", align="center", font=("Arial", 24, "bold"))
else:
    message.write("💥 GAME OVER 💥", align="center", font=("Arial", 24, "bold"))

wn.mainloop()

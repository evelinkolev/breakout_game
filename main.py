import turtle
import random

# Screen setup
win = turtle.Screen()
win.title("Breakout Game")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)


# Paddle class
class Paddle:
    def __init__(self):
        self.paddle = turtle.Turtle()
        self.paddle.speed(0)
        self.paddle.shape("square")
        self.paddle.color("white")
        self.paddle.shapesize(stretch_wid=1, stretch_len=5)
        self.paddle.penup()
        self.paddle.goto(0, -250)
        self.paddle.dx = 20

    def move_left(self):
        x = self.paddle.xcor()
        x -= self.paddle.dx
        if x < -350:
            x = -350
        self.paddle.setx(x)

    def move_right(self):
        x = self.paddle.xcor()
        x += self.paddle.dx
        if x > 350:
            x = 350
        self.paddle.setx(x)


# Ball class
class Ball:
    def __init__(self):
        self.ball = turtle.Turtle()
        self.ball.speed(40)
        self.ball.shape("square")
        self.ball.color("red")
        self.ball.penup()
        self.ball.goto(0, 0)
        self.ball.dx = 0.175
        self.ball.dy = -0.175
        self.speed_factor = 1.05

    def move(self):
        self.ball.setx(self.ball.xcor() + self.ball.dx)
        self.ball.sety(self.ball.ycor() + self.ball.dy)

    def bounce_x(self):
        self.ball.dx *= -1
        self.increase_speed()

    def bounce_y(self):
        self.ball.dy *= -1
        self.increase_speed()

    def increase_speed(self):
        self.ball.dx *= self.speed_factor
        self.ball.dy *= self.speed_factor

    def reset_position(self):
        self.ball.goto(0, 0)
        self.ball.dx = 0.175 * random.choice([-1, 1])
        self.ball.dy = -0.175


# Brick class
class Brick:
    def __init__(self, x, y):
        self.brick = turtle.Turtle()
        self.brick.speed(0)
        self.brick.shape("square")
        self.brick.color("blue")
        self.brick.shapesize(stretch_wid=1, stretch_len=2)
        self.brick.penup()
        self.brick.goto(x, y)
        self.brick.broken = False


# Create paddle
paddle = Paddle()

# Create ball
ball = Ball()

# Create bricks
bricks = []
for i in range(-350, 400, 70):
    for j in range(100, 250, 30):
        brick = Brick(i, j)
        bricks.append(brick)

# Keyboard bindings
win.listen()
win.onkeypress(paddle.move_left, "Left")
win.onkeypress(paddle.move_right, "Right")

# Main game loop
while True:
    win.update()

    # Move the ball
    ball.move()

    # Border checking
    if ball.ball.xcor() > 390:
        ball.ball.setx(390)
        ball.bounce_x()

    if ball.ball.xcor() < -390:
        ball.ball.setx(-390)
        ball.bounce_x()

    if ball.ball.ycor() > 290:
        ball.ball.sety(290)
        ball.bounce_y()

    if ball.ball.ycor() < -290:
        ball.reset_position()

    # Paddle collision
    if (-240 < ball.ball.ycor() < -230) and \
            (paddle.paddle.xcor() - 50 < ball.ball.xcor() < paddle.paddle.xcor() + 50):
        ball.ball.sety(-230)
        ball.bounce_y()

    # Brick collision
    for brick in bricks:
        if not brick.brick.broken:
            if (brick.brick.ycor() - 15 < ball.ball.ycor() < brick.brick.ycor() + 15) and \
                    (brick.brick.xcor() - 30 < ball.ball.xcor() < brick.brick.xcor() + 30):
                ball.bounce_y()
                brick.brick.goto(1000, 1000)
                brick.brick.broken = True

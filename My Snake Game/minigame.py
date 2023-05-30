import turtle
import time
import random
# You must install => pip install playsound==1.2.2 => this version of playsound otherwise it
# cannot play audio files on latest versions of Pycharm
from playsound import playsound

game_results = []


def snake_game(mode):
    game_won = False
    DELAY = 0.10  # Speed of the snake
    snake_score = 0
    WIDTH = 600  # Width of the playground
    HEIGHT = 600  # Width of the playground
    SEGMENT_SIZE = 20  # Size of the part of the snake (default size of turtle)

    # Create Window
    window = turtle.Screen()
    window.title("Snake Game")

    window.bgpic("./MySnakeGame/Optimized1.gif")
    window.setup(width=WIDTH, height=HEIGHT)
    window.tracer(0)  # closes the animation

    # Starting position of the snake
    start_x = 0
    start_y = 0
    ############# Create Objects #############
    # Create Snake
    turtle.register_shape('./MySnakeGame/head.gif')  # Add a gif visualization to snake
    snake = turtle.Turtle()
    snake.shape("./MySnakeGame/head.gif")
    snake.penup()
    snake.goto(start_x, start_y)
    snake.direction = "stop"

    # Create Apple
    turtle.register_shape('./MySnakeGame/apple2.gif')  # Add a gif visualization to food
    food = turtle.Turtle()
    food.shape("./MySnakeGame/apple2.gif")
    food.penup()
    food.goto(0, 100)
    food.shapesize(0.80, 0.80)
    #########################################

    # body part of the snake
    segments = []

    ################ Sound Effects ################
    def play_eat_sound():
        playsound("./MySnakeGame/eat.wav")

    def play_win_sound():
        playsound("./MySnakeGame/levelup.wav")

    def play_loser_sound():
        playsound("./MySnakeGame/loser.wav")

    ########## Movement functions of snake ##########
    def go_up():
        if snake.direction != "down":
            snake.direction = "up"

    def go_down():
        if snake.direction != "up":
            snake.direction = "down"

    def go_left():
        if snake.direction != "right":
            snake.direction = "left"

    def go_right():
        if snake.direction != "left":
            snake.direction = "right"

    def restart():
        segments.clear()
        window.clear()
        window.reset()
        snake_game(mode)

    # Input Cases
    window.listen()
    window.onkeypress(go_up, "w")
    window.onkeypress(go_down, "s")
    window.onkeypress(go_left, "a")
    window.onkeypress(go_right, "d")
    window.onkeypress(restart, 'space')

    ################ Show Score on the screen ################

    point = turtle.Turtle()
    point.speed(0)  # highest speed
    point.color('white')
    point.penup()
    point.goto(0, 270)  # position of writing
    point.write(f"Score: {snake_score}", align="center", font=("Arial", 10, "bold"))

    ############################################################

    def move():
        """ Change the direction of the code"""
        if snake.direction == "up":
            snake.sety(snake.ycor() + SEGMENT_SIZE)
        if snake.direction == "down":
            snake.sety(snake.ycor() - SEGMENT_SIZE)
        if snake.direction == "left":
            snake.setx(snake.xcor() - SEGMENT_SIZE)
        if snake.direction == "right":
            snake.setx(snake.xcor() + SEGMENT_SIZE)

    # Snake cannot eat itself
    def check_collision():
        for segment in segments:
            if segment.distance(snake) < SEGMENT_SIZE:
                pass

    # Main game loop
    try:
        while True:
            window.update()

            if (snake.xcor() > HEIGHT / 2 or snake.xcor() < - (HEIGHT / 2)
                    or snake.ycor() > WIDTH / 2 or snake.ycor() < - (WIDTH / 2)):
                break
            # Check snake is eating itself
            if check_collision():
                print("You've eaten yourself !!!")
                break

            # check the snake whether it eat the apple
            if snake.distance(food) < SEGMENT_SIZE:
                # selects a random coordinate to create new apple object
                x = random.randint(-(HEIGHT // 2) + SEGMENT_SIZE, (HEIGHT // 2) - SEGMENT_SIZE)
                y = random.randint(-(HEIGHT // 2) + SEGMENT_SIZE, (HEIGHT // 2) - SEGMENT_SIZE)
                play_eat_sound()
                food.goto(x, y)
                point.clear()
                snake_score += 10
                point.write(f"Score: {snake_score}", align="center", font=("Arial", 10, "bold"))

                DELAY -= 0.01

                # Add new segment
                turtle.register_shape("./MySnakeGame/body.gif")
                new_segment = turtle.Turtle()
                new_segment.speed(0)
                new_segment.shape("./MySnakeGame/body.gif")
                new_segment.penup()
                segments.append(new_segment)

            #  It updates the positions of the snake's body segments based on the previous segment's position.
            #  iterates through the segments in reverse order, starting from the last segment, and assigns the coordinates
            for part in range(len(segments) - 1, 0, -1):
                x = segments[part - 1].xcor()
                y = segments[part - 1].ycor()
                segments[part].goto(x, y)

            if len(segments) > 0:
                x = snake.xcor()
                y = snake.ycor()
                segments[0].goto(x, y)

            move()
            time.sleep(DELAY)

        pen = turtle.Turtle()
        pen.speed(0)  # highest speed
        pen.color('white')

        if snake_score >= mode * 10:
            # write the sentence on screen
            game_won = True
            game_results.append(game_won)
            pen.penup()
            pen.goto(0, 0)  # position of writing
            pen.write("You've earned enough point to play Lexi-Q !!!", align="center", font=("Arial", 20, "bold"))
            play_win_sound()
            turtle.mainloop()



        else:
            # write the sentence on screen
            game_results.append(game_won)
            pen.penup()
            pen.goto(0, 0)  # position of writing
            pen.write("You've not earned enough\npoint to play Lexi-Q !!!\nPress space to play again :)",
                      align="center", font=("Arial", 20, "bold"))
            play_loser_sound()
            turtle.mainloop()


    except turtle.Terminator:
        # Handle the window closed exception
        restart()

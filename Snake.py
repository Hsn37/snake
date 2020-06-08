import pyglet
from pyglet.window import key
from random import seed
from random import randint


SPEED = 0.07    # cannot be negative. 0 means fastest.


class Snake:

    body = pyglet.resource.image('assets/body.png')  # image for the body
    head = pyglet.resource.image('assets/head.png')
    bg = pyglet.resource.image('assets/background.png')
    direction = {'UP': 0, 'RIGHT': 90, 'DOWN': 180, 'LEFT': 270}  # dictionary defining the directions, where the
    batch = pyglet.graphics.Batch()  # numbers are angles, moving clockwise.
    sprites = [pyglet.sprite.Sprite(img=head, batch=batch)]  # contains the blocks of body of the snake
    snake = [direction['UP']]  # contains directions, of the sprites
    turnPoints = []  # contains the points where the body is supposed to turn
    prev_dir = []  # contains all the directions that the head has taken, and are yet to be taken by the body
    flag = False

    def __init__(self):
        pass

    def add_block(self):

        last_index = len(self.sprites) - 1
        self.sprites.append(pyglet.sprite.Sprite(img=self.body, batch=self.batch))
        self.snake.append(self.snake[last_index])

        # adding block considering the direction of the last block of the snake
        if self.snake[last_index] == self.direction['UP']:
            self.sprites[last_index + 1].y = self.sprites[last_index].y - 10
            self.sprites[last_index + 1].x = self.sprites[last_index].x

        elif self.snake[last_index] == self.direction['RIGHT']:
            self.sprites[last_index + 1].x = self.sprites[last_index].x - 10
            self.sprites[last_index + 1].y = self.sprites[last_index].y

        elif self.snake[last_index] == self.direction['LEFT']:
            self.sprites[last_index + 1].x = self.sprites[last_index].x + 10
            self.sprites[last_index + 1].y = self.sprites[last_index].y

        elif self.snake[last_index] == self.direction['DOWN']:
            self.sprites[last_index + 1].y = self.sprites[last_index].y + 10
            self.sprites[last_index + 1].x = self.sprites[last_index].x

    def update_snake(self):

        last_index = len(self.sprites) - 1

        # checking each block. If any block is at a turning point, its direction is changed to the direction stored in
        # prev_dir, at the corresponding index
        for y in range(1, last_index + 1):
            for k in range(0, len(self.turnPoints)):
                if self.sprites[y].x == self.turnPoints[k][0] and self.sprites[y].y == self.turnPoints[k][1]:
                    self.snake[y] = self.prev_dir[k]

                    # if the last block has passed a turning point, remove it from the list
                    if y == last_index:
                        self.flag = True

        if self.flag:
            self.prev_dir.pop(0)
            self.turnPoints.pop(0)
            self.flag = False

    def move_ahead(self):

        last_index = len(self.sprites) - 1
        for n in range(0, last_index + 1):
            if self.snake[n] == self.direction['UP']:
                self.sprites[n].y += 10
            elif self.snake[n] == self.direction['RIGHT']:
                self.sprites[n].x += 10
            elif self.snake[n] == self.direction['DOWN']:
                self.sprites[n].y -= 10
            elif self.snake[n] == self.direction['LEFT']:
                self.sprites[n].x -= 10


game_window = pyglet.window.Window(500, 320, 'Snake Classic')
WIDTH = 1280    # screen width
HEIGHT = 720    # screen height
game_window.set_location(x=WIDTH // 2 - 250, y=HEIGHT // 2 - 150)

sn = Snake()

food = [100, 200]  # initial coordinates of the food item
food_img = pyglet.resource.image('assets/food.png')  # image of food
seed(randint(0, 100))
score_string = '0'
score = pyglet.text.Label('Score: ', font_size=15, font_name='Times New Roman', x=200, y=305)
score_number = pyglet.text.Label(score_string, font_size=15, font_name='Times New Roman', x=260, y=305)


def generate_food():

    global food
    food_flag = True
    while food_flag:
        x_coord = randint(0, 49) * 10
        food[0] = x_coord

        y_coord = randint(0, 28) * 10
        food[1] = y_coord

        for n in range(0, len(sn.sprites)):
            if sn.sprites[n].x == x_coord and sn.sprites[n].y == y_coord:
                break
            elif n == len(sn.sprites) - 1:
                food_flag = False


def ate_itself():

    for k in range(1, len(sn.sprites)):
        if [sn.sprites[0].x, sn.sprites[0].y] == [sn.sprites[k].x, sn.sprites[k].y]:
            return True

    return False


def food_eaten():      # food

    if food[0] == sn.sprites[0].x and food[1] == sn.sprites[0].y:
        generate_food()
        sn.add_block()
        update_score()


def update_score():    # score_string, score_number

    global score_string, score_number
    n = int(score_string)
    n = n + 17
    score_string = str(n)
    score_number = pyglet.text.Label(score_string, font_size=15, font_name='Times New Roman', x=260, y=305)


def border_check():

    if sn.sprites[0].x >= 500 or sn.sprites[0].x < -1 or sn.sprites[0].y < -1 or sn.sprites[0].y >= 300:
        return True
    else:
        return False


def game_over():

    print('Game Over')
    pyglet.clock.unschedule(update)


def update(dt):

    sn.update_snake()
    sn.move_ahead()

    if border_check() or ate_itself():
        game_over()
        return

    food_eaten()


@game_window.event
def on_key_press(symbol, modifiers):

    # using sprites[0] and snake[0] for the head of the snake
    # if two inputs made at the same point, discard the latter
    if len(sn.turnPoints) > 0:
        if sn.sprites[0].x == sn.turnPoints[len(sn.turnPoints) - 1][0] and sn.sprites[0].y == \
                sn.turnPoints[len(sn.turnPoints) - 1][1]:
            return

    if symbol == key.UP:
        if sn.snake[0] == sn.direction['DOWN'] or sn.snake[0] == sn.direction['UP']:
            return
        sn.turnPoints.append([sn.sprites[0].x, sn.sprites[0].y])
        sn.snake[0] = sn.direction['UP']
        sn.prev_dir.append(sn.snake[0])

    elif symbol == key.DOWN:
        if sn.snake[0] == sn.direction['UP'] or sn.snake[0] == sn.direction['DOWN']:
            return
        sn.turnPoints.append([sn.sprites[0].x, sn.sprites[0].y])
        sn.snake[0] = sn.direction['DOWN']
        sn.prev_dir.append(sn.snake[0])

    elif symbol == key.LEFT:
        if sn.snake[0] == sn.direction['RIGHT'] or sn.snake[0] == sn.direction['LEFT']:
            return
        sn.turnPoints.append([sn.sprites[0].x, sn.sprites[0].y])
        sn.snake[0] = sn.direction['LEFT']
        sn.prev_dir.append(sn.snake[0])

    elif symbol == key.RIGHT:
        if sn.snake[0] == sn.direction['LEFT'] or sn.snake[0] == sn.direction['RIGHT']:
            return
        sn.turnPoints.append([sn.sprites[0].x, sn.sprites[0].y])
        sn.snake[0] = sn.direction['RIGHT']
        sn.prev_dir.append(sn.snake[0])


@game_window.event
def on_draw():
    game_window.clear()
    sn.bg.blit(0, 0)
    score.draw()
    score_number.draw()
    sn.batch.draw()
    food_img.blit(food[0], food[1])


pyglet.clock.schedule_interval(update, SPEED)

for x in range(0, 7):
    sn.add_block()


pyglet.app.run()

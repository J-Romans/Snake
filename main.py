import pygame
from numpy import array, array_equal
from random import randint

##Defining Pygame window
pygame.init()
WIDTH, HEIGHT = 400,400
SCALE = 50
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

WHITE = (255,255,255)
RED = (255,0,0)


class Snake():
    def __init__(self, head_pos, length, colour):
        self.head_pos = array(head_pos)
        self.colour = colour
        self.direction = array([1,0])
        self.body_positions = [self.head_pos-array([length-i-1,0]) for i in range(length)]

    def eatenFruit(self):
        temp = self.body_positions[0]
        self.move()
        self.body_positions.insert(0,temp)
    
    def move(self):
        possible_move = self.head_pos + self.direction
        if possible_move[0]*SCALE < 0 or possible_move[0]*SCALE >= WIDTH or possible_move[1]*SCALE < 0 or possible_move[1]*SCALE >= HEIGHT:
            pygame.quit()
        if any(array_equal(segment, possible_move) for segment in self.body_positions):
            pygame.quit()
        self.head_pos += self.direction
        self.body_positions.append(array(self.head_pos))
        del self.body_positions[0]
    
    def draw(self):
        for segment in self.body_positions:
            pygame.draw.rect(win, WHITE,(segment[0]*SCALE+2, segment[1]*SCALE+2, SCALE-2,SCALE-2))

def generateFruit(board_size, snake):
    fruit_pos = [randint(0, board_size[0]-1),randint(0, board_size[1]-1)]
    while any(array_equal(fruit_pos, segment) for segment in snake.body_positions):
        fruit_pos = [randint(0, board_size[0]-1),randint(0, board_size[1]-1)]
    return fruit_pos

def drawFruit(pos):
    pygame.draw.rect(win, RED,(pos[0]*SCALE+2, pos[1]*SCALE+2, SCALE-2,SCALE-2))

def main():
    running = True
    clock = pygame.time.Clock()
    counter = 0 #Simulate 2 FPS
    snake = Snake((3,3), 3, WHITE)
    fruit_pos = generateFruit([WIDTH//SCALE, HEIGHT//SCALE], snake)
    while running:
        counter+=1
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()  
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if snake.direction[0] != -1:
                snake.direction[0] = 1
                snake.direction[1] = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if snake.direction[0] != 1:
                snake.direction[0] = -1
                snake.direction[1] = 0
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if snake.direction[1] != -1:
                snake.direction[0] = 0
                snake.direction[1] = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if snake.direction[1] != 1:
                snake.direction[0] = 0
                snake.direction[1] = -1


        if counter == 30:
            counter = 0
            win.fill((0,0,0))
            if any(array_equal(fruit_pos, segment) for segment in snake.body_positions):
                snake.eatenFruit()
                fruit_pos = generateFruit([WIDTH//SCALE, HEIGHT//SCALE], snake)
            else:
                snake.move()

            drawFruit(fruit_pos)
            snake.draw()
       

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
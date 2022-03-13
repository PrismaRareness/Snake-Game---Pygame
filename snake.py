from email import header
from random import randint, choice

import pygame


pygame.init()



class snake:
    collor = (255, 255, 255)
    size = (10, 10)
    velocity = 5
    size_max = 49 * 49
    
    def __init__(self):
        self.texture = pygame.Surface(self.size)
        self.texture.fill(self.collor)

        self.body = [(100, 100), (90, 100), (80, 100)]
        
        self.turn = "right"    
        
        self.score = 0    
                
    def blit(self, screen):    
        for position in self.body:
            screen.blit(self.texture, position)
            
#--------------------------------------------------------------            
#The snake is not actually "moving".
# What is happening is that I am "removing" the tail/head pixel
# and adding a new one 
#--------------------------------------------------------------       
    
    def step(self):
        
        head = self.body[0]
        x = head[0]
        y = head[1]        
        
        if self.turn == "right":
            self.body.insert(0, (x + self.velocity, y)) 
        elif self.turn == "left":
            self.body.insert(0, (x - self.velocity, y))
        elif self.turn == "up":
            self.body.insert(0, (x, y - self.velocity))
        elif self.turn == "down":
            self.body.insert(0, (x, y + self.velocity))                       

        self.body.pop(-1)

    
    def up(self):
        if self.turn != "down":
            self.turn = "up"

        
    def down(self):
        if self.turn != "up":
            self.turn = "down"

                
    def left(self):
        if self.turn != "right":    
            self.turn = "left"


    def right(self):
        if self.turn != "left":
            self.turn = "right"
    
            
    def fruit_collision(self, LITTLE_FRUIT):
        return self.body[0] == LITTLE_FRUIT.position
    
    
    def eat(self):
        self.body.append((0, 0))  
        self.score += 1
        pygame.display.set_caption("Snake | Score: {}".format(self.score))

                                     
    def restricted_collision(self):
        head = self.body[0]
        x = head[0]
        y = head[1]
        
        tail = self.body[1:]
        
        return x < 0 or y < 0 or x > 490 or y > 490 or head in tail or len(self.body) > self.size_max
            

class little_fruit:
    collor = (255, 0, 0)
    size = (10, 10)
    
    def __init__(self, SNAKE):
        self.texture = pygame.Surface(self.size)     
        self.texture.fill(self.collor)   

        self.position = little_fruit.create_position(SNAKE)
        
    @staticmethod
    def create_position(SNAKE):
        x = randint(0, 49) * 10
        y = randint(0, 49) * 10
        
        if (x, y) in SNAKE.body:
            little_fruit.create_position(SNAKE)
        else:
            return x, y    
        
    def blit(self, screen):    
        screen.blit(self.texture, self.position)
        

if __name__ == "__main__":
    pygame.init()    
    resolution = (500, 500)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    black = (0, 0, 0)    
    screen.fill(black)
                
    SNAKE = snake()
    
    LITTLE_FRUIT = little_fruit(SNAKE)
    LITTLE_FRUIT.blit(screen)

    
while True:
    clock.tick(30) #30 FPS
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                SNAKE.up()
                break
            if event.key == pygame.K_DOWN:
                SNAKE.down()
                break
            if event.key == pygame.K_LEFT:
                SNAKE.left()
                break
            if event.key == pygame.K_RIGHT:
                SNAKE.right()                                               
                break   

    if SNAKE.fruit_collision(LITTLE_FRUIT):
        SNAKE.eat() 
        LITTLE_FRUIT = little_fruit(SNAKE)
        
    elif SNAKE.restricted_collision():
        SNAKE = snake()    
    
    SNAKE.step() 
    
    screen.fill(black)
    LITTLE_FRUIT.blit(screen)
    SNAKE.blit(screen)        
        
     
    pygame.display.update()
    
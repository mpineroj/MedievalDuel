import pygame, sys, time
from pygame.locals import *
from functions import gameActive, gameover
import random

vec = pygame.math.Vector2  # 2 for 2d

pygame.font.init()

#VARIABLES
SCREENHEIGHT = 450
SCREENWIDTH = 800
ACC = 1
FRIC = -0.12
FPS = 30
playerHeight = 80
player_jump = 12
gravity = 1
tickCounter = 0
timeBetweenJabs = 30

FramePerSec = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
background = pygame.image.load('imgs/backround_img.png')
background = pygame.transform.scale(background, (SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Medieval Duel')


SLASH_SOUND = pygame.mixer.Sound('sfx/mixkit-metallic-sword-strike-2160.wav')
#SLASH_SOUND.set_volume(0.2)

       

#player class
class Player(pygame.sprite.Sprite):

  def __init__(self, image, facing, x, y, keys):
    super().__init__()
    self.image = pygame.image.load(image)
    self.image = pygame.transform.scale(self.image,
                                        (playerHeight, playerHeight))
    self.rect = self.image.get_rect(topleft=(x, y))
    self.pos = vec((x, y))
    self.vel = vec(0, 0)
    self.acc = vec(0, 0)
    self.facing = facing
    self.imgFlip = pygame.transform.flip(self.image, True, False)
    self.lastJab = 0
    self.keys = keys

    #HEALTH
    self.health = 200
    self.dead = False
    self.shieldState = False

    #GUI
    self.healthbar = pygame.image.load('imgs/health_bar.png')
    self.healthbar = pygame.transform.scale(
      self.healthbar, (.75 * self.healthbar.get_width(),
                       .75 * self.healthbar.get_height()))  #scales the image
    self.healthbar_ogx = self.healthbar.get_width()

    #ANIMATION

    #list of frames to animate the knight walking
    self.P2_sprites = [
      pygame.transform.scale(pygame.image.load('imgs/blue walk2.png'),
                             (playerHeight, playerHeight)),
      pygame.transform.scale(pygame.image.load('imgs/blue walk1.png'),
                             (playerHeight, playerHeight))
    ]


    self.P1_sprites = [
      pygame.transform.scale(pygame.image.load('imgs/red walk2.png'), (playerHeight, playerHeight)), pygame.transform.scale(pygame.image.load('imgs/red walk1.png'), (playerHeight, playerHeight))
    ]

    self.current_sprite = 0  #used to cycle through the list of frames for animation

  def animate(self, player, state):
    player.current_sprite += 0.3  #ANIMATION SPEED (cycles through sprite image list)
    if player == P2:

      if state == 'attack':
        player.image = pygame.transform.scale(pygame.image.load('imgs/blue attack.png'), (playerHeight, playerHeight))
      
      if state == 'standing':
        if player.facing == 1:
          player.image = pygame.transform.scale(
            pygame.image.load('imgs/blue stand.png'),
            (playerHeight, playerHeight))
        else:
          player.image = pygame.transform.scale(
            pygame.image.load('imgs/blue stand.png'),
            (playerHeight, playerHeight))
          player.image = pygame.transform.flip(player.image, True, False)

      
        
      else:
        if player.current_sprite >= len(self.P2_sprites):
    
          player.current_sprite = 0  #sets the index counter back to 0 if it gets bigger than the amount of frames in the frame listd
  
        elif self.dead:
          self.dead_animation()  #calls the dead animation if the player is dead
  
        else:
          #last step: determines which direction sprite is facing
          if player.facing == 1:
            player.image = player.P2_sprites[int(
              player.current_sprite
            )]  #sets the sprites image to the current frame of animation
          else:
            player.image = player.P2_sprites[int(self.current_sprite)]
            player.image = pygame.transform.flip(player.image, True, False)
  
    else:
      if state == 'attack':
        player.image = pygame.transform.scale(pygame.image.load('imgs/red attack.png'), (playerHeight, playerHeight))
      if state == 'standing':
        #decides which way to face while standing
        if player.facing == 1:
          player.image = pygame.transform.scale(
            pygame.image.load('imgs/red stand.png'),
            (playerHeight, playerHeight))
        else:
          player.image = pygame.transform.scale(
            pygame.image.load('imgs/red stand.png'),
            (playerHeight, playerHeight))
          player.image = pygame.transform.flip(player.image, True, False)
      
      else:
        if player.current_sprite >= len(self.P1_sprites):
    
          player.current_sprite = 0  #sets the index counter back to 0 if it gets bigger than the amount of frames in the frame listd
  
        elif self.dead:
          player.dead_animation()  #calls the dead animation if the player is dead
  
        else:
          #last step: determines which direction sprite is facing
          if player.facing == 1:
            player.image = player.P1_sprites[int(
              player.current_sprite
            )]  #sets the sprites image to the current frame of animation
          else:
            player.image = player.P1_sprites[int(self.current_sprite)]
            player.image = pygame.transform.flip(player.image, True, False)

      

  def jump(self):
    hits = pygame.sprite.spritecollide(self, platformsprite, False)
    if hits:
      self.vel.y = player_jump

  def move(self):
    self.acc = vec(0, gravity)
    # check movement for WASD
    if self.keys == 'wasd':

      #decide if there is input for movement or standing (for animation)
      inputs1 = pygame.key.get_pressed()
      if inputs1[pygame.K_a] == 1 or inputs1[pygame.K_d] == 1 or inputs1[
          pygame.K_w] == 1:
        #move left or right with momentum
        if pygame.key.get_pressed()[pygame.K_w]:
          self.jump()
        if pygame.key.get_pressed()[pygame.K_a]:
          self.facing = 0
          self.acc.x = -ACC
          self.animate(P2, 'walking')
        if pygame.key.get_pressed()[pygame.K_d]:
          self.facing = 1
          self.acc.x += ACC
          self.animate(P2, 'walking')
        if pygame.key.get_pressed()[pygame.K_s]:
          self.guard()
      else:
        self.animate(P2, 'standing')

    # check movement for arrow keys
    if self.keys == 'arrows':

      #decide if there is input for movement or standing (for animation)
      inputs2 = pygame.key.get_pressed()
      if inputs2[pygame.K_LEFT] == 1 or inputs2[pygame.K_RIGHT] == 1 or inputs2[pygame.K_UP] == 1:
        #move left or right with momentum
        if pygame.key.get_pressed()[pygame.K_LEFT]:
          self.facing = 0
          self.acc.x = -ACC
          self.animate(P1, 'walking')
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
          self.facing = 1
          self.acc.x += ACC
          self.animate(P1, 'walking')
        if pygame.key.get_pressed()[pygame.K_UP]:
          self.jump()
          self.animate(P1, 'walking')
        if pygame.key.get_pressed()[pygame.K_DOWN]:
          print(P1.state)
          print(P2.state)
          self.guard()
      else:
        self.animate(P1, 'standing')  

    #calculate accel / vel for momentum
    self.acc.x -= self.vel.x * FRIC
    self.vel -= self.acc
    self.pos -= self.vel + 0.5 * self.acc

    #ceiling and wall constraints
    if self.pos.x <= 0:
      self.vel.x = 0
      self.pos.x = 0
    elif self.pos.x >= SCREENWIDTH - 50:
      self.vel.x = 0
      self.pos.x = SCREENWIDTH - 50
    self.rect.topleft = self.pos

  def update(self):
    self.rect.topleft = self.pos
    hitsplat = pygame.sprite.spritecollide(self, platformsprite, False)
    if self.vel.y < 0:
      if hitsplat:
        self.vel.y = 0
        self.pos.y = hitsplat[0].rect.top + 1 - playerHeight

  # checks if the players colliding in the right place
  def playerCollision(self, otherInstance):
    if self.rect.colliderect(otherInstance):
      if self.facing == 0:
        if otherInstance.rect.left < self.rect.left < otherInstance.rect.right:
          print("Would be a hit left")
          #otherInstance.health subtract some bit
          otherInstance.health -= 20
          
      elif self.facing == 1:
        if otherInstance.rect.left < self.rect.right < otherInstance.rect.right:
          print("Would be a hit right")
          otherInstance.health -= 20
          #otherInstance.health subtract some bit

  # Checks 1. correct button pressed, 2. Enough time between jabs 3. If the characters are colliding
  def jabbing(self, otherInstance):
    if (self.keys == 'wasd' and pygame.key.get_pressed()[pygame.K_SPACE]) or (
        self.keys == 'arrows' and pygame.key.get_pressed()[pygame.K_m]):
      #change animation to jabbing
      if otherInstance == P1:
        P2.state = 'attack'
      else:
        P1.state = 'attack'
        
      if tickCounter - self.lastJab > timeBetweenJabs:
        self.lastJab = tickCounter
        self.playerCollision(otherInstance)
        
        print('jabbed')
        print(self, 'has', str(self.health))
        print(otherInstance, 'has', str(otherInstance.health))
  def guard(self):
      print('fee')
      hitsfplat = pygame.sprite.spritecollide(self, platformsprite, False)
      hitsplat = pygame.sprite.spritecollide(self, platformsprite, False)
      if self.vel.y < 0:
        print("foo")
        if hitsfplat or hitsplat:
          # load guarding animation
          print('fab')
      

  def display_healthbar(self, player):
    if player.health > 0:
      player.healthbar = pygame.transform.scale(
      player.healthbar, ((player.health / 200) * player.healthbar_ogx, player.healthbar.get_height()))

      #displays healthbar in different locations depending on player
      if player == P2:
        screen.blit(player.healthbar, ((SCREENWIDTH - 50.5) -
  (player.healthbar_ogx * player.health / 200), 24))
      else:
        screen.blit(player.healthbar, (53, 24))
    else:
      pass
    if self.health <= 0:
      self.dead = True


class platform(pygame.sprite.Sprite):

  def __init__(self):
    super().__init__()
    self.surf = pygame.Surface((SCREENWIDTH, 20))
    self.surf.fill((185, 65, 48))
    self.rect = self.surf.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT - 10))


class floatplatimage(pygame.sprite.Sprite):

  def __init__(self, image, xl, yl):
    super().__init__()
    self.image = pygame.image.load(image)
    self.image = pygame.transform.scale(self.image, (150, 20))
    self.surf = pygame.Surface((150, 20))
    self.surf.fill((167, 46, 37))
    self.rect = self.surf.get_rect(center=(xl, yl))
    screen.blit(self.image, self.rect)


class fplat(pygame.sprite.Sprite):

  def __init__(self, xl, yl):
    super().__init__()
    self.surf = pygame.Surface((150, 1))
    self.surf.fill((0, 255, 25))
    self.rect = self.surf.get_rect(center=(xl, yl))
    screen.blit(self.surf, self.rect)

class Button(
        pygame.sprite.Sprite
):  #takes care of all the buttons in the program (even if they aren't supposed to be pressed)

    def __init__(self, image_path, pos_x, pos_y, scale):
        super().__init__()
        self.image = pygame.image.load(image_path)
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(
            self.image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.clicked = False

    def draw(self):
        pos = pygame.mouse.get_pos()
        action = False

        if self.rect.collidepoint(
                pos):  #checks to see if the cursor is on the button
            #print("hover")

            if pygame.mouse.get_pressed(
            )[0] and not self.clicked:  #self.clicked makes sure you can't just hold down the mouse button
                #print("clicked")
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action  #boolean for executing an action after the button is pressed

#INSTANCES
  
RP1 = fplat(200, 140)
RP2 = fplat(400, 240)
RP3 = fplat(600, 340)

P1 = Player('imgs/red stand.png', 1, 100, 300, 'arrows')
P2 = Player('imgs/blue stand.png', 0, 400, 300, 'wasd')
PT1 = platform()
i1 = floatplatimage("imgs/platbrick.jpg", 200, 150)
i2 = floatplatimage("imgs/platbrick.jpg", 400, 250)
i3 = floatplatimage("imgs/platbrick.jpg", 600, 350)

p2_healthbar = Button('imgs/p1_empty_healthbar.png', 180, 30, .75)
p1_healthbar = Button('imgs/p2_empty_healthbar.png', SCREENWIDTH - 180, 30, .75)

allPlayers = pygame.sprite.Group()
allPlayers.add(P1)
allPlayers.add(P2)

platformsprite = pygame.sprite.Group()
platformsprite.add(PT1)

fplatsprite = pygame.sprite.Group()
fplatsprite.add(i1)
fplatsprite.add(i2)
fplatsprite.add(i3)

platformsprite.add(RP1)
platformsprite.add(RP2)
platformsprite.add(RP3)

GUI_group = pygame.sprite.Group()
GUI_group.add(p1_healthbar)
GUI_group.add(p2_healthbar)

gameRunning = True
#Game Loop
if gameRunning:
  pygame.mixer.music.load('powerman.wav')
  pygame.mixer.music.play(-1)  

while gameRunning:
  screen.blit(background, (0, 0))
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

  if not P1.dead and not P2.dead:
    gameActive(platformsprite, fplatsprite, screen, P1, P2, allPlayers, GUI_group)
  elif P1.dead:
    gameover("Player 2", SCREENWIDTH, SCREENHEIGHT, screen)
  elif P2.dead:
    gameover("Player 1", SCREENWIDTH, SCREENHEIGHT, screen)
  else:
    pass
    
  
  
  tickCounter += 1
  FramePerSec.tick(FPS)

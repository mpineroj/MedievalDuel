import pygame, sys, time
from pygame.locals import QUIT

pygame.font.init()


def gameActive(platformsprite, fplatsprite, screen, P1, P2, allPlayers, GUI_group):
  for entity in platformsprite:
    screen.blit(entity.surf, entity.rect)
  for entity in fplatsprite:
    screen.blit(entity.image, entity.rect)
  allPlayers.draw(screen)
  
  P1.move()
  P2.move()
  
  P1.update()
  P2.update()
  
  P1.jabbing(P2)
  P2.jabbing(P1)
  
  GUI_group.draw(screen)

  P1.display_healthbar(P2)
  P2.display_healthbar(P1)

  pygame.display.update()


def gameover(player, X, Y, screen):
  font = pygame.font.SysFont('Comic Sans MS', 300)
  text = font.render(f"{player} wins!", False, (0, 0, 0))
  textRect = text.get_rect()
  textRect.center = (X // 2, Y // 2)
  screen.blit(text, textRect)
  
import pygame
import time

pygame.init()

surface = pygame.display.set_mode((400,300))

color = (255, 255, 0)

pygame.draw.rect(surface, color, pygame.Rect(30,30, 60,60))




pygame.display.flip()
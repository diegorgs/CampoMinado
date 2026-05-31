import pygame

pygame.mixer.init()

som_click = pygame.mixer.Sound("assets/sons/click.wav")
som_mina = pygame.mixer.Sound("assets/sons/mina.wav")
som_vitoria = pygame.mixer.Sound("assets/sons/vitoria.wav")
som_flag = pygame.mixer.Sound("assets/sons/flag.wav")


som_click.set_volume(0.2)
som_mina.set_volume(0.3)
som_vitoria.set_volume(0.5)
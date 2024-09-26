# HW3
# GamingMike45
# Python, Pygame
# 9/18/2024

import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Michael Game')
        self.screen = pygame.display.set_mode((640, 480))

        self.clock = pygame.time.Clock()

        # Load images for the character and growth stages
        self.img = pygame.image.load('data/images/player/character_walking_front.png')
        self.img.set_colorkey((0, 0, 0))

        # Load and resize watering can image
        self.watering_can_image = pygame.image.load('data/images/watering_can.png')  # Path to your watering can image
        self.watering_can_image = pygame.transform.scale(self.watering_can_image, (50, 50))  # Resize to 50x50
        self.watering_can_rect = self.watering_can_image.get_rect()

        self.img_pos = [160, 260]
        self.movement = [False, False, False, False]

        # Define collision areas
        self.collision_areas = [
            pygame.Rect(50, 350, 50, 50),
            pygame.Rect(110, 350, 50, 50),
            pygame.Rect(170, 350, 50, 50), 
            pygame.Rect(230, 350, 50, 50)
        ]

        # Plant status and growth stage
        self.planted = [False, False, False, False]
        self.growth_stage = [0, 0, 0, 0]  # 0: seeds, 1: sprouts, 2: grown
        self.growth_timer = [0, 0, 0, 0]  # Timer for each plot

        self.growth_time = 200  # Time to grow (in frames)
        self.just_harvested = [False, False, False, False]  # Tracks recently harvested plots

        self.farm_house_image = pygame.image.load('data/maps/farm_house.png')
        self.farm_house_image = pygame.transform.scale(self.farm_house_image, (300, 300))
        self.river = pygame.image.load('data/maps/river.png')
        self.river = pygame.transform.scale(self.river, (100 ,100))

        

    def run(self):
        while True:
            self.screen.fill((100, 255, 100))
            self.screen.blit(self.farm_house_image, (300, 110))
            self.screen.blit(self.river, (0, 100)) 
            pygame.draw.rect(self.screen, (0, 0, 255), (0, 200, 100, 100))           

            # Get mouse position for watering can
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.watering_can_rect.topleft = (mouse_x, mouse_y)

            img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())

            for i, area in enumerate(self.collision_areas):
                pygame.draw.rect(self.screen, (150, 75, 0), area)  # Brown plot    
                
                if img_r.colliderect(area):
                    if self.planted[i]:
                        if self.growth_stage[i] == 2:   # Harvest the crop and revert the plot to empty when passing over grown crops
                            self.planted[i] = False
                            self.growth_stage[i] = 0
                            self.growth_timer[i] = 0
                            self.just_harvested[i] = True

                    else:   # Automatically plant when the player passes over an empty plot
                        if not self.just_harvested[i]:
                            self.planted[i] = True
                            self.growth_stage[i] = 0  # Set growth stage to seeds
                            self.growth_timer[i] = 0  # Reset growth timer

                else:   # If the player has left a harvested plot, it's ready for planting again
                    self.just_harvested[i] = False

                # If planted, handle growth
                if self.planted[i]:
                    if area.collidepoint(mouse_x, mouse_y): # Mouse is over the plot; grow the plant
                        self.growth_timer[i] += 1
                        if self.growth_timer[i] >= self.growth_time:
                            if self.growth_stage[i] < 2:  # Move to the next stage
                                self.growth_stage[i] += 1
                                self.growth_timer[i] = 0  # Reset timer for next growth stage

                # Draw based on the growth stage
                if self.planted[i]:
                    # Small green square for seed stage
                    if self.growth_stage[i] == 0:
                        seed_rect = pygame.Rect(    # Small square in the center
                            area.centerx - 5, area.centery - 5, 10, 10
                        )
                        pygame.draw.rect(self.screen, (0, 255, 0), seed_rect)

                    # Medium green square for sprout stage
                    elif self.growth_stage[i] == 1: 
                        sprout_rect = pygame.Rect(  # Medium square
                            area.centerx - 10, area.centery - 10, 20, 20
                        )
                        pygame.draw.rect(self.screen, (0, 255, 0), sprout_rect) 

                    # Full dark green square for grown stage
                    elif self.growth_stage[i] == 2:
                        grown_rect = pygame.Rect(
                            area.centerx - 25, area.centery - 25, 50, 50
                        )  # Full grown crop size
                        pygame.draw.rect(self.screen, (0, 100, 0), grown_rect)

            # Movement
            self.img_pos[0] += (self.movement[3] - self.movement[2]) * 5
            self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5

            self.screen.blit(self.img, self.img_pos)
            self.screen.blit(self.watering_can_image, self.watering_can_rect.topleft)  # Draw the watering can

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:  # Up
                        self.movement[0] = True
                    if event.key == pygame.K_s:  # Down
                        self.movement[1] = True
                    if event.key == pygame.K_a:  # Left
                        self.movement[2] = True
                    if event.key == pygame.K_d:  # Right
                        self.movement[3] = True
                        


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:  # Up
                        self.movement[0] = False
                    if event.key == pygame.K_s:  # Down
                        self.movement[1] = False
                    if event.key == pygame.K_a:  # Left
                        self.movement[2] = False
                    if event.key == pygame.K_d:  # Right
                        self.movement[3] = False

            pygame.display.update()
            self.clock.tick(60)

Game().run()


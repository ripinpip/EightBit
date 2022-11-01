import gc
import math

import pygame
import random
from pygame import KEYDOWN, K_ESCAPE, K_w, K_a, K_s, K_d, K_q, RLEACCEL, K_r, K_e, K_BACKSPACE, K_z, K_c, K_TAB, K_LCTRL

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

spriteImages = ["sprites/apple.png", "sprites/heart.png", "sprites/icecream.png", "sprites/money.png", "sprites/music"
                                                                                                       ".png"]

appleImage = pygame.image.load("sprites/apple.png")
newAppleImage = pygame.Surface(appleImage.get_size(), 0, screen)
newAppleImage.blit(appleImage, (0, 0))
newAppleImage.set_colorkey((0, 0, 0), RLEACCEL)
appleImage = newAppleImage
appleSmallImage = pygame.transform.scale(appleImage, (300, 300))
del newAppleImage, appleImage

heartImage = pygame.image.load("sprites/heart.png")
newHeartImage = pygame.Surface(heartImage.get_size(), 0, screen)
newHeartImage.blit(heartImage, (0, 0))
newHeartImage.set_colorkey((0, 0, 0), RLEACCEL)
heartImage = newHeartImage
heartSmallImage = pygame.transform.scale(heartImage, (300, 300))
del newHeartImage, heartImage

icecreamImage = pygame.image.load("sprites/icecream.png")
newIcecreamImage = pygame.Surface(icecreamImage.get_size(), 0, screen)
newIcecreamImage.blit(icecreamImage, (0, 0))
newIcecreamImage.set_colorkey((0, 0, 0), RLEACCEL)
icecreamImage = newIcecreamImage
icecreamSmallImage = pygame.transform.scale(icecreamImage, (400, 400))
del newIcecreamImage, icecreamImage

moneyImage = pygame.image.load("sprites/money.png")
newMoneyImage = pygame.Surface(moneyImage.get_size(), 0, screen)
newMoneyImage.blit(moneyImage, (0, 0))
newMoneyImage.set_colorkey((0, 0, 0), RLEACCEL)
moneyImage = newMoneyImage
moneySmallImage = pygame.transform.scale(moneyImage, (400, 400))
del newMoneyImage, moneyImage

musicImage = pygame.image.load("sprites/music.png")
newMusicImage = pygame.Surface(musicImage.get_size(), 0, screen)
newMusicImage.blit(musicImage, (0, 0))
newMusicImage.set_colorkey((0, 0, 0), RLEACCEL)
musicImage = newMusicImage
musicSmallImage = pygame.transform.scale(musicImage, (400, 400))
del newMusicImage, musicImage

# Prepare cache of rotated images
appleSmallImages = {0: appleSmallImage}
appleSmallRect = appleSmallImage.get_rect()

heartSmallImages = {0: heartSmallImage}
heartSmallRect = heartSmallImage.get_rect()

icecreamSmallImages = {0: icecreamSmallImage}
icecreamSmallRect = icecreamSmallImage.get_rect()

moneySmallImages = {0: moneySmallImage}
moneySmallRect = moneySmallImage.get_rect()

musicSmallImages = {0: musicSmallImage}
musicSmallRect = musicSmallImage.get_rect()

for angle in range(1, 360):
    appleSmallImages[angle] = pygame.transform.rotate(appleSmallImage, angle)

    heartSmallImages[angle] = pygame.transform.rotate(heartSmallImage, angle)

    icecreamSmallImages[angle] = pygame.transform.rotate(icecreamSmallImage, angle)

    moneySmallImages[angle] = pygame.transform.rotate(moneySmallImage, angle)

    musicSmallImages[angle] = pygame.transform.rotate(musicSmallImage, angle)


class Icon(pygame.sprite.Sprite):

    def autoMode(self):
        self.rect.center = calculateNewXY(self.rect.center[0], self.rect.center[1], self.speed, self.direction)

        self.angle = (self.angle + self.rotationSpeed) % 360.0
        try:
            self.image = pygame.transform.scale(self.images[int(self.angle)], (self.width, self.height))
        except KeyError:
            pass

    def updatePos(self, key):

        if key[K_w]:
            self.rect.move_ip(0, -self.speed)

        if key[K_s]:
            self.rect.move_ip(0, self.speed)

        if key[K_a]:
            self.rect.move_ip(-self.speed, 0)

        if key[K_d]:
            self.rect.move_ip(self.speed, 0)

        if key[K_z]:
            self.angle = (self.angle + self.rotationSpeed) % 360.0
            try:
                self.image = pygame.transform.scale(self.images[int(self.angle)], (self.width, self.height))
            except KeyError:
                pass

        if key[K_c]:
            self.angle = (self.angle - self.rotationSpeed) % 360.0
            try:
                self.image = pygame.transform.scale(self.images[int(self.angle)], (self.width, self.height))
            except KeyError:
                pass

    def __init__(self):
        super(Icon, self).__init__()
        self.angle = random.randint(1, 359)

        imagesOptions = [appleSmallImages, heartSmallImages, icecreamSmallImages, moneySmallImages, musicSmallImages]
        self.images = imagesOptions[random.randint(0, 4)]
        self.surf = self.images[self.angle]

        self.width = random.randint(int(getWindowSize()[1] / 4), int(getWindowSize()[1] / 3))
        self.height = self.width

        self.scaled = pygame.transform.scale(self.surf, (self.width, self.height))
        self.image = self.scaled

        # sets the transparency of a color
        self.scaled.set_colorkey((0, 0, 0), RLEACCEL)

        self.rect = self.scaled.get_rect(
            center=(
                random.randint(0, getWindowSize()[0]),
                random.randint(0, getWindowSize()[1]),
            )
        )

        self.speed = random.randint(1, 2)

        rotationalSpeedOptions = [0.2, 0.3, 0.4, 0.5, 0.6]
        self.rotationSpeed = rotationalSpeedOptions[random.randint(0, 4)]

        self.direction = random.randint(1, 360) * 180 / math.pi


class InstructionsSprite(pygame.sprite.Sprite):

    def __init__(self):
        super(InstructionsSprite, self).__init__()

        self.image = pygame.image.load("sprites/controls.png").convert()

        self.width = 494
        self.height = 590

        self.scaled = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = self.scaled

        # sets the transparency of a color
        self.scaled.set_colorkey((0, 0, 0), RLEACCEL)

        self.rect = self.scaled.get_rect(
            bottomleft=(
                screen.get_rect().bottomleft
            )
        )


def getWindowSize():
    (width, height) = pygame.display.get_surface().get_size()
    return width, height


def calculateNewXY(x, y, speed, angleInRads):
    newX = x + (speed * math.cos(angleInRads))
    newY = y + (speed * math.sin(angleInRads))
    return newX, newY


allSprites = pygame.sprite.Group()

running = True
dragMode = False
autoMode = False
instructions = True

instructionsSprite = InstructionsSprite()

pygame.init()

pygame.time.set_timer(pygame.USEREVENT, 250)
clock = pygame.time.Clock()

# where game starts running
while running:

    gc.disable()

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            # ESC quits the program
            if event.key == K_ESCAPE:
                running = False

            # q creates a new sprite
            if event.key == K_q:
                if len(allSprites) > 25:
                    allSprites.remove(allSprites.sprites()[0])

                newSprite = Icon()
                allSprites.add(newSprite)

            # e removes the last sprite
            if event.key == K_e:
                if len(allSprites) >= 1:
                    allSprites.remove(allSprites.sprites()[len(allSprites) - 1])

            # backspace deletes all the sprites
            if event.key == K_BACKSPACE:
                if len(allSprites) >= 1:
                    for entity in allSprites:
                        allSprites.remove(entity)

            # r turns on drag mode
            if event.key == K_r:
                screen.fill((0, 0, 0))
                for entity in allSprites:
                    screen.blit(entity.image, entity.rect)

                pygame.display.flip()

                if dragMode:
                    dragMode = False
                else:
                    dragMode = True

            # TAB turns on auto mode
            if event.key == K_TAB:

                if autoMode:
                    autoMode = False
                else:
                    autoMode = True

            # L CTRL turns on the instructions
            if event.key == K_LCTRL:

                if instructions:
                    instructions = False
                else:
                    instructions = True

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if autoMode:
                if len(allSprites) > 25:
                    allSprites.remove(allSprites.sprites()[0])

                newSprite = Icon()
                allSprites.add(newSprite)

    if not dragMode:
        screen.fill((0, 0, 0))

    if autoMode:
        for entity in allSprites:
            entity.autoMode()
            screen.blit(entity.image, entity.rect)
    else:
        pressed_keys = pygame.key.get_pressed()

        for entity in allSprites:
            entity.updatePos(pressed_keys)
            screen.blit(entity.image, entity.rect)

    if instructions:
        screen.blit(instructionsSprite.image, instructionsSprite.rect)
    else:
        instructionsSprite.kill()

    pygame.display.flip()

    gc.collect()
    clock.tick(60)

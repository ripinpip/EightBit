import pygame
import random
from pygame import KEYDOWN, K_ESCAPE, K_w, K_a, K_s, K_d, K_q, RLEACCEL, K_r, K_e, K_BACKSPACE, K_z, K_c

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

spriteImages = ["sprites/apple.png", "sprites/heart.png", "sprites/icecream.png", "sprites/money.png", "sprites/music"
                                                                                                       ".png"]

appleImage = pygame.image.load("sprites/apple.png")
newAppleImage = pygame.Surface(appleImage.get_size(), 0, screen)
newAppleImage.blit(appleImage, (0, 0))
newAppleImage.set_colorkey((0, 0, 0), RLEACCEL)
appleImage = newAppleImage
del newAppleImage

# Prepare cache of rotated images
appleImages = {0: appleImage}
appleRect = appleImage.get_rect()

for angle in range(1, 360):

    rotatedAppleImage = pygame.transform.rotate(appleImage, angle)
    rotatedAppleRect = rotatedAppleImage.get_rect()

    if rotatedAppleRect == appleRect:

        rotatedAppleImage.set_colorkey((0, 0, 0), RLEACCEL)
        appleImages[angle] = rotatedAppleImage

    else:

        # trim any new transparent pixels around the edges

        newAppleRotatedImage = pygame.Surface(appleRect.size, 0, screen)

        offsetAppleX = (appleRect.width - rotatedAppleRect.width) // 2
        offsetAppleY = (appleRect.height - rotatedAppleRect.height) // 2
        newAppleRotatedImage.blit(rotatedAppleImage, (offsetAppleX, offsetAppleY))

        newAppleRotatedImage.set_colorkey((0, 0, 0), RLEACCEL)
        appleImages[angle] = newAppleRotatedImage

        del newAppleRotatedImage, offsetAppleX, offsetAppleY

del rotatedAppleImage, rotatedAppleRect


class Icon(pygame.sprite.Sprite):
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
            self.image = self.images[int(self.angle)]

        if key[K_c]:
            self.angle = (self.angle - self.rotationSpeed) % 360.0
            self.image = self.images[int(self.angle)]

    def __init__(self):
        super(Icon, self).__init__()
        # self.surf = pygame.image.load(spriteImages[random.randint(0, 4)]).convert()
        self.angle = random.randint(1, 360)

        self.images = appleImages
        self.surf = self.images[round(self.angle)]

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

        rotationalSpeedOptions = [0.1, 0.2, 0.3, 0.4, 0.5]
        self.rotationSpeed = rotationalSpeedOptions[random.randint(0, 4)]


def getWindowSize():
    (width, height) = pygame.display.get_surface().get_size()
    return width, height


allSprites = pygame.sprite.Group()

running = True
dragMode = False

# where game starts running
while running:

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            # ESC quits the program
            if event.key == K_ESCAPE:
                running = False

            # q creates a new sprite
            if event.key == K_q:
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
                    screen.blit(entity.scaled, entity.rect)

                pygame.display.flip()

                if dragMode:
                    dragMode = False
                else:
                    dragMode = True

        if event.type == pygame.QUIT:
            running = False

    if not dragMode:
        screen.fill((0, 0, 0))

    pressed_keys = pygame.key.get_pressed()

    for entity in allSprites:
        entity.updatePos(pressed_keys)
        screen.blit(entity.image, entity.rect)

    pygame.display.flip()

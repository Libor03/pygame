import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE
)



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
text = "Asfasfasf"
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.image.load ("images/jet.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_down_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left <0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <=0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/missile.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center =(
                random.randint (SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint (0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5,20)

    def update(self):
        if pygame.sprite.spritecollideany(player, powerups):
            self.kill()
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super(Powerup, self).__init__()
        self.surf = pygame.image.load("images/pow_pow_power_rangers.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center =(
                random.randint (SCREEN_WIDTH + 30, SCREEN_WIDTH + 30),
                random.randint (0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5,20)

    def update(self):
        if self.rect.right < 0:
            self.kill()
        if pygame.sprite.spritecollideany(player, powerups):
            self.kill()
        self.rect.move_ip(-self.speed, 0)




class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH +100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5,0)
        if self.rect.right <0:
            self.kill()

class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color):
        super(Text, self).__init__()
        self.color = color
        self.font = pygame.font.SysFont("Arial", size)
        self.surf = self.font.render(text, 1, self.color)
        self.rect = self.surf.get_rect()

    def update(self, text):
        self.surf = self.font.render(text, 1, self.color)


pygame.mixer.init()

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
ADDPOWERUP = pygame.USEREVENT + 3
pygame.time.set_timer(ADDPOWERUP, 5000)

player = Player()
powerupp = Powerup()
enemy = Enemy()
text = Text("asdasd", 30, "white")

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
powerups = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy, powerupp)

pygame.mixer.music.load("sound/Sky_dodge_theme.ogg")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.1)

move_up_sound = pygame.mixer.Sound("sound/Jet_up.ogg")
move_down_sound = pygame.mixer.Sound("sound/Jet_down.ogg")
collision_sound = pygame.mixer.Sound("sound/Boom.ogg")
move_up_sound.set_volume(0.1)
move_down_sound.set_volume(0.1)
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:

            print((f"{event.key}"))
            if event.key == K_ESCAPE:
                running = False


        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        elif event.type == ADDPOWERUP:
            new_powerup = Powerup()
            powerups.add(new_powerup)
            all_sprites.add(new_powerup)


    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    clouds.update()
    powerups.update()
    text.update("asdasd")
    screen.fill((135,203,250))
    surf = pygame.Surface((20,20))
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        move_down_sound.stop()
        move_up_sound.stop()
        pygame.mixer.music.stop()
        pygame.time.delay(50)
        collision_sound.play()
        pygame.time.delay(500)
        running = False
    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.mixer.quit()

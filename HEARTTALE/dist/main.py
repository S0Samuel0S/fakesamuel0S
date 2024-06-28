import pygame
import settings as s
import random

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
pygame.display.set_caption('HEARTTALE')
bg_sound = "bg_sound.wav"
endvoice = "Dievoice.wav"
scsound = "win_voice.wav"
hitsound = "hit.wav"
Sans = pygame.image.load("sans.png")
player_img = pygame.image.load("heart.png")
player_img = pygame.transform.scale(player_img, (30, 30))
Sans = pygame.transform.scale(Sans, (200, 200))


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        screen.blit(player_img, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_UP] and self.y > 100:
            self.y -= 5
        if keys[pygame.K_DOWN] and self.y < 370:
            self.y += 5
        if keys[pygame.K_RIGHT] and self.x < 370:
            self.x += 5
        if keys[pygame.K_LEFT] and self.x > 100:
            self.x -= 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Bone:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 5

    def draw(self, screen):
        pygame.draw.rect(screen, s.WHITE, (self.x, self.y, self.width, self.height))


    def move(self):
        self.y -= self.speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


bones = []
gravity_timer = 0
player = Player(200, 200, 30, 30)


def gravityATK():
    global s
    dirn = random.randint(1, 4)
    if dirn == 1:
        if player.x < 370:
            player.x += 10
        else:
            s.p_HP -= 2
    if dirn == 2:
        if player.x > 100:
            player.x -= 10
        else:
            s.p_HP -= 2
    if dirn == 3:
        if player.y > 370:
            player.y += 10
        else:
            s.p_HP -= 2
    if dirn == 4:
        if player.y > 100:
            player.y -= 10
        else:
            s.p_HP -= 2


def main():
    global bones, gravity_timer, player
    win_timer = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    pygame.mixer.music.load(hitsound)
    pygame.mixer.music.load(endvoice)
    pygame.mixer.music.load(bg_sound)

    pygame.mixer.music.play(-1)
    run = True
    while run:
        pygame.time.delay(15)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

        if s.p_HP < 1:
            screen.fill(s.BLACK)
            pygame.display.update()
            pygame.mixer.music.stop()
            pygame.mixer.Sound(endvoice).play()

            pygame.time.delay(3000)
            run = False
            break
        if pygame.time.get_ticks() - win_timer > 150000:
            screen.fill(s.RED)
            pygame.display.update()
            pygame.mixer.music.stop()
            pygame.mixer.Sound(scsound).play()
            pygame.time.delay(27000)
            run = False
            pygame.quit()
            break

        screen.fill(s.BLACK)
        screen.blit(Sans, (150, 400))
        pygame.draw.line(screen, s.WHITE, (400, 400), (400, 100), 5)
        pygame.draw.line(screen, s.WHITE, (100, 400), (400, 400), 5)
        pygame.draw.line(screen, s.WHITE, (100, 100), (100, 400), 5)
        pygame.draw.line(screen, s.WHITE, (100, 100), (400, 100), 5)

        player.move(keys)
        player.draw(screen)

        
        if current_time - gravity_timer > 1000:
            gravityATK()
            gravity_timer = current_time

        pygame.draw.rect(screen, s.RED, (10, 10, 100, 20))
        pygame.draw.rect(screen, s.GREEN, (10, 10, s.p_HP, 20))

        text = s.font.render('HP: ' + str(s.p_HP), True, s.WHITE)
        screen.blit(text, (10, 40))

        if random.randint(0, 1000) < 50:
            x = random.randint(-50, 600)
            new_bone = Bone(x, 700, 300, 10)
            bones.append(new_bone)

        for b in bones:
            b.move()
            b.draw(screen)
            if b.rect.colliderect(player.rect):
                s.p_HP -= 1
                pygame.mixer.Sound(hitsound).play
                pygame.time.delay(1)
            if b.y < 0:
                bones.remove(b)

        
        pygame.display.update()


main()



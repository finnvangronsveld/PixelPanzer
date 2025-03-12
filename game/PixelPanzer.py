import pygame
import math
import os
import sys
import time

# Pad naar de assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

# Initialiseer pygame
pygame.init()
pygame.mixer.init()

# Laad de achtergrondmuziek en menu achtergrond
pygame.mixer.music.load(os.path.join(ASSETS_DIR, "MainMenu.wav"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Constanten
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
DARK_GRAY = (50, 50, 50)
TANK_WIDTH, TANK_HEIGHT = 50, 50
BULLET_RADIUS = 5
BULLET_SPEED = 5
SHOOT_COOLDOWN = 500
MAX_BULLETS = 5
GAME_OVER_FONT = pygame.font.Font(None, 74)
BUTTON_FONT = pygame.font.Font(None, 50)

# Zet het scherm op full-screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()  # Verkrijg de schermgrootte na het instellen op full-screen
pygame.display.set_caption("PixelPanzer - Main Menu")

# Laad de achtergrond
background = pygame.image.load(os.path.join(ASSETS_DIR, "MenuBackground.png"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Fonts
font = pygame.font.Font(None, 35)

# Laad assets voor het spel
BLUE_TANK_IMAGE = pygame.image.load(os.path.join(ASSETS_DIR, "blue_tank.png"))
RED_TANK_IMAGE = pygame.image.load(os.path.join(ASSETS_DIR, "red_tank.png"))
BACKGROUND_IMAGE = pygame.image.load(os.path.join(ASSETS_DIR, "background.png"))
OBSTACLE_IMAGE = pygame.image.load(os.path.join(ASSETS_DIR, "steen2.png"))
OBSTACLE_IMAGE = pygame.transform.scale(OBSTACLE_IMAGE, (120, 60))

BLUE_BULLET_IMAGE = pygame.image.load(os.path.join(ASSETS_DIR, "blue_raket.png"))
RED_BULLET_IMAGE = pygame.image.load(os.path.join(ASSETS_DIR, "red_raket.png"))
BLUE_BULLET_IMAGE = pygame.transform.rotate(BLUE_BULLET_IMAGE, 180)
BLUE_BULLET_IMAGE = pygame.transform.scale(BLUE_BULLET_IMAGE, (30, 15))
RED_BULLET_IMAGE = pygame.transform.scale(RED_BULLET_IMAGE, (30, 15))

TANK_WIDTH, TANK_HEIGHT = 50, 50
BLUE_TANK_IMAGE = pygame.transform.scale(BLUE_TANK_IMAGE, (TANK_WIDTH, TANK_HEIGHT))
RED_TANK_IMAGE = pygame.transform.scale(RED_TANK_IMAGE, (TANK_WIDTH, TANK_HEIGHT))


# Laad en speel achtergrond muziek af voor het spel
pygame.mixer.music.load(os.path.join(ASSETS_DIR, "main.wav"))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0)

# Laad geluiden
ENGINE_SOUND = os.path.join(ASSETS_DIR, "engine.wav")
BIG_EXPLOSION_SOUND = os.path.join(ASSETS_DIR, "big_explosion.wav")
SMALL_EXPLOSION_SOUND = os.path.join(ASSETS_DIR, "small_explosion.wav")
engine_sound = pygame.mixer.Sound(ENGINE_SOUND)
engine_sound.set_volume(0.7)
big_explosion_sound = pygame.mixer.Sound(BIG_EXPLOSION_SOUND)
big_explosion_sound.set_volume(0.7)
small_explosion_sound = pygame.mixer.Sound(SMALL_EXPLOSION_SOUND)
small_explosion_sound.set_volume(1.2)

# Upgrade eigenschappen
UPGRADE_ZONE = pygame.Rect(900, 600, 100, 100)  # Positie van de upgrade-zone
UPGRADE_SPEED = 6  # Verhoogde snelheid
UPGRADE_SHOOT_COOLDOWN = 250  # Snellere schietfrequentie
UPGRADE_DURATION = 15000  # Upgrade duurt 5 seconden
TIMER_DURATION = 15000  # Timer van 15 seconden

# easter egg eigenschappen
EASTER_EGG_ZONE = pygame.Rect(400, 300, 50, 50)  # Verborgen rechthoek voor easter egg (locatie en grootte)

# Laad de geluidsbestanden
MAIN_MUSIC = "assets/main.wav"  # Zorg ervoor dat je het juiste pad naar het bestand gebruikt
EASTER_EGG_MUSIC = "assets/mainmenu.wav"  # Zorg ervoor dat je het juiste pad naar het bestand gebruikt

pygame.mixer.music.load(MAIN_MUSIC)  # Laad de hoofd muziek
pygame.mixer.music.play(-1)  # Speel de hoofd muziek af in een lus

# Laad de easter egg geluid
easter_egg_sound = pygame.mixer.Sound(EASTER_EGG_MUSIC)

def draw_button(text, color, rect):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, DARK_GRAY, rect, 3)  # Border
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (rect.x + 20, rect.y + 10))

def info_screen():
    running = True
    while running:
        screen.fill(DARK_GRAY)
        title_text = GAME_OVER_FONT.render("Game Information", True, (255, 255, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 6))

        # Information about the game
        info_text1 = font.render("PixelPanzer is a tank battle game where two players", True, WHITE)
        info_text2 = font.render("control tanks and try to destroy each other!", True, WHITE)
        info_text3 = font.render("The goal is to hit the opponent's tank 3 times.", True, WHITE)
        info_text4 = font.render("Use WASD to move and SPACE to shoot.", True, WHITE)
        info_text5 = font.render("Use arrow keys to move and ENTER to shoot.", True, WHITE)

        # Positioning the info texts
        screen.blit(info_text1, (WIDTH // 2 - info_text1.get_width() // 2, HEIGHT // 4))
        screen.blit(info_text2, (WIDTH // 2 - info_text2.get_width() // 2, HEIGHT // 4 + 40))
        screen.blit(info_text3, (WIDTH // 2 - info_text3.get_width() // 2, HEIGHT // 4 + 80))
        screen.blit(info_text4, (WIDTH // 2 - info_text4.get_width() // 2, HEIGHT // 4 + 120))
        screen.blit(info_text5, (WIDTH // 2 - info_text5.get_width() // 2, HEIGHT // 4 + 160))

        # Bereken de nieuwe x-positie voor het centreren van de knop
        back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)  # 200 is de breedte van de knop
        draw_button("Back to Menu", GREEN, back_button)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    main_menu()  # Return to the main menu
                    running = False  # Stop the info screen


# Laad assets en begin instellingen zoals eerder

def draw_slider(x, y, width, height, value):
    """
    Teken een mooiere slider op het scherm met afgeronde hoeken en een schaduw.
    """
    # Teken de achtergrond van de slider (met een lichte schaduw)
    shadow_offset = 5
    pygame.draw.rect(screen, (50, 50, 50), (x + shadow_offset, y + shadow_offset, width, height), border_radius=10)  # Schaduw
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), border_radius=10)  # Slider base

    # Teken de volumeknop (met afgeronde hoeken)
    pygame.draw.rect(screen, GREEN, (x + value * (width - 20), y - 5, 20, height + 10), border_radius=5)  # Slider knob

def main_menu():
    pygame.mixer.music.load(os.path.join(ASSETS_DIR, "MainMenu.wav"))  # Laad de menu muziek
    pygame.mixer.music.set_volume(0.5)  # Zet standaard volume op 0.5
    pygame.mixer.music.play(-1)  # Speel de muziek in een loop af

    # Stel de grootte en positie van de volumebalk in het midden van de onderkant
    volume_slider_width = 300
    volume_slider_height = 20
    volume_slider_x = WIDTH // 2 - volume_slider_width // 2  # Centraal horizontaal
    volume_slider_y = HEIGHT - volume_slider_height - 50  # 50 pixels van de onderkant
    slider_value = 0.5  # Start bij 50% volume

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Zet het scherm naar fullscreen
    pygame.display.set_caption("PixelPanzer - Main Menu")

    running = True
    while running:
        screen.blit(background, (0, 0))  # Teken de achtergrond

        # Teken de volumebalk
        draw_slider(volume_slider_x, volume_slider_y, volume_slider_width, volume_slider_height, slider_value)

        # Tekst om het volume aan te geven
        volume_text = font.render(f"Volume: {int(slider_value * 100)}%", True, WHITE)
        screen.blit(volume_text, (WIDTH // 2 - volume_text.get_width() // 2, volume_slider_y - 40))

        # Definieer de knoppen
        start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 60)
        exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)
        info_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 60)

        # Teken de knoppen (met afgeronde hoeken en schaduwen)
        draw_button("Start Game", GREEN, start_button)
        draw_button("Exit", RED, exit_button)
        draw_button("Game Info", (0, 0, 255), info_button)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Verander volume op basis van slider
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(volume_slider_x, volume_slider_y, volume_slider_width, volume_slider_height).collidepoint(event.pos):
                    slider_value = (event.pos[0] - volume_slider_x) / (volume_slider_width - 20)
                    slider_value = max(0, min(slider_value, 1))  # Beperk de waarde van de slider tussen 0 en 1
                    pygame.mixer.music.set_volume(slider_value)  # Pas het volume aan

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if pygame.Rect(volume_slider_x, volume_slider_y, volume_slider_width, volume_slider_height).collidepoint(event.pos):
                        slider_value = (event.pos[0] - volume_slider_x) / (volume_slider_width - 20)
                        slider_value = max(0, min(slider_value, 1))  # Beperk de waarde van de slider tussen 0 en 1
                        pygame.mixer.music.set_volume(slider_value)  # Pas het volume aan

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()  # Stop de menu muziek
                    pygame.mixer.music.load(os.path.join(ASSETS_DIR, "main.wav"))  # Laad de spel muziek
                    pygame.mixer.music.set_volume(0.1)  # Stel het volume van de spel muziek in
                    pygame.mixer.music.play(-1)  # Speel de muziek in een loop af
                    main()  # Start het game bestand
                    running = False
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if info_button.collidepoint(event.pos):
                    info_screen()  # Toon het info-scherm
                    running = False





def main():
    # Zet het scherm naar fullscreen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("PixelPanzer")

    clock = pygame.time.Clock()

    class Tank:
        def __init__(self, x, y, angle, image, keys, player_num, reverse_movement=False):
            self.x = x
            self.y = y
            self.angle = angle
            self.image = image
            self.speed = 3
            self.hit_count = 0
            self.shoot_cooldown = 500
            self.keys = keys
            self.bullets = []
            self.last_shot_time = 0
            self.reverse_movement = reverse_movement
            self.is_moving = False
            self.upgraded = False
            self.upgrade_time = 0
            self.upgrade_message = ""
            self.timer_message = ""
            self.font = pygame.font.Font(None, 36)  # Font voor het bericht
            self.upgrade_message_time = 0  # Tijd wanneer upgrade-bericht werd ingesteld
            self.upgrade_expired_time = 0  # Tijd wanneer de upgrade is verlopen
            self.player_num = player_num  # Het nummer van de speler (1 of 2)
            self.easter_egg_message = ""  # Geheime boodschap voor het easter egg
            self.has_found_easter_egg = False  # Flag om bij te houden of het easter egg al gevonden is
            self.is_in_easter_egg_zone = False  # Flag om bij te houden of de tank in de easter egg zone is

        def move(self, keys_pressed, obstacles, other_tank):
            if keys_pressed[self.keys['left']]:
                self.angle -= 2
            if keys_pressed[self.keys['right']]:
                self.angle += 2

            direction = 1 if self.reverse_movement else 1
            new_x, new_y = self.x, self.y
            moving = False

            if keys_pressed[self.keys['up']]:
                new_x += direction * self.speed * math.cos(math.radians(self.angle))
                new_y += direction * self.speed * math.sin(math.radians(self.angle))
                moving = True
            elif keys_pressed[self.keys['down']]:
                new_x -= direction * self.speed * math.cos(math.radians(self.angle))
                new_y -= direction * self.speed * math.sin(math.radians(self.angle))
                moving = True

            tank_rect = pygame.Rect(new_x - TANK_WIDTH / 2, new_y - TANK_HEIGHT / 2, TANK_WIDTH, TANK_HEIGHT)
            for obstacle in obstacles:
                obstacle_hitbox = pygame.Rect(obstacle.x + 10, obstacle.y + 5, 60, 30)
                if tank_rect.colliderect(obstacle_hitbox):
                    return

            other_tank_rect = pygame.Rect(other_tank.x - TANK_WIDTH / 2, other_tank.y - TANK_HEIGHT / 2, TANK_WIDTH, TANK_HEIGHT)
            if tank_rect.colliderect(other_tank_rect):
                return

            self.x = max(TANK_WIDTH / 2, min(WIDTH - TANK_WIDTH / 2, new_x))
            self.y = max(TANK_HEIGHT / 2, min(HEIGHT - TANK_HEIGHT / 2, new_y))

            if moving and not self.is_moving:
                engine_sound.play()
            if not moving and self.is_moving:
                engine_sound.stop()

            self.is_moving = moving

            self.check_upgrade()
            self.check_easter_egg()

        def check_upgrade(self):
            if UPGRADE_ZONE.collidepoint(self.x, self.y) and not self.upgraded:
                self.upgraded = True
                self.upgrade_time = pygame.time.get_ticks()
                self.speed = UPGRADE_SPEED
                self.shoot_cooldown = UPGRADE_SHOOT_COOLDOWN
                self.upgrade_message = "Upgrade verkregen! +Snelheid +Schietfrequentie"
                self.upgrade_message_time = pygame.time.get_ticks()  # Sla de tijd op dat het upgrade-bericht werd getoond
                self.timer_message = "Timer: 15s"

            if self.upgraded:
                elapsed_time = pygame.time.get_ticks() - self.upgrade_time
                remaining_time = max(0, (TIMER_DURATION - elapsed_time) // 1000)
                self.timer_message = f"{remaining_time}s"

                if elapsed_time > UPGRADE_DURATION:
                    self.upgraded = False
                    self.speed = 3
                    self.shoot_cooldown = 500
                    self.upgrade_expired_time = pygame.time.get_ticks()  # Wanneer de upgrade is verlopen
                    self.upgrade_message = "Upgrade verlopen!"
                    self.timer_message = ""

                # Verwijder het upgrade-bericht "Upgrade verlopen!" na 3 seconden
            if self.upgrade_message == "Upgrade verlopen!" and pygame.time.get_ticks() - self.upgrade_expired_time > 3000:
                self.upgrade_message = ""

        def check_easter_egg(self):
            # Check of de tank over de easter egg-zone gaat
            if EASTER_EGG_ZONE.collidepoint(self.x, self.y) and not self.has_found_easter_egg:
                self.easter_egg_message = "Hmmmm, you found something!"
                self.has_found_easter_egg = True
                if not self.is_in_easter_egg_zone:
                    easter_egg_sound.play(-1)  # Speel de easter egg muziek in een lus
                    self.is_in_easter_egg_zone = True  # Zet de flag om aan te geven dat we in de zone zijn

            elif not EASTER_EGG_ZONE.collidepoint(self.x, self.y):
                # Als je de easter egg zone verlaat, stop de muziek
                if self.is_in_easter_egg_zone:
                    easter_egg_sound.stop()  # Stop de easter egg muziek zodra je de zone verlaat
                    self.is_in_easter_egg_zone = False
                if self.has_found_easter_egg:
                    self.easter_egg_message = ""
                    self.has_found_easter_egg = False

        def draw(self):
            rotated_image = pygame.transform.rotate(self.image, -self.angle)
            tank_rect = rotated_image.get_rect(center=(self.x, self.y))
            screen.blit(rotated_image, tank_rect.topleft)

            # Bepaal de positie van de tekst afhankelijk van het player_num
            if self.player_num == 1:
                x_pos = 20  # Links bovenaan
                text_color = (255, 0, 0)  # Rood voor Tank 1
                timer_color = (255, 0, 0)  # Rood voor Tank 1
            else:
                x_pos = screen.get_width() - 20 - self.font.size(self.upgrade_message)[0]  # Rechts bovenaan
                text_color = (0, 0, 255)  # Blauw voor Tank 2
                timer_color = (0, 0, 255)  # Blauw voor Tank 2

            # Toon het laatste bericht (upgradebericht)
            if self.upgrade_message:
                text_surface = self.font.render(self.upgrade_message, True, text_color)
                screen.blit(text_surface, (x_pos, 20))  # Plaats de tekst bovenaan, zonder ruimte eronder

            # Toon timer boven de tank
            if self.timer_message:
                timer_surface = self.font.render(self.timer_message, True, timer_color)
                screen.blit(timer_surface, (self.x - 20, self.y - 40))

            # Toon het easter egg bericht (geheime boodschap)
            if self.easter_egg_message:
                easter_surface = self.font.render(self.easter_egg_message, True,(255, 255, 255))  # Groene kleur voor de boodschap
                screen.blit(easter_surface,(screen.get_width() // 2 - easter_surface.get_width() // 2, 90))  # Midden bovenaan

        def shoot(self):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > SHOOT_COOLDOWN and len(self.bullets) < MAX_BULLETS:
                barrel_x = self.x + (TANK_WIDTH // 2) * math.cos(math.radians(self.angle))
                barrel_y = self.y + (TANK_HEIGHT // 2) * math.sin(math.radians(self.angle))
                bullet_dx = BULLET_SPEED * math.cos(math.radians(self.angle))
                bullet_dy = BULLET_SPEED * math.sin(math.radians(self.angle))

                if self.image == BLUE_TANK_IMAGE:
                    bullet_image = pygame.transform.rotate(BLUE_BULLET_IMAGE, 180)
                else:
                    bullet_image = RED_BULLET_IMAGE

                rotated_bullet_image = pygame.transform.rotate(bullet_image, -self.angle)

                self.bullets.append([barrel_x, barrel_y, bullet_dx, bullet_dy, rotated_bullet_image])
                self.last_shot_time = current_time
                small_explosion_sound.play()

        def update_bullets(self, opponent, obstacles):
            for bullet1 in self.bullets[:]:
                # Beweeg de kogel
                bullet1[0] += bullet1[2]
                bullet1[1] += bullet1[3]

                # Verwijder kogel als deze buiten het scherm gaat
                if bullet1[0] < 0 or bullet1[0] > WIDTH or bullet1[1] < 0 or bullet1[1] > HEIGHT:
                    self.bullets.remove(bullet1)
                else:
                    # Controleer op botsing tussen kogels
                    for bullet2 in opponent.bullets[:]:
                        if self.check_bullet_collision(bullet1, bullet2):
                            self.bullets.remove(bullet1)
                            opponent.bullets.remove(bullet2)
                            self.explode(bullet1[0], bullet1[1])  # Speel de explosie af voor de eerste kogel
                            opponent.explode(bullet2[0], bullet2[1])  # Speel de explosie af voor de tweede kogel
                            small_explosion_sound.play()  # Speel het explosiegeluid af

                    # Controleer of de kogel de tegenstander raakt
                    if opponent.hitbox().collidepoint(bullet1[0], bullet1[1]):
                        opponent.hit_count += 1
                        self.bullets.remove(bullet1)
                        self.explode(bullet1[0], bullet1[1])  # Speel explosie af bij botsing met de tegenstander
                        big_explosion_sound.play()

                    # Controleer of de kogel een obstakel raakt
                    for obstacle in obstacles:
                        obstacle_hitbox = pygame.Rect(obstacle.x + 10, obstacle.y + 5, 60, 30)
                        if obstacle_hitbox.collidepoint(bullet1[0], bullet1[1]):
                            self.bullets.remove(bullet1)
                            self.explode(bullet1[0], bullet1[1])  # Speel explosie af bij botsing met obstakel
                            small_explosion_sound.play()
                            break

                # Teken de kogel
                screen.blit(bullet1[4],
                            (bullet1[0] - bullet1[4].get_width() // 2, bullet1[1] - bullet1[4].get_height() // 2))

        def check_bullet_collision(self, bullet1, bullet2):
            """
            Controleer of twee kogels elkaar raken.
            """
            bullet1_rect = pygame.Rect(bullet1[0] - bullet1[4].get_width() // 2,
                                       bullet1[1] - bullet1[4].get_height() // 2, bullet1[4].get_width(),
                                       bullet1[4].get_height())
            bullet2_rect = pygame.Rect(bullet2[0] - bullet2[4].get_width() // 2,
                                       bullet2[1] - bullet2[4].get_height() // 2, bullet2[4].get_width(),
                                       bullet2[4].get_height())

            # Controleer of de hitboxen van de kogels elkaar raken
            return bullet1_rect.colliderect(bullet2_rect)

        def explode(self, x, y):
            """
            Toon een explosie bij de opgegeven positie zonder vertraging.
            """
            # Laad een explosie-afbeelding
            explosion_image = pygame.image.load(os.path.join(ASSETS_DIR, "explosion.png"))
            explosion_image = pygame.transform.scale(explosion_image, (50, 50))  # Pas de grootte aan

            # Toon de explosie-afbeelding op de opgegeven locatie
            screen.blit(explosion_image, (x - explosion_image.get_width() // 2, y - explosion_image.get_height() // 2))

        def hitbox(self):
            return pygame.Rect(self.x - TANK_WIDTH / 2, self.y - TANK_HEIGHT / 2, TANK_WIDTH, TANK_HEIGHT)

    def draw_game_over(winner):
        # Set the screen size to 800x600 for the game over screen
        game_over_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Game Over")
        game_over_screen.fill(WHITE)
        game_over_screen.blit(background, (0, 0))  # Use the same background as the main menu

        pygame.mixer.music.load(os.path.join(ASSETS_DIR, "MainMenu.wav"))  # Laad de menu muziek
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Speel de muziek in een loop af

        # Add the "Winner" text, without shadow effect
        game_over_text = GAME_OVER_FONT.render(f"{winner} Wins!", True, (255, 0, 0))
        game_over_screen.blit(game_over_text,
                              (WIDTH // 2 - game_over_text.get_width() // 2,
                               HEIGHT // 3 + 50))  # Move down by 50 pixels

        # Retry, Exit and Back to Menu buttons with hover effects
        retry_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 70, 240,
                                   60)  # Moved up 30 pixels for retry button
        exit_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 150, 240,
                                  60)  # Moved up 30 pixels for exit button
        menu_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 230, 240,
                                  60)  # Moved up 30 pixels for back to menu button

        mouse_pos = pygame.mouse.get_pos()

        # Retry button hover effect
        if retry_button.collidepoint(mouse_pos):
            pygame.draw.rect(game_over_screen, (0, 255, 0), retry_button, border_radius=10)
            pygame.draw.rect(game_over_screen, DARK_GRAY, retry_button, 5)
        else:
            pygame.draw.rect(game_over_screen, (0, 200, 0), retry_button, border_radius=10)
            pygame.draw.rect(game_over_screen, DARK_GRAY, retry_button, 5)

        # Exit button hover effect
        if exit_button.collidepoint(mouse_pos):
            pygame.draw.rect(game_over_screen, (255, 0, 0), exit_button, border_radius=10)
            pygame.draw.rect(game_over_screen, DARK_GRAY, exit_button, 5)
        else:
            pygame.draw.rect(game_over_screen, (200, 0, 0), exit_button, border_radius=10)
            pygame.draw.rect(game_over_screen, DARK_GRAY, exit_button, 5)

        # Back to Menu button hover effect
        if menu_button.collidepoint(mouse_pos):
            pygame.draw.rect(game_over_screen, (0, 0, 255), menu_button, border_radius=10)
            pygame.draw.rect(game_over_screen, DARK_GRAY, menu_button, 5)
        else:
            pygame.draw.rect(game_over_screen, (0, 0, 200), menu_button, border_radius=10)
            pygame.draw.rect(game_over_screen, DARK_GRAY, menu_button, 5)

        retry_text = BUTTON_FONT.render("Retry", True, WHITE)
        exit_text = BUTTON_FONT.render("Exit", True, WHITE)
        menu_text = BUTTON_FONT.render("Back to Menu", True, WHITE)

        # Center the text on the buttons
        game_over_screen.blit(retry_text, (retry_button.x + (retry_button.width - retry_text.get_width()) // 2,
                                           retry_button.y + (retry_button.height - retry_text.get_height()) // 2))
        game_over_screen.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2,
                                          exit_button.y + (exit_button.height - exit_text.get_height()) // 2))
        game_over_screen.blit(menu_text, (menu_button.x + (menu_button.width - menu_text.get_width()) // 2,
                                          menu_button.y + (menu_button.height - menu_text.get_height()) // 2))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.collidepoint(event.pos):
                        main()  # Retry the game by starting the main function again
                    if exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    if menu_button.collidepoint(event.pos):
                        main_menu()  # Go back to the main menu

    tank1 = Tank(100, 540, 0, RED_TANK_IMAGE, {'left': pygame.K_q, 'right': pygame.K_d, 'up': pygame.K_z, 'down': pygame.K_s, 'shoot': pygame.K_SPACE},player_num=1, reverse_movement=True)
    tank2 = Tank(1820, 540, 180, BLUE_TANK_IMAGE, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN, 'shoot': pygame.K_RETURN},player_num=2, reverse_movement=True)

    obstacles = [
        pygame.Rect(100, 50, 100, 50),  # Obstakel 1
        pygame.Rect(1800, 50, 100, 50),  # Obstakel 2
        pygame.Rect(400, 150, 150, 50),  # Obstakel 3
        pygame.Rect(1700, 250, 80, 40),  # Obstakel 4
        pygame.Rect(600, 350, 80, 40),  # Obstakel 5
        pygame.Rect(1300, 450, 120, 60),  # Obstakel 6
        pygame.Rect(200, 550, 100, 50),  # Obstakel 7
        pygame.Rect(800, 650, 120, 60),  # Obstakel 8
        pygame.Rect(1000, 100, 90, 45),  # Obstakel 9
        pygame.Rect(400, 800, 110, 55),  # Obstakel 10
        pygame.Rect(1500, 600, 100, 50),  # Obstakel 11
        pygame.Rect(100, 700, 130, 65),  # Obstakel 12
        pygame.Rect(900, 300, 120, 60),  # Obstakel 13
        pygame.Rect(1600, 300, 150, 75),  # Obstakel 14
        pygame.Rect(300, 1000, 80, 40),  # Obstakel 15
        pygame.Rect(1200, 700, 100, 50),  # Obstakel 16
        pygame.Rect(500, 250, 100, 50),  # Obstakel 17
        pygame.Rect(1500, 800, 120, 60),  # Obstakel 18
        pygame.Rect(600, 900, 90, 45),  # Obstakel 19
        pygame.Rect(1700, 950, 110, 55),  # Obstakel 20
        # Obstakels in het midden
        pygame.Rect(900, 500, 120, 60),  # Obstakel 21
        pygame.Rect(850, 550, 100, 50),  # Obstakel 22
        pygame.Rect(950, 550, 100, 50),  # Obstakel 23
        pygame.Rect(800, 600, 120, 60),  # Obstakel 24
        pygame.Rect(1000, 600, 120, 60)  # Obstakel 25
    ]

    while True:
        clock.tick(60)
        screen.fill(WHITE)
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        for obstacle in obstacles:
            screen.blit(OBSTACLE_IMAGE, (obstacle.x, obstacle.y))

        keys_pressed = pygame.key.get_pressed()

        if tank1.hit_count >= 3:
            draw_game_over("Blue Tank")
            break
        if tank2.hit_count >= 3:
            draw_game_over("Red Tank")
            break

        tank1.move(keys_pressed, obstacles, tank2)
        tank2.move(keys_pressed, obstacles, tank1)

        if keys_pressed[tank1.keys['shoot']]:
            tank1.shoot()
        if keys_pressed[tank2.keys['shoot']]:
            tank2.shoot()

        tank1.update_bullets(tank2, obstacles)
        tank2.update_bullets(tank1, obstacles)
        tank1.draw()
        tank2.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main_menu()
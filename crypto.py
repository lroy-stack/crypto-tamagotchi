import pygame
import sys
import random

pygame.init()

# Adaptado a 9:16 (ej. 360x640)
WIDTH, HEIGHT = 360, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crypto Tamagotchi")

# Colores
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (255, 0,   0)
BLUE   = (0,   0, 255)
YELLOW = (255, 255, 0)

# Colores NEÓN
NEON_GREEN  = (57, 255, 20)
NEON_PINK   = (255, 20, 147)
NEON_CYAN   = (0, 255, 255)
NEON_YELLOW = (255, 255, 0)

# Fuentes
font      = pygame.font.SysFont("arial", 28, bold=True)
big_font  = pygame.font.SysFont("arialblack", 40, bold=True)
title_font= pygame.font.SysFont("arialblack", 50, bold=True)  # Título más grande

def draw_text_outline(text, x, y, used_font, main_color, outline_color=BLACK, outline_thickness=2, center=False):
    """Dibuja texto con contorno (outline)."""
    base_surface = used_font.render(text, True, main_color)
    base_rect = base_surface.get_rect()
    if center:
        base_rect.center = (x, y)
    else:
        base_rect.topleft = (x, y)

    # Contorno alrededor del texto
    for dx in range(-outline_thickness, outline_thickness + 1):
        for dy in range(-outline_thickness, outline_thickness + 1):
            if abs(dx) + abs(dy) != 0:
                outline_surface = used_font.render(text, True, outline_color)
                outline_rect = outline_surface.get_rect(center=base_rect.center)
                outline_rect.move_ip(dx, dy)
                screen.blit(outline_surface, outline_rect)

    screen.blit(base_surface, base_rect)

# Carga de fuente de iconos (Font Awesome Brands) para los íconos de redes
try:
    icon_font = pygame.font.Font("fontawesome-free-6.7.2-web/webfonts/fa-brands-400.ttf", 28)
except:
    icon_font = font

# Íconos de redes (FontAwesome Brands)
ICON_INSTAGRAM = chr(0xf16d)
ICON_TWITTER   = chr(0xf099)
ICON_YOUTUBE   = chr(0xf167)

icon_insta    = icon_font.render(ICON_INSTAGRAM, True, BLACK)
icon_twitter  = icon_font.render(ICON_TWITTER,   True, BLACK)
icon_youtube  = icon_font.render(ICON_YOUTUBE,   True, BLACK)

icon_positions = {
    "insta":   (20,  HEIGHT - 60),
    "twitter": (80,  HEIGHT - 60),
    "youtube": (140, HEIGHT - 60)
}

# Carga de imágenes
bg     = pygame.image.load("background.png")
bg     = pygame.transform.scale(bg, (WIDTH, HEIGHT))
happy  = pygame.image.load("happy.png")
sad    = pygame.image.load("sad.png")
hungry = pygame.image.load("hungry.png")
coin   = pygame.image.load("coin.png")
happy  = pygame.transform.scale(happy, (100, 100))
sad    = pygame.transform.scale(sad, (100, 100))
hungry = pygame.transform.scale(hungry, (100, 100))
coin   = pygame.transform.scale(coin, (50, 50))

# ------------------ Variables globales ------------------
game_state = {
    "energy":               100,
    "hunger":               0,
    "happiness":            100,
    "crypto":               0,
    "message":              "",
    "message_timer":        0,
    "difficulty_multiplier":1.0,
    "flash_feed_timer":     0,
    "flash_play_timer":     0,
    "start_time":           pygame.time.get_ticks()
}

clock = pygame.time.Clock()

# ------------------- Funciones Lógica Tamagotchi -------------------
def feed():
    if game_state["hunger"] > 0:
        game_state["hunger"] = max(game_state["hunger"] - 20, 0)
        game_state["message"] = "¡Alimentado!"
        game_state["flash_feed_timer"] = 15
    else:
        game_state["message"] = "¡No tiene hambre!"
    game_state["message_timer"] = 60

def play():
    if game_state["energy"] > 10:
        game_state["happiness"] = min(game_state["happiness"] + 10, 100)
        game_state["energy"]    = max(game_state["energy"] - 15, 0)
        game_state["message"]   = "¡Jugado!"
        game_state["flash_play_timer"] = 15
    else:
        game_state["message"] = "¡Cansado!"
    game_state["message_timer"] = 60

def sleep():
    game_state["energy"] = min(game_state["energy"] + 20, 100)
    game_state["hunger"] = min(game_state["hunger"] + 10, 100)
    game_state["message"] = "¡Dormido!"
    game_state["message_timer"] = 60

def mine_crypto():
    if game_state["energy"] > 50 and game_state["happiness"] > 50:
        game_state["crypto"] += 10
        game_state["energy"] = max(game_state["energy"] - 10, 0)
        game_state["happiness"] = max(game_state["happiness"] - 5, 0)
        game_state["message"] = "¡Minando!"
    else:
        game_state["message"] = "¡Falta energía/felicidad!"
    game_state["message_timer"] = 60

def share_game():
    """Ejemplo de botón 'Compartir'."""
    print("Compartiendo el juego... (ejemplo)")

def reset_game():
    """Reinicia el estado para empezar de nuevo."""
    game_state["energy"]               = 100
    game_state["hunger"]               = 0
    game_state["happiness"]            = 100
    game_state["crypto"]               = 0
    game_state["message"]              = ""
    game_state["message_timer"]        = 0
    game_state["difficulty_multiplier"]= 1.0
    game_state["flash_feed_timer"]     = 0
    game_state["flash_play_timer"]     = 0
    game_state["start_time"]           = pygame.time.get_ticks()

# -------------------------------------------------------------------
def draw_neon_bar(x, y, value, max_value, base_color, flash=False):
    fill_width = int(200 * (value / max_value))
    glow_surf = pygame.Surface((220, 30), pygame.SRCALPHA)
    glow_surf.fill((0, 0, 0, 0))
    glow_color = base_color if not flash else (255, 255, 255)
    pygame.draw.rect(glow_surf, glow_color + (50,), (0, 0, 220, 30), border_radius=8)
    screen.blit(glow_surf, (x-10, y-5))

    pygame.draw.rect(screen, BLACK, (x, y, 200, 20), border_radius=3)
    pygame.draw.rect(screen, base_color, (x, y, fill_width, 20), border_radius=3)

def draw_particles():
    """Efecto de partículas al minar."""
    for _ in range(15):
        px = random.randint(WIDTH//2 - 70, WIDTH//2 + 70)
        py = random.randint(HEIGHT//2 + 30, HEIGHT//2 + 130)
        size = random.randint(2, 5)
        color = random.choice((NEON_YELLOW, NEON_CYAN, NEON_PINK))
        pygame.draw.circle(screen, color, (px, py), size)

# ------------------ Pantalla de GameOver con Comenzar / Salir ------------------
def game_over_screen():
    """
    Muestra la pantalla de GameOver y 2 botones:
      - Comenzar (reiniciar juego)
      - Salir (cerrar aplicación)
    """
    end_time = pygame.time.get_ticks()
    time_survived = (end_time - game_state["start_time"]) // 1000

    # Creamos botones "Comenzar" y "Salir"
    restart_btn = NeonButton((WIDTH//2 - 120), (HEIGHT//2 + 80), 100, 50, "Comenzar")
    exit_btn    = NeonButton((WIDTH//2 + 20),  (HEIGHT//2 + 80), 100, 50, "Salir")

    # Bucle de la pantalla de gameover
    while True:
        screen.fill(BLACK)
        draw_text_outline("GAME OVER", WIDTH//2, HEIGHT//2 - 60, big_font, RED, outline_color=WHITE, outline_thickness=2, center=True)
        draw_text_outline(f"Sobreviviste: {time_survived}s", WIDTH//2, HEIGHT//2, font, YELLOW, outline_color=BLACK, outline_thickness=2, center=True)
        draw_text_outline(f"Cripto: {game_state['crypto']}", WIDTH//2, HEIGHT//2 + 40, font, YELLOW, outline_color=BLACK, outline_thickness=2, center=True)

        # Dibujamos los botones
        restart_btn.draw(screen)
        exit_btn.draw(screen)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Comprueba si se hace clic en "Comenzar"
                if restart_btn.rect.collidepoint(mx, my):
                    restart_btn.click()
                    reset_game()  # Reiniciamos variables
                    return        # Regresamos al main
                # Comprueba si se hace clic en "Salir"
                if exit_btn.rect.collidepoint(mx, my):
                    exit_btn.click()
                    pygame.quit()
                    sys.exit()

# ------------------- Pantalla de Inicio -------------------
def start_screen():
    """
    Pantalla de inicio.
    """
    sad_cover = pygame.transform.scale(sad, (120, 120))
    share_button = NeonButton(x=WIDTH - 90, y=20, w=70, h=40, text="Comp.")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if share_button.rect.collidepoint(mx, my):
                    share_game()
                    share_button.click()
                else:
                    return  # Comienza el juego

        screen.fill(WHITE)
        # Título en 2 líneas
        draw_text_outline("Crypto", WIDTH//2, 80, title_font, NEON_PINK, outline_color=BLACK, outline_thickness=2, center=True)
        draw_text_outline("Tamagotchi", WIDTH//2, 140, big_font, NEON_CYAN, outline_color=BLACK, outline_thickness=2, center=True)
        screen.blit(sad_cover, (WIDTH//2 - 60, HEIGHT//2 - 60))
        draw_text_outline("Toca la pantalla", WIDTH//2, HEIGHT//2 + 70, font, BLACK, outline_color=WHITE, outline_thickness=2, center=True)

        # Íconos redes
        screen.blit(icon_insta,   icon_positions["insta"])
        screen.blit(icon_twitter, icon_positions["twitter"])
        screen.blit(icon_youtube, icon_positions["youtube"])

        # Botón Compartir
        share_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

# ------------------ Botones Táctiles con Hover & Flash ---------------------
class NeonButton:
    def __init__(self, x, y, w=None, h=None, text="", base_color=(50, 50, 50), hover_color=(80, 80, 80)):
        """
        Si x, y se pasan como tupla, lo manejamos. w,h deben ser enteros.
        """
        if isinstance(x, tuple):
            self.rect = pygame.Rect(x[0], x[1], w, h)
        else:
            self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.base_color = base_color
        self.hover_color = hover_color
        self.flash_timer = 0  
        self.font = pygame.font.SysFont("arial", 24, bold=True)

    def draw(self, surface):
        mx, my = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mx, my) else self.base_color

        if self.flash_timer > 0:
            glow_surf = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
            glow_surf.fill((0, 0, 0, 0))
            pygame.draw.rect(glow_surf, (255, 255, 255, 80), (0, 0, self.rect.width + 10, self.rect.height + 10), border_radius=8)
            surface.blit(glow_surf, (self.rect.x - 5, self.rect.y - 5))
            self.flash_timer -= 1

        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def click(self):
        self.flash_timer = 10

# ------------------------ B O T O N E S  (en español) ------------------------
feed_button  = NeonButton(10,   HEIGHT - 70, 75,  50, "Alim.")
play_button  = NeonButton(95,   HEIGHT - 70, 75,  50, "Jugar")
sleep_button = NeonButton(180,  HEIGHT - 70, 75,  50, "Dormir")
mine_button  = NeonButton(265,  HEIGHT - 70, 75,  50, "Minar")

def main():
    # Primero, pantalla de inicio
    start_screen()

    # Variables de animación del avatar
    avatar_y  = HEIGHT // 2 - 100
    direction = 1
    running   = True

    while running:
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Botones Tamagotchi
                if feed_button.rect.collidepoint(mx, my):
                    feed()
                    feed_button.click()    
                elif play_button.rect.collidepoint(mx, my):
                    play()
                    play_button.click()
                elif sleep_button.rect.collidepoint(mx, my):
                    sleep()
                    sleep_button.click()
                elif mine_button.rect.collidepoint(mx, my):
                    mine_crypto()
                    mine_button.click()

        # Actualizaciones de estado
        game_state["energy"]    = max(game_state["energy"] - 0.1 * game_state["difficulty_multiplier"], 0)
        game_state["hunger"]    = min(game_state["hunger"] + 0.1 * game_state["difficulty_multiplier"], 100)
        game_state["happiness"] = max(game_state["happiness"] - 0.1 * game_state["difficulty_multiplier"], 0)
        game_state["difficulty_multiplier"] += 0.001

        # Timers de flash en las barras
        if game_state["flash_feed_timer"] > 0:
            game_state["flash_feed_timer"] -= 1
        if game_state["flash_play_timer"] > 0:
            game_state["flash_play_timer"] -= 1

        # Game Over
        if (game_state["energy"] <= 0 or 
            game_state["hunger"] >= 100 or 
            game_state["happiness"] <= 0):
            # Pantalla de game over con opciones
            game_over_screen()
            # Vuelve si se pulsó "Comenzar" => se reinicia y se llama a start_screen() de nuevo
            start_screen()
            avatar_y  = HEIGHT // 2 - 100
            direction = 1
            continue

        # Barras
        draw_neon_bar(20, 20,  game_state["energy"],    100, NEON_GREEN, flash=False)
        draw_neon_bar(20, 50,  game_state["hunger"],    100, NEON_PINK,  flash=(game_state["flash_feed_timer"] > 0))
        draw_neon_bar(20, 80,  game_state["happiness"], 100, NEON_CYAN,  flash=(game_state["flash_play_timer"] > 0))

        # Texto Cripto
        draw_text_outline(f"Cripto: {game_state['crypto']}", 
                          20, 110, font, NEON_YELLOW, outline_color=BLACK, outline_thickness=2)

        # Animación avatar
        avatar_y += direction
        if avatar_y > (HEIGHT // 2 - 95) or avatar_y < (HEIGHT // 2 - 105):
            direction *= -1

        # Escogemos imagen según estado
        if game_state["happiness"] > 70:
            screen.blit(happy, (WIDTH//2 - 50, avatar_y))
        elif game_state["hunger"] > 50:
            screen.blit(hungry, (WIDTH//2 - 50, avatar_y))
        else:
            screen.blit(sad, (WIDTH//2 - 50, avatar_y))

        # Partículas si minando
        if game_state["message"] == "¡Minando!" and game_state["message_timer"] > 0:
            screen.blit(coin, (WIDTH//2 - 25, HEIGHT//2 + 50))
            draw_particles()

        # Mensaje temporal (ej. "¡Alimentado!")
        if game_state["message_timer"] > 0:
            draw_text_outline(
                game_state["message"],
                WIDTH//2, HEIGHT - 130,  
                font, NEON_YELLOW,
                outline_color=BLACK,
                outline_thickness=2,
                center=True
            )
            game_state["message_timer"] -= 1

        # Dibujamos los 4 botones
        feed_button.draw(screen)
        play_button.draw(screen)
        sleep_button.draw(screen)
        mine_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()

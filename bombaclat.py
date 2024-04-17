import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 128)
FONT_SIZE = 20

# Jamaican slang responses
responses = [
    "Bless Up",
    "Likkle More",
    "One Love",
    "Yes, Iyah!",
    "No, Iyah!",
    "Yeah, Mon!",
    "No worries, Mon!",
    "Definitely, Rasta!",
    "Not today, Jah!",
    "Yea, Mon, Big Up!",
    "Nah, Man, Nuff Respect!",
    "Absolutely, Irie!",
    "Not this time, Babylon!",
]

# Initialize window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magic 8 Ball")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Input box
input_box = pygame.Rect(105, 180, 400, 30)  # Shifted lower
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
done = False

# Magic 8 Ball
magic_8_ball_radius = 50
magic_8_ball_center = (WIDTH // 2, 90)  # Positioned slightly above

# Magic 8 Ball speech bubble
magic_8_ball_speech_bubble = pygame.Rect(190, 250, 220, 100)  # Shifted lower

# Text surface to display response
response_surface = None

# Backspace variables
backspace_delay = 300  # milliseconds
backspace_repeat = 50  # milliseconds
backspace_timer = 0
backspace_repeat_timer = 0

def draw_gradient():
    # Create a gradient surface
    gradient = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        alpha = int(255 * (1 - y / HEIGHT))
        color = (0, 0, 50, alpha)  # Dark blue gradient
        pygame.draw.line(gradient, color, (0, y), (WIDTH, y))
    window.blit(gradient, (0, 0))

def draw_rounded_rect(surface, color, rect, border_radius, width=0):
    """
    Draw a rectangle with rounded corners to the given surface.
    :param surface: The surface to draw on.
    :param color: The color of the rectangle.
    :param rect: The rectangle to draw.
    :param border_radius: The radius of the rounded corners.
    :param width: The width of the border. If 0, the rectangle will be filled.
    """
    if width:  # If border width is specified, draw the border first
        border_rect = pygame.Rect(rect)
        pygame.draw.rect(surface, color, border_rect.inflate(-2 * width, -2 * width))
        border_rect.inflate_ip(-2 * width, -2 * width)
        pygame.draw.rect(surface, color, border_rect, border_radius=border_radius)
    else:  # If no border width, just fill the rectangle
        pygame.draw.rect(surface, color, rect, border_radius=border_radius)

def draw_magic_8_ball():
    # Draw Magic 8 Ball
    pygame.draw.circle(window, BLACK, magic_8_ball_center, magic_8_ball_radius)
    pygame.draw.circle(window, BLUE, magic_8_ball_center, magic_8_ball_radius - 2)

    # Draw number "8" on the Magic 8 Ball
    font_8 = pygame.font.Font(None, 30)
    text_surface_8 = font_8.render("8", True, WHITE)
    text_rect_8 = text_surface_8.get_rect(center=magic_8_ball_center)
    window.blit(text_surface_8, text_rect_8)

    # Draw speech bubble with rounded corners
    draw_rounded_rect(window, WHITE, magic_8_ball_speech_bubble, 10, 2)
    draw_rounded_rect(window, WHITE, magic_8_ball_speech_bubble.inflate(4, 4), 10)  # Draw border

    if text == '':
        magic_8_ball_text = font.render("Ask", True, BLACK)
        # Center the text within the speech bubble
        text_rect = magic_8_ball_text.get_rect(center=(magic_8_ball_speech_bubble.centerx, magic_8_ball_speech_bubble.centery + 5))
        window.blit(magic_8_ball_text, text_rect)
    else:
        if response_surface:
            response_rect = response_surface.get_rect(center=(magic_8_ball_speech_bubble.x + magic_8_ball_speech_bubble.w // 2,
                                                               magic_8_ball_speech_bubble.y + magic_8_ball_speech_bubble.h // 2))
            window.blit(response_surface, response_rect)

# Main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if input_box.collidepoint(event.pos):
                # Toggle the active variable.
                active = not active
            else:
                active = False
            # Change the current color of the input box.
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    # When Enter key is pressed, get a response from the Magic 8 Ball
                    response = random.choice(responses)
                    response_surface = font.render(response, True, BLACK)
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    backspace_timer = pygame.time.get_ticks() + backspace_delay
                    backspace_repeat_timer = pygame.time.get_ticks() + backspace_repeat
                    # Clear the response when backspace is pressed
                    response_surface = None
                else:
                    text += event.unicode

    # Continuous backspace deletion
    current_time = pygame.time.get_ticks()
    if pygame.key.get_pressed()[pygame.K_BACKSPACE] and current_time > backspace_timer:
        if current_time > backspace_repeat_timer:
            text = text[:-1]
            backspace_repeat_timer = current_time + backspace_repeat

    window.fill(BLACK)

    draw_gradient()

    # Render input box
    pygame.draw.rect(window, color, input_box)
    txt_surface = font.render(text, True, WHITE)
    width = max(400, txt_surface.get_width()+10)
    input_box.w = width
    window.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(window, WHITE, input_box, 2)

    # Draw Magic 8 Ball
    draw_magic_8_ball()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()

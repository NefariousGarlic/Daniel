import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Set up full-screen mode
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Game clock for frame rate control
clock = pygame.time.Clock()

# Load character images (daniel.png and danielmouth.png)
character_normal = pygame.image.load('daniel.png')
character_mouth = pygame.image.load('danielmouth.png')

# Scale character images 5x (original size assumed to be 80x80)
character_normal = pygame.transform.scale(character_normal, (80 * 5, 80 * 5))
character_mouth = pygame.transform.scale(character_mouth, (80 * 5, 80 * 5))

# Load food images
burger = pygame.image.load('burger.png')
chicken_wing = pygame.image.load('ChickenWing.png')

# Scale food images 5x (original size assumed to be 50x50)
burger = pygame.transform.scale(burger, (50 * 5, 50 * 5))
chicken_wing = pygame.transform.scale(chicken_wing, (50 * 5, 50 * 5))

# Set initial character position (center bottom of the screen)
character_x = screen_width // 2 - (80 * 5) // 2
character_y = screen_height - 100 - (80 * 5)  # Leave space at the bottom for character
character_speed = 10
current_character_image = character_normal  # Start with the normal image

# Falling food attributes
food_list = []
food_images = [burger, chicken_wing]  # List of possible food images
food_speed = 7
food_spawn_time = 25  # Spawn a food every 25 frames

# Scoring
score = 0

# Timer setup (1 minute)
game_duration = 60  # Total game time in seconds
start_time = pygame.time.get_ticks()  # Record start time

# Font for score, timer, and game over
font = pygame.font.SysFont(None, 55)

# Game loop
running = True
frames = 0  # Count frames to control food spawn rate
while running:
    screen.fill((50, 168, 82))  # Background color

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Character movement (arrow keys or WASD)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        character_x -= character_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        character_x += character_speed

    # Keep character within screen bounds
    if character_x < 0:
        character_x = 0
    if character_x > screen_width - 80 * 5:
        character_x = screen_width - 80 * 5

    # Spawn new food
    if frames % food_spawn_time == 0:
        food_x = random.randint(0, screen_width - 50 * 5)
        food_image = random.choice(food_images)  # Randomly choose between burger and chicken wing
        food_list.append([food_x, -50 * 5, food_image])  # Start food above the screen

    # Update food positions
    character_near_food = False  # Flag to track if food is near

    for food_item in food_list[:]:
        food_item[1] += food_speed  # Move food down

        # Check if food is close to the character
        if character_x < food_item[0] < character_x + 80 * 5 and character_y - 20 < food_item[1] + 50 * 5 < character_y:
            current_character_image = character_mouth  # Switch to mouth open when food is close
            character_near_food = True
        elif character_near_food == False:
            current_character_image = character_normal  # Switch back to normal if no food is near

        # Check if food is caught
        if character_x < food_item[0] < character_x + 80 * 5 and character_y < food_item[1] + 50 * 5 < character_y + 80 * 5:
            food_list.remove(food_item)
            score += 1  # Increase score when food is caught

        # Check if food falls off the screen (no penalty, just remove it)
        elif food_item[1] > screen_height:
            food_list.remove(food_item)

    # Draw the character
    screen.blit(current_character_image, (character_x, character_y))

    # Draw the food
    for food_item in food_list:
        screen.blit(food_item[2], (food_item[0], food_item[1]))

    # Calculate remaining time
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Time in seconds
    remaining_time = max(0, game_duration - elapsed_time)  # Ensure it doesn't go below 0

    # Display score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # Display timer
    timer_text = font.render(f"Time Left: {int(remaining_time)}s", True, (255, 255, 255))
    screen.blit(timer_text, (20, 80))

    # Check if time is up
    if remaining_time <= 0:
        game_over_text = font.render(f"Time's Up! Final Score: {score}", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - 200, screen_height // 2 - 50))
        pygame.display.flip()
        pygame.time.delay(3000)  # Wait 3 seconds before quitting
        running = False

    # Update the display
    pygame.display.flip()

    # Frame count (for food spawn control)
    frames += 1

    # Cap the frame rate at 60 frames per second
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()

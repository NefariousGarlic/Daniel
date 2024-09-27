import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Set up full-screen mode
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Game clock for frame rate control
clock = pygame.time.Clock()

# Load character images with high resolution
character_normal = pygame.image.load('danielbaldpants.png')
character_mouth = pygame.image.load('danielbaldmouth.png')

# Scale character images to twice the original size
character_size = 400  # High resolution size (double the original 300)
character_normal = pygame.transform.scale(character_normal, (character_size, character_size))
character_mouth = pygame.transform.scale(character_mouth, (character_size, character_size))

# Load food images with high resolution
burger = pygame.image.load('burger.png')
chicken_wing = pygame.image.load('ChickenWing.png')
eggplant = pygame.image.load('eggplant.png')
cucumber = pygame.image.load('cumber.png')
chip = pygame.image.load('chip.png')

# Scale food images to high quality
food_size = 100  # Adjust food size for quality
burger = pygame.transform.scale(burger, (food_size, food_size))
chicken_wing = pygame.transform.scale(chicken_wing, (food_size, food_size))
eggplant = pygame.transform.scale(eggplant, (food_size, food_size))
cucumber = pygame.transform.scale(cucumber, (food_size, food_size))
chip = pygame.transform.scale(chip, (food_size, food_size))

# Update food images list
food_images = [burger, chicken_wing, eggplant, cucumber, chip]

# Load background image
background_image = pygame.image.load('fruitwall.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Set initial character position (center bottom of the screen)
character_x = screen_width // 2 - character_size // 2
character_y = screen_height - 100 - character_size
character_speed = 10
current_character_image = character_normal

# Falling food attributes
food_list = []
food_speed = 5
food_spawn_time = 25  # Spawn a food every 25 frames

# Scoring and high score board
score = 0
high_scores = []

# Timer setup (1 minute)
game_duration = 60
start_time = pygame.time.get_ticks()

# Font for score, timer, and game over
font = pygame.font.SysFont('Arial', 55)

# Function to reset game state
def reset_game():
    global score, food_list, character_x, character_y, current_character_image, start_time
    high_scores.append(score)  # Save the score to high scores
    score = 0
    food_list = []
    character_x = screen_width // 2 - character_size // 2
    character_y = screen_height - 100 - character_size
    current_character_image = character_normal
    start_time = pygame.time.get_ticks()  # Reset start time

# Define a proximity threshold
proximity_threshold = 50  # Adjust this value as needed

# Variable to track rounds
round_counter = 0

# Game loop
running = True
frames = 0
while running:
    # Draw the background image
    screen.blit(background_image, (0, 0))

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
    if character_x > screen_width - character_size:
        character_x = screen_width - character_size

    # Spawn new food
    if frames % food_spawn_time == 0:
        food_x = random.randint(0, screen_width - food_size)
        food_image = random.choice(food_images)
        food_list.append([food_x, -food_size, food_image])

    # Update food positions
    food_nearby = False  # Track if food is nearby
    for food_item in food_list[:]:
        food_item[1] += food_speed

        # Check if food is caught
        if character_x < food_item[0] < character_x + character_size and \
           character_y < food_item[1] + food_size < character_y + character_size:
            food_list.remove(food_item)
            score += 1
            food_nearby = True  # Set flag if food is caught

        # Check if food falls off the screen
        elif food_item[1] > screen_height:
            food_list.remove(food_item)

        # Check proximity to food
        if (food_item[1] + food_size) < (character_y + character_size) and \
           (food_item[1] + food_size) > character_y and \
           (food_item[0] + food_size) > character_x and \
           food_item[0] < (character_x + character_size):
            food_nearby = True

    # Update character image based on food proximity
    if food_nearby:
        current_character_image = character_mouth
    else:
        current_character_image = character_normal

    # Draw the character
    screen.blit(current_character_image, (character_x, character_y))

    # Draw the food
    for food_item in food_list:
        screen.blit(food_item[2], (food_item[0], food_item[1]))

    # Calculate remaining time
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    remaining_time = max(0, game_duration - elapsed_time)

    # Display score and timer
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))
    timer_text = font.render(f"Time Left: {int(remaining_time)}s", True, (255, 255, 255))
    screen.blit(timer_text, (20, 80))

    # Check if time is up
    if remaining_time <= 0:
        # Switch character images every other round
        round_counter += 1
        if round_counter % 2 == 0:
            character_normal = pygame.image.load('danielbaldpants.png')
            character_mouth = pygame.image.load('danielbaldmouth.png')
        else:
            character_normal = pygame.image.load('daniel.png')
            character_mouth = pygame.image.load('danielmouth.png')

        # Reset the game
        reset_game()

    # Update the display
    pygame.display.flip()

    # Frame count for spawn control
    frames += 1

    # Cap the frame rate at 60 frames per second
    clock.tick(60)

# Quit pygame
pygame.quit()

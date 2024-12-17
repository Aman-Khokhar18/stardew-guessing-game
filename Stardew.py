import pygame
import sys
import pandas as pd
import random
import os


# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stardew Valley Screen")

# Load a Stardew Valley-like background image
background_image = pygame.image.load("stardew_valley_background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Play button sprite
play_button_image = pygame.image.load("play_button_sprite.png")
play_button_image = pygame.transform.scale(play_button_image, (220, 173))
button_x = (SCREEN_WIDTH - play_button_image.get_width()) // 2
button_y = (SCREEN_HEIGHT - play_button_image.get_height()) // 2

# Dialogue box dimensions
dialogue_box_width = SCREEN_WIDTH
dialogue_box_height = SCREEN_HEIGHT / 2
dialogue_padding_x = SCREEN_HEIGHT / 15
dialogue_padding_y = SCREEN_WIDTH / 25



# Load the dialogue image
dialogue_box_sprite = pygame.image.load("dialogue_box.png")
dialogue_box_sprite = pygame.transform.scale(dialogue_box_sprite, (dialogue_box_width, dialogue_box_height))

#Load box sprite
box_sprite = pygame.image.load("box.png")
box_sprite = pygame.transform.scale(box_sprite, (200, 200))


# Player input field
player_input = ""
filtered_suggestions = []
feedback_message = ""
feedback_color = (255, 0, 0)  # Default to red for incorrect message

# Load the CSV file globally and store it in a variable
df = pd.read_csv("stardew.csv", encoding='latin-1')

# Font for the dialogue box
font = pygame.font.Font(r"C:\\Users\\amank\\Stardew\\StardewValley.ttf", 48)
text_color = (255,255,255)


def safe_sample(data, num_items):
    """Safely sample from data without exceeding the number of available items."""
    return random.sample(data, min(len(data), num_items))

# Select a random row from the CSV file for the item to guess
def select_random_item():
    random_index = random.randint(0, len(df) - 1)
    return random_index

random_index = select_random_item()

def select_new_villager():
    """Select a new random villager and update all related attributes."""
    global random_index, boxes_to_draw, names,birthday, likes, dislikes, hates, lives_in, marriage, quotes, likes_final, dislikes_final, hates_final, loves_final, dialogue_messages, name_to_guess
    
    # Select a new random villager
    random_index = select_random_item()
    
    # Update villager attributes
    names = df.iloc[:, 0]
    birthday = df.iloc[random_index, 1]
    likes = df.iloc[random_index, 2]
    loves = df.iloc[random_index, 3]
    dislikes = df.iloc[random_index, 4]
    hates = df.iloc[random_index, 5]
    lives_in = df.iloc[random_index, 6]
    marriage = df.iloc[random_index, 7]
    quotes = df.iloc[random_index, 8]
    
    # Update safely sampled attributes
    likes_list = likes.split("\n")
    loves_list = loves.split("\n")
    dislikes_list = dislikes.split("\n")
    hates_list = hates.split("\n")
    
    dislikes_final = ", ".join(safe_sample(dislikes_list, 1))
    hates_final = ", ".join(safe_sample(hates_list, 1))
    likes_final = ", ".join(safe_sample(likes_list, 1))
    loves_final = ", ".join(safe_sample(loves_list, 1))
    
    # Update dialogue messages
    dialogue_messages = [
        "Birthday of the Villager: {} ".format(birthday),
        "Dislikes: {}".format(dislikes_final),
        "Hates: {}".format(hates_final),
        "Likes: {}".format(likes_final),
        "Loves: {}".format(loves_final),
        "Marriable? {} ".format(marriage),
        "Quotes: {} ".format(quotes),
    ]

    boxes_to_draw = [
    ("Birthday:", birthday),
    ("Dislikes:", dislikes_final),
    ("Hates:", hates_final),
    ("Likes:", likes_final),
    ("Loves:", loves_final),
    ("Lives in:", lives_in),
]

    name_to_guess = names[random_index]
    #print(name_to_guess)
    
select_new_villager()

current_message_index = 0

def draw_menu():
    """Draw the menu screen."""
    screen.blit(background_image, (0, 0))
    screen.blit(play_button_image, (button_x, button_y))
    screen.blit(font.render("By Blink", True, text_color), (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100))
    

def wrap_text(text, font, max_width):
    """Wrap text to fit within a specified width."""
    words = text.split(" ")
    wrapped_lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word
    wrapped_lines.append(current_line)
    return wrapped_lines


def filter_suggestions(input_text):
    """Filter suggestions based on input text."""
    return [item for item in names if item.lower().startswith(input_text.lower())]

def draw_box_spirit(box_loc_height, box_loc_width, title, value):
    """Draw the box sprite on top of the screen and display the title and value inside it."""
    # Draw the box sprite
    screen.blit(box_sprite, (box_loc_height, box_loc_width))

    # Scale the font size based on the box width for both lines
    font_size = min(box_sprite.get_width() // max(len(title), len(value)), 48)  # Adjust font size to fit
    font = pygame.font.Font(r"C:\\Users\\amank\\Stardew\\StardewValley.ttf", font_size+10)

    # Render the title and value
    title_surface = font.render(title, True, (107, 55, 16))  # White color for title
    value_surface = font.render(value, True, (107, 55, 16))  # White color for value

    # Calculate the total height needed for both title and value
    total_height = title_surface.get_height() + value_surface.get_height()

    # Calculate starting Y position to center text vertically within the box
    start_y = box_loc_width + (box_sprite.get_height() - total_height) // 2

    # Calculate the center position for the text horizontally
    center_x = box_loc_height + box_sprite.get_width() // 2

    # Calculate positions for title and value
    title_rect = title_surface.get_rect(center=(center_x, start_y + title_surface.get_height() // 2))
    value_rect = value_surface.get_rect(center=(center_x, start_y + title_surface.get_height() + value_surface.get_height() // 2))

    # Draw title and value on the box
    screen.blit(title_surface, title_rect)
    screen.blit(value_surface, value_rect)

# List of box data (title, value) you want to display


def draw_dialogue_screen():
    """Draw the dialogue screen with multiple boxes."""
    screen.blit(background_image, (0, 0))
    # Draw the spirit image (dialogue box)
    spirit_x = (SCREEN_WIDTH - dialogue_box_sprite.get_width()) // 2
    spirit_y = (SCREEN_HEIGHT - dialogue_box_sprite.get_height())
    screen.blit(dialogue_box_sprite, (spirit_x, spirit_y))

    # Draw the boxes up to the current message index, keeping previous ones
    box_loc_height = 10  # Starting vertical position for the first row
    box_loc_width = 100  # Starting horizontal position for the first box

    for i, (title, value) in enumerate(boxes_to_draw):
        if i > current_message_index:  # Only draw up to the current message index
            break
        
        # Draw the current box
        draw_box_spirit(box_loc_height, box_loc_width, title, value)

        # Move to the next box position (rightwards)
        box_loc_height += 200  # Move horizontally by 250 pixels

        # If the box goes beyond the screen width, reset to the next row
        if box_loc_width + 250 > SCREEN_WIDTH:  # Check if the box will overflow horizontally
            box_loc_width = 100  # Reset horizontal position to the start
            box_loc_height += 250  # Move down to the next row

    # Dialogue box text position
    box_x = spirit_x + (dialogue_box_sprite.get_width() - dialogue_box_width) // 2 + dialogue_padding_x
    box_y = spirit_y + (dialogue_box_sprite.get_height() - dialogue_box_height) // 2 + dialogue_padding_y

    # Render and draw the wrapped text for the current dialogue message
    max_text_width = dialogue_box_width - 2 * dialogue_padding_x
    text_lines = wrap_text(dialogue_messages[current_message_index], font, max_text_width)
    line_y = box_y
    for line in text_lines:
        text_surface = font.render(line, True, (107, 55, 16))  # Brownish text color
        screen.blit(text_surface, (box_x, line_y))
        line_y += text_surface.get_height() + 5

    # Draw player input field
    input_surface = font.render(player_input, True, (107, 55, 16))
    input_rect = input_surface.get_rect(topleft=(box_x, line_y + 20))
    screen.blit(input_surface, (box_x, line_y + 20))

    # Draw filtered suggestions
    suggestion_y = input_rect.bottom + 10
    for suggestion in filtered_suggestions:
        suggestion_surface = font.render(suggestion, True, (192, 99, 29))
        screen.blit(suggestion_surface, (box_x, suggestion_y))
        suggestion_y += suggestion_surface.get_height() + 5

    # Display feedback message
    feedback_surface = font.render(feedback_message, True, feedback_color)
    screen.blit(feedback_surface, (box_x, suggestion_y + 20))


def handle_menu_event(event):
    """Handle events for the menu state."""
    global current_state
    if event.type == pygame.MOUSEBUTTONDOWN:
        if button_x <= event.pos[0] <= button_x + play_button_image.get_width() and button_y <= event.pos[1] <= button_y + play_button_image.get_height():
            current_state = "dialogue"

incorrect_guesses = 0

def handle_dialogue_event(event):
    """Handle events for the dialogue state."""
    global player_input, current_state, current_message_index, feedback_message, feedback_color, name_to_guess, filtered_suggestions, incorrect_guesses
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            player_input = player_input[:-1]
        elif event.key == pygame.K_RETURN:
            if player_input.lower() == name_to_guess.lower():
                feedback_message = "Correct! Well done."
                feedback_color = (0, 255, 0)  # Green color for correct message
                name_to_guess = names[random_index]  # Select a new item after correct guess
                current_state = "victory"  # Transition to victory state after correct guess
                incorrect_guesses = 0  # Reset incorrect guesses after a correct guess
            else:
                incorrect_guesses += 1
                feedback_message = "Try again! That's not the right guess."
                feedback_color = (255, 0, 0)  # Red color for incorrect message

                if incorrect_guesses >= 7:
                    feedback_message = "You've failed! The correct item was: " + name_to_guess
                    feedback_color = (255, 255, 0)  # Yellow color for final incorrect message
                    current_state = "victory"  # Transition to victory state after 8 incorrect guesses

            player_input = ""
            current_message_index = (current_message_index + 1) % len(dialogue_messages)
        
        else:
            player_input += event.unicode

        # Update suggestions
        filtered_suggestions = filter_suggestions(player_input) if player_input.strip() else []

    
def draw_victory_screen():
    """Draw the victory screen with the guessed item name or the fact that 8 guesses have been made."""
    screen.blit(background_image, (0, 0))  # Fill screen with black color
    sprite_path = os.path.join("C:\\Users\\amank\\Stardew\\character_sprites", f"{name_to_guess}.png")
    sprite = pygame.image.load(sprite_path)
    sprite = pygame.transform.scale(sprite, (200, 200))
    sprite_x = (screen.get_width() - sprite.get_width()) // 2
    sprite_y = (screen.get_height() - sprite.get_height()) // 2

    screen.blit(sprite, (sprite_x , sprite_y - 150))

    if incorrect_guesses >= 7:
        victory_message = f"You've failed! The correct guess was: {name_to_guess}"
    else:
        victory_message = f"Correct! You guessed: {name_to_guess}"

    victory_surface = font.render(victory_message, True, (255, 255, 255))  # White text
    victory_rect = victory_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(victory_surface, victory_rect)

    # Draw "Press Enter to Play Again" message
    play_again_message = "Press Enter to Play Again"
    play_again_surface = font.render(play_again_message, True, (255, 255, 255))  # White text
    play_again_rect = play_again_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(play_again_surface, play_again_rect)

    
def handle_victory_event(event):
    """Handle events for the victory state."""
    global current_state, random_index, name_to_guess, incorrect_guesses, feedback_message, feedback_color, birthday
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        # Reset for next round
        current_state = "menu"
        random_index = select_random_item()  # Select a new random item
        incorrect_guesses = 0
        select_new_villager()

        # Reset feedback message and color
        birthday = df.iloc[random_index ,1]
        feedback_message = ""
        feedback_color = (255, 0, 0)  # Default to red for incorrect message

def play_music():
    pygame.mixer.music.load("background_music.mp3")  # Replace with your music file name
    pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)

    
def main_loop():
    """Main game loop."""
    global current_state, player_input, feedback_message, feedback_color

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif current_state == "menu":
                handle_menu_event(event)
            elif current_state == "dialogue":
                handle_dialogue_event(event)
            elif current_state == "victory":
                handle_victory_event(event)

        if current_state == "menu":
            draw_menu()
        elif current_state == "dialogue":
            draw_dialogue_screen()
        elif current_state == "victory":
            draw_victory_screen()

        pygame.display.flip()

# Initial state
current_state = "menu"

# Start the main game loop
main_loop()

# Quit pygame
pygame.quit()
sys.exit()

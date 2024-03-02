import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)  # Define RED color for hints and messages
WORD_FONT = pygame.font.SysFont('comicsans', 40)
LETTER_FONT = pygame.font.SysFont('comicsans', 30)
HINT_FONT = pygame.font.SysFont('comicsans', 30)
RADIUS = 20
GAP = 15
A = 65

HANGMAN_STAGES = [
    """
       ------
       |    |
       |    
       |   
       |    
       |   
    --------
    """,
    """
       ------
       |    |
       |    O
       |    
       |    
       |   
    --------
    """,
    """
       ------
       |    |
       |    O
       |    |
       |    
       |   
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |    
       |   
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |    
       |   
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / 
       |   
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |   
    --------
    """
]

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game! Made by: AshlingC")

topics = {
    "Animals": [("giraffe", "Has a long neck"),
                ("elephant", "Has a long trunk"),
                ("kangaroo", "Jumps around in Australia"),
                ("chimpanzee", "Close relative to humans")],
    "Cars": [("ferrari", "Italian luxury sports car"),
             ("tesla", "Innovative electric car company"),
             ("lamborghini", "Famous for its supercars"),
             ("porsche", "Known for high-performance sports cars")],
}

def get_random_word_and_topic():
    topic, words_hints = random.choice(list(topics.items()))
    word, hint = random.choice(words_hints)
    word = word.upper()
    return topic, word, hint

def draw(topic, word, guessed, letters, hangman_status, hint=None):
    WIN.fill(WHITE)

    text = HINT_FONT.render(f"Topic: {topic}", 1, BLACK)
    WIN.blit(text, (10, 10))

    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    WIN.blit(text, (400, 200))


    if hangman_status >= 3 and hint:
        hint_text = HINT_FONT.render(f"Hint: {hint}", 1, RED)
        WIN.blit(hint_text, (10, 50))

    for i, line in enumerate(HANGMAN_STAGES[hangman_status].split('\n')):
        text = LETTER_FONT.render(line, 1, BLACK)
        WIN.blit(text, (WIDTH / 4, 100 + i * 20))

    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            color = BLACK if ltr in word or ltr not in guessed else GRAY
            pygame.draw.circle(WIN, color, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, WHITE if ltr in guessed else BLACK)
            WIN.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    pygame.display.update()

def display_message(message, color=BLACK):
    WIN.fill(WHITE)
    text = WORD_FONT.render(message, 1, color)
    WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    run = True
    topic, word, hint = get_random_word_and_topic()
    guessed = []
    hangman_status = 0

    startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    starty = 450
    letters = []
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if 'a' <= event.unicode <= 'z':
                    letter = event.unicode.upper()
                    if letter not in guessed:
                        guessed.append(letter)
                        if letter not in word:
                            hangman_status += 1
                            if hangman_status == 6:
                                draw(topic, word, guessed, letters, hangman_status, hint)
                                display_message("You Lose! The word was " + word, RED)
                                run = False
                        if all(l in guessed for l in word):
                            draw(topic, word, guessed, letters, hangman_status, hint)
                            display_message("You WON!", BLACK)
                            run = False
        draw(topic, word, guessed, letters, hangman_status, hint if hangman_status >= 3 else None)

    pygame.quit()

main()
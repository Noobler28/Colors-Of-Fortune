#imports

# datetime
import datetime

#random
import random

#time
import time

#os
import os

#pickle
import pickle

#random
import random

#pygame
import pygame

#TK
from tkinter import *
from tkinter.ttk import *
from time import strftime

version = 1.5

pygame.init()
devmode = False

# List of available titles
initial_titles = ["Beginner"]
unlocked_titles = ["Beginner"]  # Start with initial titles unlocked
current_title = "Beginner"  # Start with the "Beginner" title

# List of available pets
initial_pets = ["None"]
unlocked_pets = ["None"]  # Start with initial pets unlocked
current_pet = "None"  # Start with no pet

print("save game with 'F1' load game with 'F2'")

# Time variables
current_time = pygame.time.get_ticks()

# flow Minigame variables
flow_minigame_active = False
flow_difficulty = "easy"  # easy, medium, hard
flow_grid_size = 5  # Default size for easy
flow_board = []
flow_selected = None
flow_completed = {"easy": False, "medium": False, "hard": False}
flow_rewards = {
    "easy": 10000,
    "medium": 50000,
    "hard": {"pet": "Plumber", "mult": 15}
}

# Prestige variables
prestige_cost = 1000000
prestige_points = 0 # Used for unlocking prestige upgrades
prestige_upgrades = {
    "Auto Buy Upgrades": {"cost": 5, "unlocked": False},
    "Auto Buy Automaters": {"cost": 5, "unlocked": False},
    "Free Automater": {"cost": 20, "unlocked": False}, # Multi Purchase
    }
prestige_menu_open = False
prestiges = 0
parrot_owned = False

# Command
command = ""

# Time
Time_Spent = 0

def increase_time_spent(seconds):
    global Time_Spent
    Time_Spent += seconds

# Gambling variables
earnings = 0
losings = 0
bankrupt = False
allIn = False
gambling = False

#Game Objects
score = 100
managers_owned = 0
base_multiplier = 1 + prestiges
extra_multiplier = 0

# Holiday Pets

# Define special limited pets
special_pets = {
    "Christmas": {"name": "Reindeer", "mult": 10},
    "Easter": {"name": "Easter Bunny", "mult": 8},
    "Halloween": {"name": "Ghost", "mult": 7},
    "New Year": {"name": "Firework Dragon", "mult": 12},
    "St. Patrick's Day": {"name": "Leprechaun", "mult": 9},
    "Valentine's Day": {"name": "Cupid", "mult": 6},
    "Independence Day": {"name": "Eagle", "mult": 11},
    "Thanksgiving": {"name": "Turkey", "mult": 5}
}

# Function to check if today is a holiday and unlock special pets
def check_holiday():
    global unlocked_pets
    today = time.strftime("%m-%d")
    holidays = {
        "12-25": "Christmas",
        "04-01": "Easter",
        "10-31": "Halloween",
        "01-01": "New Year",
        "03-17": "St. Patrick's Day",
        "02-14": "Valentine's Day",
        "07-04": "Independence Day",
        "11-25": "Thanksgiving"
    }
    if today in holidays:
        holiday = holidays[today]
        special_pet = special_pets[holiday]
        if special_pet["name"] not in unlocked_pets:
            unlocked_pets.append(special_pet["name"])
            print(f"Special Holiday Pet Unlocked: {special_pet['name']} with x{special_pet['mult']} multiplier!")

# Call the check_holiday function when the game starts
check_holiday()

# Dropdown menu variables
menu_expanded = False
dropdown_rect = pygame.Rect(900, 5, 200, 30)  # Positioning dropdown box
dropdown_options_rects = []  # List to hold collision rects for dropdown options

# Pets dropdown menu variables
pets_menu_expanded = False
pets_dropdown_rect = pygame.Rect(900, 45, 200, 30)  # Positioning pets dropdown box
pets_dropdown_options_rects = []  # List to hold collision rects for pets dropdown options

mystery_boxes_opened = 0  # Track number of mystery boxes opened

# Add new variables for mystery boxes
mystery_box_costs = {
    "titles": 1000,
    "pets": 2000
}

mystery_box_titles = [
    ("Explorer", 40),
    ("Adventurer", 40),
    ("Champion", 15),
    ("WTF", 0.1)
]

mystery_box_pets = [
    {"name": "Dog", "mult": 1, "weight": 40},
    {"name": "Cat", "mult": 2, "weight": 40},
    {"name": "Dragon", "mult": 3, "weight": 15},
    {"name": "Phoenix", "mult": 4, "weight": 3.5},
    {"name": "Unicorn", "mult": 5, "weight": 1},
    {"name": "Shark", "mult": 20, "weight": 0.1},
    {"name": "Rubber Ducky", "mult": 100, "weight": 0.0001}
]

# List of available titles
titles = ["Beginner", "Awesome Sauce", "Developer", "Money Bags", "Explorer", "Adventurer", "Champion", "Gambler"]

# List of available pets
pets = ["Dog", "Cat", "Dragon", "Phoenix", "Unicorn", "Reindeer", "Easter Bunny", 
        "Ghost", "Firework Dragon", "Leprechaun", "Cupid", "Eagle", "Turkey", 
        "Parrot", "Shark", "Plumber","Rubber Ducky"]

# Function to handle opening a mystery box
def open_mystery_box(box_type):
    global score, unlocked_titles, unlocked_pets, mystery_boxes_opened, mystery_box_costs
    if score >= mystery_box_costs[box_type]:
        score -= mystery_box_costs[box_type]
        mystery_boxes_opened += 1
        if mystery_box_costs[box_type] <= 1000000:  # if the cost is less than 1 million, increase the cost by 5000
            mystery_box_costs[box_type] += 5000
        else:
            mystery_box_costs[box_type] += 0
        if box_type == "titles":
            # Weighted random choice for titles
            titles_list, weights = zip(*mystery_box_titles)
            new_title = random.choices(titles_list, weights=weights, k=1)[0]
            # Find the weight for rarity
            title_weight = dict(mystery_box_titles)[new_title]
            # Determine rarity
            if title_weight <= 0.1:
                rarity = "Legendary"
            elif title_weight <= 15:
                rarity = "Epic"
            elif title_weight <= 40:
                rarity = "Rare"
            else:
                rarity = "Common"
            if new_title not in unlocked_titles:
                unlocked_titles.append(new_title)
            show_box_popup(new_title, rarity)
            print(f"Congratulations! You unlocked the title: {new_title}")
        elif box_type == "pets":
            # Weighted random choice for pets
            pet_names = [pet["name"] for pet in mystery_box_pets]
            pet_weights = [pet["weight"] for pet in mystery_box_pets]
            new_pet_name = random.choices(pet_names, weights=pet_weights, k=1)[0]
            new_pet = next(pet for pet in mystery_box_pets if pet["name"] == new_pet_name)
            if new_pet["name"] not in unlocked_pets:
                unlocked_pets.append(new_pet["name"])
            # Determine rarity
            if new_pet["weight"] <= 0.001:
                rarity = "Legendary"
            elif new_pet["weight"] <= 0.1:
                rarity = "Epic"
            elif new_pet["weight"] <= 3.5:
                rarity = "Rare"
            else:
                rarity = "Common"
            show_box_popup(new_pet["name"], rarity)
            print(f"Congratulations! You unlocked the pet: {new_pet['name']}")
            # Special animation for Rubber Ducky
            if new_pet["name"] == "Rubber Ducky":
                show_rubber_ducky_animation()

def show_rubber_ducky_animation():
    # Colors and setup
    ducky_yellow = (255, 215, 0)  # Brighter gold color
    ducky_shade = (255, 180, 0)
    ducky_highlight = (255, 255, 150)
    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2
    
    # Font with outline effect
    font_big = pygame.font.SysFont("Comic Sans MS", 42, bold=True)
    text = font_big.render("RUBBER DUCKY!!!", True, (255, 215, 0))
    text_outline = font_big.render("RUBBER DUCKY!!!", True, (200, 100, 0))
    
    # Water setup
    pond_color = (100, 200, 255)
    pond_ripples = []
    
    # Cute duck details
    blush_color = (255, 150, 150)
    eye_highlight = (255, 255, 255)
    
    # Beautiful rock formations
    rocks = [
        # Each rock has: x, y, width, height, base_color, highlight_color, shadow_color
        {"x": -180, "y": 120, "w": 45, "h": 25, 
         "colors": [(120, 110, 100), (140, 130, 120), (100, 90, 80)],
         "details": [(-5, -3, 30, 15), (10, 5, 20, 10)]},
         
        {"x": -120, "y": 140, "w": 35, "h": 20,
         "colors": [(110, 100, 90), (130, 120, 110), (90, 80, 70)],
         "details": [(5, -2, 20, 12), (-8, 3, 15, 8)]},
         
        {"x": 150, "y": 130, "w": 40, "h": 22,
         "colors": [(130, 120, 110), (150, 140, 130), (110, 100, 90)],
         "details": [(-5, -2, 25, 15), (10, 3, 18, 10)]},
         
        {"x": 90, "y": 150, "w": 30, "h": 18,
         "colors": [(100, 90, 80), (120, 110, 100), (80, 70, 60)],
         "details": [(3, -1, 18, 10), (-5, 4, 12, 7)]}
    ]
    
    # Small pebbles around the rocks
    pebbles = [
        (-160, 135, 8, 5, (110, 100, 90)),
        (-140, 145, 6, 4, (120, 110, 100)),
        (160, 140, 7, 5, (100, 90, 80)),
        (130, 155, 5, 3, (130, 120, 110)),
        (-190, 125, 9, 6, (115, 105, 95)),
        (110, 145, 6, 4, (125, 115, 105))
    ]
    
    start_time = pygame.time.get_ticks()
    duration = 3500  # Longer duration

    while pygame.time.get_ticks() - start_time < duration:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        # Animation calculations
        elapsed = pygame.time.get_ticks() - start_time
        t = elapsed / 250.0
        bounce_offset = int(40 * abs((t % 2) - 1))
        
        # Create ripples when duck is at bottom of bounce
        if int(t % 2) == 1 and elapsed % 30 < 5:
            pond_ripples.append({"time": 0, "size": 5, "alpha": 255})
            
        # Update ripples
        for ripple in pond_ripples[:]:
            ripple["time"] += 1
            ripple["size"] += 2
            ripple["alpha"] -= 5
            if ripple["alpha"] <= 0:
                pond_ripples.remove(ripple)

        # Draw everything
        screen.fill((135, 206, 235))  # Sky blue background
        
        # Draw pond with gradient
        pond_rect = pygame.Rect(center_x - 200, center_y + 50, 400, 100)
        pygame.draw.ellipse(screen, pond_color, pond_rect)
        for i in range(1, 5):
            alpha = 100 - i*20
            temp_surf = pygame.Surface((400, 100), pygame.SRCALPHA)
            pygame.draw.ellipse(temp_surf, (*pond_color[:3], alpha), 
                               (0, 0, 400 - i*20, 100 - i*10))
            screen.blit(temp_surf, (center_x - 200 + i*10, center_y + 50 + i*5))
        
        # Draw beautiful rocks
        for rock in rocks:
            rock_x = center_x + rock["x"]
            rock_y = center_y + rock["y"]
            
            # Main rock shape with shading
            pygame.draw.ellipse(screen, rock["colors"][0], 
                               (rock_x, rock_y, rock["w"], rock["h"]))
            pygame.draw.ellipse(screen, rock["colors"][1], 
                               (rock_x + 2, rock_y - 2, rock["w"] - 4, rock["h"] - 4), 2)
            pygame.draw.ellipse(screen, rock["colors"][2], 
                               (rock_x, rock_y, rock["w"], rock["h"]), 2)
            
            # Rock details/textures
            for detail in rock["details"]:
                dx, dy, dw, dh = detail
                pygame.draw.ellipse(screen, rock["colors"][1 if random.random() > 0.5 else 2], 
                                   (rock_x + dx, rock_y + dy, dw, dh))
        
        # Draw small pebbles
        for pebble in pebbles:
            px, py, pw, ph, pcolor = pebble
            pygame.draw.ellipse(screen, pcolor, 
                              (center_x + px, center_y + py, pw, ph))
            pygame.draw.ellipse(screen, (pcolor[0]-10, pcolor[1]-10, pcolor[2]-10), 
                              (center_x + px, center_y + py, pw, ph), 1)
        
        # Draw ripples
        for ripple in pond_ripples:
            temp_surf = pygame.Surface((ripple["size"]*2, ripple["size"]*2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (255, 255, 255, ripple["alpha"]), 
                              (ripple["size"], ripple["size"]), ripple["size"], 2)
            screen.blit(temp_surf, (center_x - ripple["size"], center_y + 100 - ripple["size"]))
        
        # Draw duck body with shading (unchanged from previous version)
        pygame.draw.circle(screen, ducky_yellow, (center_x, center_y + bounce_offset - 10), 60)
        pygame.draw.ellipse(screen, ducky_shade, (center_x - 60, center_y + bounce_offset - 50, 120, 100))
        pygame.draw.circle(screen, ducky_highlight, (center_x + 20, center_y + bounce_offset - 30), 10)
        
        # Draw duck head (unchanged from previous version)
        head_pos = (center_x + 40, center_y - 30 + bounce_offset)
        pygame.draw.circle(screen, ducky_yellow, head_pos, 30)
        
        # Draw cute face (unchanged from previous version)
        pygame.draw.circle(screen, (0, 0, 0), (head_pos[0] + 15, head_pos[1] - 10), 5)  # Eye
        pygame.draw.circle(screen, eye_highlight, (head_pos[0] + 16, head_pos[1] - 11), 2)  # Eye sparkle
        pygame.draw.circle(screen, blush_color, (head_pos[0] + 5, head_pos[1] + 5), 5)  # Blush
        pygame.draw.circle(screen, blush_color, (head_pos[0] + 25, head_pos[1] + 5), 5)  # Blush
        
        # Draw beak (unchanged from previous version)
        beak_points = [
            (head_pos[0] + 13, head_pos[1]),
            (head_pos[0] + 48, head_pos[1] + 10),
            (head_pos[0] + 13, head_pos[1] + 20),
            (head_pos[0] + 23, head_pos[1] + 10)
        ]
        pygame.draw.polygon(screen, (255, 140, 0), beak_points)
        pygame.draw.lines(screen, (230, 120, 0), True, beak_points[:3], 2)
        
        # Draw text with outline effect (unchanged from previous version)
        text_pos = (center_x - text.get_width()//2, center_y - 150)
        for dx, dy in [(1,1), (-1,1), (1,-1), (-1,-1)]:
            screen.blit(text_outline, (text_pos[0] + dx, text_pos[1] + dy))
        screen.blit(text, text_pos)
        
        # Draw cute sparkles occasionally (unchanged from previous version)
        if random.random() < 0.05:
            sparkle_x = random.randint(center_x - 100, center_x + 100)
            sparkle_y = random.randint(center_y - 200, center_y - 50)
            pygame.draw.circle(screen, (255, 255, 255), (sparkle_x, sparkle_y), 3)
            pygame.draw.line(screen, (255, 255, 255), (sparkle_x-5, sparkle_y), (sparkle_x+5, sparkle_y), 2)
            pygame.draw.line(screen, (255, 255, 255), (sparkle_x, sparkle_y-5), (sparkle_x, sparkle_y+5), 2)
        
        pygame.display.flip()
        pygame.time.delay(16)

# Daily quests
daily_quests = {
    "earn_money": {"target": 0, "progress": 0, "reward": 0, "completed": False},
    "rebirth": {"target": 0, "progress": 0, "reward": 0, "completed": False},
    "buy_automaters": {"target": 0, "progress": 0, "reward": 0, "completed": False},
    "buy_upgrades": {"target": 0, "progress": 0, "reward": 0, "completed": False},
    "gamble": {"target": 0, "progress": 0, "reward": 0, "completed": False},
    "mystery_boxes": {"target": 0, "progress": 0, "reward": 0, "completed": False},
    "play_time": {"target": 0, "progress": 0, "reward": 0, "completed": False}
}

# Infinite chain quests
infinite_quests = {
    "earn_money": {"targets": [10_000, 100_000, 1_000_000, 10_000_000, 100_000_000, 1_000_000_000, 10_000_000_000, 100_000_000_000, 1_000_000_000_000, 10_000_000_000_000, 100_000_000_000_000, 10_000_000_000_000_000],
                  "current_index": 0, "progress": 0, "reward": 0},
    "rebirth": {"targets": [1, 5, 10, 50, 100, 200, 500, 1000, 2000, 5000],
               "current_index": 0, "progress": 0, "reward": 0},
    "automaters": {"targets": [5, 10, 15, 20, 25, 30, 100, 200, 300, 400, 500, 10000],
                  "current_index": 0, "progress": 0, "reward": 0},
    "upgrades": {"targets": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000],
                "current_index": 0, "progress": 0, "reward": 0}
}

# Track last daily quest reset
last_daily_reset = datetime.date.today()

# Colors
colors = {
    "black": (25, 25, 25),
    "white": (255, 255, 255),
    "gray": (150, 150, 150),
    "green": (128, 255, 128),
    "red": (255, 128, 128),
    "blue": (128, 128, 255),
    "purple": (200, 128, 255),
    "orange": (255, 200, 128),
    "yellow": (255, 255, 128),
    "cyan": (128, 255, 255),
    "magenta": (255, 160, 255),
    "beige": (255, 220, 180),
    "trueGreen": (0, 255, 0),
    "trueRed": (255, 0, 0),
    "trueBlue": (50, 50, 255),
    "trueWhite": (255, 255, 255),
    "truePurple": (128, 0, 128),
    "trueOrange": (255, 127, 0),
    "trueYellow": (255, 255, 0),
    "trueCyan": (0, 255, 255),
    "trueMagenta": (255, 0, 255),
    "trueBeige": (189, 154, 122),
    "darkGreen": (2, 48, 32),
    "darkRed": (139, 0, 0),
    "darkBlue": (0, 0, 139),
    "pearl": (226, 223, 210),
    "darkPurple": (48, 25, 52),
    "darkOrange": (139, 64, 0),
    "darkYellow": (139, 128, 0),
    "teal": (0, 128, 128),
    "mulberry": (119, 7, 55),
    "tan": (210, 180, 140)
}
# quests


# Daily reward
import time

# Achievement
claimed = False

# Daily Reward Button
daily_reward_button = pygame.Rect(670, 600, 150, 50)

# Add Achievements Button (below daily reward)
achievements_button = pygame.Rect(670, 660, 150, 50)
achievements_menu_open = False

# Add a variable to track the last time the player claimed the daily reward
last_daily_reward_time = 0

# Function to check if the player is eligible to claim the daily reward
def can_claim_daily_reward():
    global last_daily_reward_time
    current_time = time.time()
    return current_time - last_daily_reward_time >= 86400  # 86400 seconds in a day

# Function to get the remaining time until the next daily reward
def get_time_until_next_daily_reward():
    global last_daily_reward_time
    current_time = time.time()
    remaining_time = 86400 - (current_time - last_daily_reward_time)
    if remaining_time < 0:
        remaining_time = 0
    hours, remainder = divmod(remaining_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

# Function to claim the daily reward
def claim_daily_reward():
    global score, last_daily_reward_time, claimed
    if can_claim_daily_reward():
        daily_reward_amount = random.randint(100,1000)  # Example reward amount
        score += daily_reward_amount
        claimed = True
        last_daily_reward_time = time.time()
        print(f"Daily reward claimed! You received £{daily_reward_amount}.")
    else:
        print("You have already claimed your daily reward. Please try again later.")

def gamble(amount):
    global score, earnings, losings, allIn, bankrupt

    if score >= amount:
        if score == amount:
            allIn = True
        else:
            allIn = False

        score -= amount

        weights = [0.3, 0.6, 0.1]
        result = random.choices(["win", "lose", "jackpot"], weights=weights, k=1)[0]

        if result == "win":
            winnings = amount * 2
            score += winnings
            earnings += winnings - amount
            print(f"You won £{winnings}!")
            show_gamble_popup(f"You won £{winnings}!", (0, 128, 0))
        elif result == "jackpot":
            winnings = amount * 10
            score += winnings
            earnings += winnings - amount
            print(f"You won the jackpot! £{winnings}!")
            show_gamble_popup(f"JACKPOT! £{winnings}!", (255, 140, 0))
        elif result == "lose":
            print("You lost!")
            show_gamble_popup("You lost!", (200, 0, 0))
            losings += amount
            if allIn:
                bankrupt = True
    else:
        print("Not enough money to gamble!")
        show_gamble_popup("Not enough money!", (200, 0, 0))

# Upgrades maxed
maxed_upgrades = 0
upgrades_bought = 0

screen = pygame.display.set_mode((1500, 890),
                                 pygame.RESIZABLE)
pygame.display.set_caption(f'Colors of Fortune Version: {version}')
background = colors["black"]
framerate = 60
font = pygame.font.Font('freesansbold.ttf' , 12)
font1 = pygame.font.SysFont("Arial", 12)
popup_font = pygame.font.SysFont("Arial", 20)
timer = pygame.time.Clock()

# Set up the text input box
input_box = pygame.Rect(670, 840, 200, 30)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active_input_box = None
text = ''
text_input = pygame.Rect(670, 840, 200, 30)  # Define text_input

# Define new frame properties
new_frame_coords = (1170, 200)
new_frame_size = (260, 200)

# Set up the amount input box
amount_input_box = pygame.Rect(new_frame_coords[0] + 10, new_frame_coords[1] + new_frame_size[1] - 40, 200, 30)
amount_text = ''
amount_color = color_inactive

secret_words = {}
with open('secret_codes.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            parts = line.split(':')
            if len(parts) == 2:
                code = parts[0].strip()
                reward = parts[1].strip()
                try:
                    secret_words[code] = int(reward)
                except ValueError:
                    print(f"Invalid reward value for code '{code}': {reward}")

used_words = set()
awesome = False
use_word = 0

# Define box properties within the window boundaries
box1_coords = (1175, 5)
box1_size = (250, 30)
box2_coords = (1175, 30)
box2_size = (250, 160)
inner_box_padding = 5
inner_box_coords = (1175, 30)
inner_box_size =(250, 80)

# Create the text surface for the text box
text_surface = font.render("Mystery Boxes", True, colors["white"])

# Create text surfaces for inner boxes
box_costs = [100, 500, 1000]
text_surfaces_costs = [font.render(f"${cost}", True, colors["white"]) for cost in box_costs]

# Gambling Buttons
all_in_button = pygame.Rect(amount_input_box.x + amount_input_box.width - 200, amount_input_box.y - 100, 80, 30)
half_button = pygame.Rect(amount_input_box.x + amount_input_box.width - 100, amount_input_box.y - 100, 80, 30)

# Set up achievement popup
popups = []
popup_queue = []
popup_timer = 0
popup_duration = 2000  # milliseconds (2 seconds)

# Gamble popups
gamble_popups = []
gamble_popup_queue = []
gamble_popup_timer = 0
gamble_popup_duration = 1200  # milliseconds (1.2 seconds)

# Box popups
box_popups = []
box_popup_queue = []
box_popup_timer = 0
box_popup_duration = 2000  # 2 seconds

popup_texts = [
    ("Code Cracker - Achievement", "Use An Input Code"), #0
    ("First Thousands - Achievement", "Earn £10K"), #1
    ("Colour Connoisseur - Achievement", "Buy 5 Automators"), #2
    ("Big leauges - Achievement", "Earn £100,000"), #3
    ("Hue Hunter - Achievement", "Buy 20 Automators"), #4
    ("Millionair - Achievement", "Earn £1M"), #5
    ("Money Master - Achievement", "Earn $10M"), #6
    ("Fortune Finder - Achievement", "Earn $25M"), #7
    ("Golden Goose - Achievement", "Earn $50M"), #8
    ("Rainbow Raider - Achievement", "Buy 10 Automators"), #9
    ("Pigment Prodigy - Achievement", "Buy 15 Automators"), #10
    ("Chromatic Champion - Achievement", "Buy all 30 Automators"), #11
    ("Multi-Millionaire - Achievement", "Earn $100M"), #12
    ("Achievement Hunter - Achievement", "Unlock Every Achievement"), #13
    ("Prestige Perfection - Achievement", "Prestige 1 times"), #14
    ("Awesome Sauce - Achievement", "You are Awesome!"), #15 HIDDEN
    ("Pet Lover - Achievement", "Unlock all pets"), #16
    ("Title Master - Achievement", "Unlock all titles"), #17
    ("Mystery Solver - Achievement", "Open 10 mystery boxes"), #18
    ("Billionair - Achievement", "Earn $1B"), #19
    ("Ultimate Prestige - Achievement", "Prestige 10 times"), #20
    ("Mystery Box Master - Achievement", "Open 50 mystery boxes"), #21
    ("So Many Secrets - Achievement", "Use all secret codes"), #22
    ("Winner Winner Chicken Dinner - Achievment", "Earn over £200k while gambling"), #23
    ("Not Everyone Wins - Achievement", "Lose over £200k while gambling"), #24
    ("Rock Bottom - Achievement", "Go bankrupt while gambling"), #25
    ("All In - Achievement", "Go all in while gambling"), #26
    ("Upgrade God - Achievement", "Max out one colors upgrades"), #27
    ("Upgrade Champion - Achievement", "Max out 15 color upgrades"), #28
    ("Upgrade God - Achievement","Max out ALL color upgrades" ), #29
    ("Mr Money Bags - Achievement","Earn £1T"), #30
    ("WHY WOULD YOU DO THIS - Achievement","Earn £1QD"), #31
    ("Daily Reward - Achievement", "Claim your daily reward"), #32
    ("Playtime - Achievement", "Play for 1 hour"), #33
    ("Playtime 2 - Achievement", "Play for 5 hours"), #34
    ("Playtime 3 - Achievement", "Play for 10 hours"), #35
    ("Playtime 4 - Achievement", "Play for 50 hours"), #36
    ("Playtime 5 - Achievement", "Play for 100 hours"), #37
    ("Playtime 6 - Achievement", "Play for 500 hours"), #38
    ("Playtime 7 - Achievement", "Play for 1000 hours"), #39
]

def unlock_achievement(index):
    global achievements_unlocked
    if not achievements[index]["unlocked"]:
        achievements[index]["unlocked"] = True
        achievements_unlocked += 1
        popup_queue.append(index)

for text1, text2 in popup_texts:
    popup = pygame.Surface((400, 100))
    popup.fill(colors["white"])
    popup.set_alpha(255)  # Make the popup not see-through
    popup_text1 = popup_font.render(text1, True, colors["black"])
    popup_text2 = popup_font.render(text2, True, colors["black"])
    popup.blit(popup_text1, (popup.get_width() // 2 - popup_text1.get_width() // 2, 25))
    popup.blit(popup_text2, (popup.get_width() // 2 - popup_text2.get_width() // 2, 45))
    popups.append(popup)

# Function to display achievement popup and pause the game for a short time
def display_achievement_popup(index):
    screen.blit(popups[index], (screen.get_width() // 2 - popups[index].get_width() // 2, screen.get_height() // 2 - popups[index].get_height() // 2))
    pygame.display.update()
    pygame.time.wait(3000)

def show_gamble_popup(message, color=(0, 0, 0)):
    popup = pygame.Surface((250, 40))
    popup.fill((255, 255, 255))
    popup.set_alpha(230)
    text = font.render(message, True, color)
    popup.blit(text, (popup.get_width() // 2 - text.get_width() // 2, 10))
    gamble_popups.append(popup)
    gamble_popup_queue.append(len(gamble_popups) - 1)

def show_box_popup(name, rarity):
    popup = pygame.Surface((200, 60))
    popup.fill((255, 255, 255))
    popup.set_alpha(230)
    text1 = font.render(f"You unboxed: {name}", True, (0, 0, 0))
    text2 = font.render(f"Rarity: {rarity}", True, (0, 0, 0))
    popup.blit(text1, (20, 10))
    popup.blit(text2, (20, 30))
    box_popups.append(popup)
    box_popup_queue.append(len(box_popups) - 1)

# Function to save game progress
def save_game():
    global score, managers_owned, base_multiplier, extra_multiplier, unlocked_titles, current_title, prestige_cost, prestiges, current_pet, unlocked_pets, used_words, claimed, last_daily_reward_time, achievements, achievements_unlocked, mystery_boxes_opened, color_values, color_lengths, color_speeds, color_costs, color_owned, color_manager_costs, time_spent, daily_quest_progress
    save_data = {
        'score': score,
        'managers_owned': managers_owned,
        'base_multiplier': base_multiplier,
        'extra_multiplier': extra_multiplier,
        'prestige_cost': prestige_cost,
        'prestiges': prestiges,
        'unlocked_pets': unlocked_pets,
        'unlocked_titles': unlocked_titles,
        'current_title': current_title,
        'current_pet': current_pet,
        'used_words': used_words,
        'claimed': claimed,
        'last_daily_reward_time': last_daily_reward_time,
        'achievements': achievements,
        'achievements_unlocked': achievements_unlocked,
        'mystery_boxes_opened': mystery_boxes_opened,
        'color_values': color_values,
        'color_lengths': color_lengths,
        'color_speeds': color_speeds,
        'color_costs': color_costs,
        'color_owned': color_owned,
        'color_manager_costs': color_manager_costs,
        'time_spent': Time_Spent,
        'daily_quest_progress': daily_quest_progress,
    }
    with open('savegame.pkl', 'wb') as save_file:
        pickle.dump(save_data, save_file)
    print("Game saved successfully.")

# Function to load saved game
def load_game():
    global score, managers_owned, base_multiplier, extra_multiplier, unlocked_titles, current_title, prestige_cost, prestiges, current_pet, unlocked_pets, used_words, claimed, last_daily_reward_time, achievements, achievements_unlocked, mystery_boxes_opened, color_values, color_lengths, color_speeds, color_costs, color_owned, color_manager_costs, Time_Spent, daily_quest_progress
    if os.path.exists('savegame.pkl'):
        with open('savegame.pkl', 'rb') as save_file:
            save_data = pickle.load(save_file)
            score = save_data.get('score', 0)
            managers_owned = save_data.get('managers_owned', 0)
            base_multiplier = save_data.get('base_multiplier', 1)
            extra_multiplier = save_data.get('extra_multiplier', 0)
            prestige_cost = save_data.get('prestige_cost', 1000000)
            prestiges = save_data.get('prestiges', 0)
            unlocked_pets = save_data.get('unlocked_pets', ["None"])
            unlocked_titles = save_data.get('unlocked_titles', ["Beginner"])
            current_title = save_data.get('current_title', "Beginner")
            current_pet = save_data.get('current_pet', "None")
            used_words = save_data.get('used_words', set())
            claimed = save_data.get('claimed', False)
            last_daily_reward_time = save_data.get('last_daily_reward_time', 0)
            achievements = save_data.get('achievements', [])
            achievements_unlocked = save_data.get('achievements_unlocked', 0)
            mystery_boxes_opened = save_data.get('mystery_boxes_opened', 0)
            color_values = save_data.get('color_values', {})
            color_lengths = save_data.get('color_lengths', {})
            color_speeds = save_data.get('color_speeds', {})
            color_costs = save_data.get('color_costs', {})
            color_owned = save_data.get('color_owned', {})
            color_manager_costs = save_data.get('color_manager_costs', {})
            Time_Spent = save_data.get('time_spent', 0)
            daily_quest_progress = save_data.get('daily_quest_progress', {})
        print("Game loaded successfully.")
    else:
        print("No saved game found.")

# Function to draw the mystery box menu
def draw_mystery_box_menu():
    # Draw Titles Box
    titles_box = pygame.draw.rect(screen, colors["blue"], [1250, 50, 150, 50])
    formatted_titles_cost = format_number(mystery_box_costs['titles'])
    titles_text = font.render(f"Titles Box - £{formatted_titles_cost}", True, colors["black"])
    screen.blit(titles_text, (1275, 65))

    # Draw Pets Box
    pets_box = pygame.draw.rect(screen, colors["green"], [1250, 120, 150, 50])
    formatted_pets_cost = format_number(mystery_box_costs['pets'])
    pets_text = font.render(f"Pets Box - £{formatted_pets_cost}", True, colors["black"])
    screen.blit(pets_text, (1275, 135))

    return titles_box, pets_box

#game variables

achievements_total = len(popup_texts)
achievements_unlocked = 0

# Achievement values and states
achievements = [
    {"value": 0, "unlocked": False}, # Code Cracker
    {"value": 10000, "unlocked": False}, # Treasure Trove
    {"value": 1, "unlocked": False}, # Colour Connoisseur
    {"value": 100000, "unlocked": False}, # Riches Runner
    {"value": 1, "unlocked": False}, # Hue Hunter
    {"value": 1000000, "unlocked": False}, # Wealth Accumulator
    {"value": 10000000, "unlocked": False}, # Money Master
    {"value": 25000000, "unlocked": False}, # Fortune Finder
    {"value": 50000000, "unlocked": False}, # Golden Goose
    {"value": 1, "unlocked": False}, # Rainbow Raider
    {"value": 1, "unlocked": False}, # Pigment Prodigy
    {"value": 1, "unlocked": False}, # Chromatic Champion
    {"value": 100000000, "unlocked": False}, # Multi-Millionaire
    {"value": 1, "unlocked": False}, # Achievement Hunter
    {"value": 1, "unlocked": False}, # Prestige Perfection
    {"value": 1, "unlocked": False}, # Awesome Sauce
    {"value": 1, "unlocked": False}, # Pet Lover
    {"value": 1, "unlocked": False}, # Title Master
    {"value": 1, "unlocked": False}, # Mystery Solver
    {"value": 1000000000, "unlocked": False}, # Money Hoarder
    {"value": 1, "unlocked": False}, # Ultimate Prestige
    {"value": 1, "unlocked": False}, # Mystery Box Master
    {"value": 1, "unlocked": False}, # Shh dont tell
    {"value": 1, "unlocked": False}, # Gambling Addict
    {"value": 1, "unlocked": False}, # Not Everyone Wins
    {"value": 1, "unlocked": False}, # Bankrupt
    {"value": 1, "unlocked": False}, # All In
    {"value": 1, "unlocked": False}, # Upgrade Master
    {"value": 1, "unlocked": False}, # Upgrade Champion
    {"value": 1, "unlocked": False}, # Upgrade God
    {"value": 1000000000000, "unlocked": False}, # Mr Money Bags
    {"value": 1000000000000000,"unlocked": False}, # WHY WOULD YOU DO THIS
    {"value": 1, "unlocked": False}, # Daily Reward
    {"value": 1, "unlocked": False}, # Playtime 1
    {"value": 1, "unlocked": False}, # Playtime 2
    {"value": 1, "unlocked": False}, # Playtime 3
    {"value": 1, "unlocked": False}, # Playtime 4
    {"value": 1, "unlocked": False}, # Playtime 5
    {"value": 1, "unlocked": False}, # Playtime 6
    {"value": 1, "unlocked": False}, # Playtime 7
]

# Values, lengths, and speeds for colors
color_values = {
    "green": 1, "red": 2, "orange": 3, "white": 4, "purple": 5, "blue": 6,
    "yellow": 7, "cyan": 8, "magenta": 9, "beige": 10, "trueGreen": 11,
    "trueRed": 12, "trueOrange": 13, "trueWhite": 14, "truePurple": 15,
    "trueBlue": 16, "trueYellow": 17, "trueCyan": 18, "trueMagenta": 19,
    "trueBeige": 20, "darkGreen": 21, "darkRed": 22, "darkOrange": 23,
    "pearl": 24, "darkPurple": 25, "darkBlue": 26, "darkYellow": 27,
    "teal": 28, "mulberry": 29, "tan": 30
}

color_lengths = {color: 0 for color in color_values}
color_speeds = {
    "green": 5,  "red": 7, "orange": 9, "white": 11, "purple": 13, "blue": 15,
    "yellow": 17, "cyan": 19, "magenta": 21, "beige": 23, "trueGreen": 25,
    "trueRed": 27, "trueOrange": 29, "trueWhite": 31, "truePurple": 33,
    "trueBlue": 35, "trueYellow": 37, "trueCyan": 39, "trueMagenta": 41,
    "trueBeige": 43, "darkGreen": 45, "darkRed": 47, "darkOrange": 49,
    "pearl": 51, "darkPurple": 53, "darkBlue": 55, "darkYellow": 57,
    "teal": 59, "mulberry": 61, "tan": 63
}

# Draw buttons function
color_costs = {color: value for color, value in color_values.items()}
color_owned = {color: False for color in color_values}
color_manager_costs = {
    "green": 1000, "red": 3000, "orange": 5000, "white": 7000, "purple": 9000,
    "blue": 15000, "yellow": 25000, "cyan": 45000, "magenta": 80000, "beige": 150000,
    "trueGreen": 200000, "trueRed": 250000, "trueOrange": 300000, "trueWhite": 400000,
    "truePurple": 550000, "trueBlue": 700000, "trueYellow": 750000, "trueCyan": 800000,
    "trueMagenta": 840000, "trueBeige": 960000, "darkGreen": 1175000, "darkRed": 1350000,
    "darkOrange": 1575000, "pearl": 1800000, "darkPurple": 2150000, "darkBlue": 3115000,
    "darkYellow": 2475000, "teal": 3450000, "mulberry": 3770000, "tan": 4000000
}

# Initialize draw_<color> variables and unlocked status
for i, color in enumerate(color_values):
    globals()[f"draw_{color}"] = False
    globals()[f"{color}_unlocked"] = i < 5  # Unlock the first 5 buttons initially

# Draw task function
def draw_task(color, y_coord, x_coord, value, draw, length, speed, unlocked):
    global score
    task_color = colors[color] if unlocked else colors["gray"]

    if draw and length < 200:
        length += 200 / (speed * framerate)
    elif length >= 200:
        draw = False
        length = 0
        score += value * total_multiplier

    # Calculate time left
    time_left = speed - (length / (200 / speed))
    time_left_text = font.render(f"{time_left:.1f}s", True, colors["trueWhite"])

    task = pygame.draw.circle(screen, task_color, (x_coord, y_coord), 25, 5)
    pygame.draw.rect(screen, task_color, [x_coord + 40, y_coord - 15, 200, 30])
    pygame.draw.rect(screen, colors["black"], [x_coord + 45, y_coord - 10, 190, 20])
    pygame.draw.rect(screen, task_color, [x_coord + 40, y_coord - 15, length, 30])
    value_text = font.render(str(round(value, 2)), True, colors["trueWhite"])
    screen.blit(value_text, (x_coord - 14, y_coord - 10))
    screen.blit(time_left_text, (x_coord + 200, y_coord - 5))  # Adjust position as needed

    return task, length, draw

# Combined draw buttons function
def draw_buttons(color, x_coord, row, cost, owned, manager_cost, unlocked, speed, maxed_upgrades):
    # Define Y positions for each row
    row_y_positions = [595, 630, 665]
    manager_y_positions = [715, 750, 785]

    y_coord = row_y_positions[row]  # Get the Y position based on the row
    manager_y = manager_y_positions[row]  # Get the manager button position

    # Check if speed is at max upgrade level (0.5 or lower)
    maxed_out = speed <= 0.5

    # Draw upgrade button
    if unlocked:
        if maxed_out:
            color_button = pygame.draw.rect(screen, colors["gray"], [x_coord, y_coord, 50, 30])
            max_text = font.render("MAX", True, colors["black"])
            screen.blit(max_text, (x_coord + 10, y_coord + 5))
        else:
            color_button = pygame.draw.rect(screen, colors[color], [x_coord, y_coord, 50, 30])
            formatted_cost = "£" + format_number(cost)
            color_cost = font.render(formatted_cost, True, colors["black"])
            screen.blit(color_cost, (x_coord + 6, y_coord + 5))
    else:
        color_button = pygame.draw.rect(screen, colors["gray"], [x_coord, y_coord, 50, 30])
        lock_text = font.render("Locked", True, colors["black"])
        screen.blit(lock_text, (x_coord + 6, y_coord + 5))

    # Draw manager button
    if not owned:
        if unlocked:
            manager_button = pygame.draw.rect(screen, colors[color], [x_coord, manager_y, 50, 30])
            formatted_manager_cost = "£" + format_number(manager_cost)
            manager_text = font.render(formatted_manager_cost, True, colors["black"])
            screen.blit(manager_text, (x_coord + 6, manager_y + 5))
        else:
            manager_button = pygame.draw.rect(screen, colors["gray"], [x_coord, manager_y, 50, 30])
            lock_text = font.render("Locked", True, colors["black"])
            screen.blit(lock_text, (x_coord + 6, manager_y + 5))
    else:
        manager_button = pygame.draw.rect(screen, colors["black"], [x_coord, manager_y, 50, 30])

    return color_button, manager_button

# Handle secret word input
def handle_secret_word_input(cash):
    if text_input.get_text() == cash:
        money += 100
        text = ''

# Define global multipliers
title_multipliers = {
    "Beginner": 1, "Awesome Sauce": 5, "Developer": 15, "Money Bags": 2,
    "Explorer": 3, "Adventurer": 2, "Champion": 5, "Gambler": 4, "WTF": 20
}
pet_multipliers = {
        "None": 0, "Dog": 1, "Cat": 2, "Dragon": 3, "Phoenix": 4, "Unicorn": 5,
        "Reindeer": 10, "Easter Bunny": 8, "Ghost": 7, "Firework Dragon": 12,
        "Leprechaun": 9, "Cupid": 6, "Eagle": 11, "Turkey": 5, "Parrot": 6, "Shark": 20,
        "Plumber": 15, "Rubber Ducky": 100,
}

# Update the pet_multipliers dictionary to include special pets
pet_multipliers.update({pet["name"]: pet["mult"] for pet in special_pets.values()})

# Set multiplier based on current title and pet
def set_multiplier():
    global base_multiplier, extra_multiplier, total_multiplier
    base_multiplier = title_multipliers.get(current_title, 1) + prestiges
    pet_multiplier = pet_multipliers.get(current_pet, 0)
    total_multiplier = base_multiplier + extra_multiplier + pet_multiplier

    return total_multiplier

# Function to format large numbers with suffixes
def format_number(n):
    if n >= 1_000_000_000_000_000:
        return f"{n / 1_000_000_000_000:.1f}Qd"
    if n >= 1_000_000_000_000:
        return f"{n / 1_000_000_000:.1f}T"
    if n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.1f}B"
    elif n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}K"
    else:
        return str(n)

# Draw dropdown menu with multipliers
def draw_dropdown_menu():
    global dropdown_interacting
    dropdown_interacting = False
    pygame.draw.rect(screen, colors["white"], dropdown_rect, 2)
    title_text = font.render(f"{current_title} (x{title_multipliers.get(current_title, 1)} multiplier)", True, colors["white"])
    screen.blit(title_text, (dropdown_rect.x + 5, dropdown_rect.y + 5))
    pygame.draw.polygon(screen, colors["white"], [(dropdown_rect.x + dropdown_rect.width - 20, dropdown_rect.centery - 3),
                                                  (dropdown_rect.x + dropdown_rect.width - 10, dropdown_rect.centery - 3),
                                                  (dropdown_rect.x + dropdown_rect.width - 15, dropdown_rect.centery + 3)])
    if menu_expanded:
        dropdown_interacting = True
        for i, option_rect in enumerate(dropdown_options_rects):
            pygame.draw.rect(screen, colors["gray"], option_rect)
            option_text = font.render(f"{unlocked_titles[i]} (x{title_multipliers.get(unlocked_titles[i], 1)} multiplier)", True, colors["white"])
            screen.blit(option_text, (option_rect.x + 5, option_rect.y + 5))

# Draw pets dropdown menu with multipliers
def draw_pets_dropdown_menu():
    global pets_dropdown_interacting
    pets_dropdown_interacting = False
    pygame.draw.rect(screen, colors["white"], pets_dropdown_rect, 2)
    pet_text = font.render(f"{current_pet} (x{pet_multipliers.get(current_pet, 0)} multiplier)", True, colors["white"])
    screen.blit(pet_text, (pets_dropdown_rect.x + 5, pets_dropdown_rect.y + 5))
    pygame.draw.polygon(screen, colors["white"], [(pets_dropdown_rect.x + pets_dropdown_rect.width - 20, pets_dropdown_rect.centery - 3),
                                                  (pets_dropdown_rect.x + pets_dropdown_rect.width - 10, pets_dropdown_rect.centery - 3),
                                                  (pets_dropdown_rect.x + pets_dropdown_rect.width - 15, pets_dropdown_rect.centery + 3)])
    if pets_menu_expanded:
        pets_dropdown_interacting = True
        for i, option_rect in enumerate(pets_dropdown_options_rects):
            pygame.draw.rect(screen, colors["gray"], option_rect)
            option_text = font.render(f"{unlocked_pets[i]} (x{pet_multipliers.get(unlocked_pets[i], 0)} multiplier)", True, colors["white"])
            screen.blit(option_text, (option_rect.x + 5, option_rect.y + 5))

# Function to display the multiplier on the screen
def display_multiplier(total_multiplier):
    formatted_multiplier = format_number(total_multiplier)
    display_mult = font.render(f'Multiplier: x{formatted_multiplier}', True, colors["trueRed"], colors["black"])
    screen.blit(display_mult, (425, 860))

# Update the display functions to use the format_number function
def display_automators():
    formatted_automators = format_number(managers_owned)
    display_automators = font.render(f'Automators Bought: {formatted_automators} / 30', True, colors["trueRed"], colors["black"])
    screen.blit(display_automators, (425, 845))
    formatted_automators = format_number(upgrades_bought)
    display_upgrades = font.render(f'Upgrades Bought: {upgrades_bought} / 2010 ', True, colors["trueRed"], colors["black"])
    screen.blit(display_upgrades, (245, 845))

def display_prestige_cost():
    formatted_prestige_cost = format_number(prestige_cost)
    prestige_text = font.render(f'Prestige - £{formatted_prestige_cost}', True, colors["black"])
    screen.blit(prestige_text, (22, 835))

# Update the display functions to use the format_number function
def display_score():
    formatted_score = format_number(score)
    display_score = font.render(f'Money: £{formatted_score}', True, colors["trueRed"], colors["black"])
    screen.blit(display_score, (440, 5))


# Initialize close_button and prestige_button
close_button = None
prestige_button = None

# Add a variable to track the last time the time was updated
last_time_update = pygame.time.get_ticks()

# Add a variable to track the last time the save reminder was displayed
last_save_reminder_time = pygame.time.get_ticks()
save_reminder_interval = 300000 # 5 minutes in milliseconds

# RUNNING LOOP
running = True
achievements_menu_scroll_offset = 0
ACHIEVEMENTS_MENU_WIDTH = 650
ACHIEVEMENTS_MENU_HEIGHT = 600
ACHIEVEMENT_ROW_HEIGHT = 38  # Increased spacing
achievements_menu_scroll_offset = 0

# Add a new button for the quests menu (below achievements button)
quests_menu_button = pygame.Rect(670, 720, 150, 50)
quests_menu_open = False

# Add a new button for the flow free minigame (below quests menu)
flow_minigame_button = pygame.Rect(900, 720, 150, 50)
flow_minigame_open = False

while running:
    timer.tick(framerate)
    current_time = pygame.time.get_ticks()

    # Increment Time_Spent every second
    if current_time - last_time_update >= 1000:  # 1000 ms = 1 second
        Time_Spent += 1
        last_time_update = current_time

    draw_dropdown_menu()
    draw_pets_dropdown_menu()

    # Update dropdown options based on unlocked titles
    dropdown_options_rects = []  # Reset list before re-populating
    for i, _ in enumerate(unlocked_titles):
        option_rect = dropdown_rect.copy()
        option_rect.y += (i + 1) * dropdown_rect.height  # Offset for each option
        dropdown_options_rects.append(option_rect)

    # Update dropdown options based on unlocked pets
    pets_dropdown_options_rects = []  # Reset list before re-populating
    for i, _ in enumerate(unlocked_pets):
        option_rect = pets_dropdown_rect.copy()
        option_rect.y += (i + 1) * pets_dropdown_rect.height  # Offset for each option
        pets_dropdown_options_rects.append(option_rect)

    # Calculate total multiplier including extra features
    total_multiplier = set_multiplier()

    for color in color_owned:
        if color_owned[color] and not globals()[f"draw_{color}"]:
            globals()[f"draw_{color}"] = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Achievements menu scroll and close logic
        if achievements_menu_open:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Mouse wheel scroll
                if event.button == 4:  # Scroll up
                    achievements_menu_scroll_offset = max(achievements_menu_scroll_offset - 30, 0)
                elif event.button == 5:  # Scroll down
                    max_scroll = max(0, len(popup_texts) * 30 - (ACHIEVEMENTS_MENU_HEIGHT - 450))
                    achievements_menu_scroll_offset = min(achievements_menu_scroll_offset + 30, max_scroll)
                # Close button click
                mouse_x, mouse_y = event.pos
                close_ach_rect = pygame.Rect(600 + ACHIEVEMENTS_MENU_WIDTH - 120, 200, 100, 40)
                if close_ach_rect.collidepoint(mouse_x, mouse_y):
                    achievements_menu_open = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    achievements_menu_scroll_offset = max(achievements_menu_scroll_offset - 30, 0)
                elif event.key == pygame.K_DOWN:
                    max_scroll = max(0, len(popup_texts) * 30 - (ACHIEVEMENTS_MENU_HEIGHT - 100))
                    achievements_menu_scroll_offset = min(achievements_menu_scroll_offset + 30, max_scroll)

        # --- Add quests menu scroll/close logic here if needed ---
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Color tasks and managers
                for i, color in enumerate(color_values):
                    if globals()[f"task_{color}"].collidepoint((mouse_x, mouse_y)) and globals()[f"{color}_unlocked"]:
                        globals()[f"draw_{color}"] = True
                    if globals()[f"{color}_manager_buy"].collidepoint((mouse_x, mouse_y)) and score >= color_manager_costs[color] and not color_owned[color] and globals()[f"{color}_unlocked"]:
                        color_owned[color] = True
                        managers_owned += 1
                        score -= color_manager_costs[color]
                        if i < len(color_values) - 1:
                            next_color = list(color_values.keys())[i + 1]
                            globals()[f"{next_color}_unlocked"] = True
                    if globals()[f"{color}_buy"].collidepoint((mouse_x, mouse_y)) and score >= color_costs[color] and globals()[f"{color}_unlocked"] and color_speeds[color] > 0.5:
                        score -= color_costs[color]
                        color_values[color] += 1
                        color_speeds[color] = max(0.5, color_speeds[color] - 0.5)
                        color_costs[color] += 5
                        upgrades_bought += 1
                        if color_speeds[color] == 0.5:
                            maxed_upgrades += 1

                # Dropdowns
                if dropdown_rect.collidepoint((mouse_x, mouse_y)):
                    menu_expanded = not menu_expanded
                elif menu_expanded:
                    for i, option_rect in enumerate(dropdown_options_rects):
                        if option_rect.collidepoint((mouse_x, mouse_y)):
                            current_title = list(unlocked_titles)[i]
                            menu_expanded = False

                if pets_dropdown_rect.collidepoint((mouse_x, mouse_y)):
                    pets_menu_expanded = not pets_menu_expanded
                elif pets_menu_expanded:
                    for i, option_rect in enumerate(pets_dropdown_options_rects):
                        if option_rect.collidepoint((mouse_x, mouse_y)):
                            current_pet = list(unlocked_pets)[i]
                            pets_menu_expanded = False

                # ACHIEVEMENT CHECKS 

                # 0: Use An Input Code
                if use_word >= 1 and not achievements[0]["unlocked"]:
                    unlock_achievement(0)
                # 1: Earn £10K
                if score >= 10_000 and not achievements[1]["unlocked"]:
                    unlock_achievement(1)
                # 2: Buy 5 Automators
                if managers_owned >= 5 and not achievements[2]["unlocked"]:
                    unlock_achievement(2)
                # 3: Earn £100,000
                if score >= 100_000 and not achievements[3]["unlocked"]:
                    unlock_achievement(3)
                # 4: Buy 20 Automators
                if managers_owned >= 20 and not achievements[4]["unlocked"]:
                    unlock_achievement(4)
                # 5: Earn £1M
                if score >= 1_000_000 and not achievements[5]["unlocked"]:
                    unlock_achievement(5)
                # 6: Earn $10M
                if score >= 10_000_000 and not achievements[6]["unlocked"]:
                    unlock_achievement(6)
                # 7: Earn $25M
                if score >= 25_000_000 and not achievements[7]["unlocked"]:
                    unlock_achievement(7)
                # 8: Earn $50M
                if score >= 50_000_000 and not achievements[8]["unlocked"]:
                    unlock_achievement(8)
                # 9: Buy 10 Automators
                if managers_owned >= 10 and not achievements[9]["unlocked"]:
                    unlock_achievement(9)
                # 10: Buy 15 Automators
                if managers_owned >= 15 and not achievements[10]["unlocked"]:
                    unlock_achievement(10)
                # 11: Buy all 30 Automators
                if managers_owned >= 30 and not achievements[11]["unlocked"]:
                    unlock_achievement(11)
                # 12: Earn $100M
                if score >= 100_000_000 and not achievements[12]["unlocked"]:
                    unlock_achievement(12)
                # 13: Complete Every Achievement
                if achievements_unlocked == achievements_total - 1 and not achievements[13]["unlocked"]:
                    unlock_achievement(13)
                # 14: Prestige 1 times
                if prestiges >= 1 and not achievements[14]["unlocked"]:
                    unlock_achievement(14)
                # 15: You are Awesome!
                if awesome and not achievements[15]["unlocked"]:
                    new_title10 = f"Awesome Sauce"
                    unlocked_titles.append(new_title10)
                    unlock_achievement(15)
                # 16: Unlock all pets
                if all(pet in unlocked_pets for pet in pets) and not achievements[16]["unlocked"]:
                    unlock_achievement(16)
                # 17: Unlock all titles
                if all(title in unlocked_titles for title in titles) and not achievements[17]["unlocked"]:
                    unlock_achievement(17)
                # 18: Open 10 mystery boxes
                if mystery_boxes_opened >= 10 and not achievements[18]["unlocked"]:
                    unlock_achievement(18)
                # 19: Earn $1B
                if score >= 1_000_000_000 and not achievements[19]["unlocked"]:
                    unlock_achievement(19)
                # 20: Prestige 10 times
                if prestiges >= 10 and not achievements[20]["unlocked"]:
                    unlock_achievement(20)
                # 21: Open 50 mystery boxes
                if mystery_boxes_opened >= 50 and not achievements[21]["unlocked"]:
                    unlock_achievement(21)
                # 22: Use all secret codes
                if len(used_words) == len(secret_words) and not achievements[22]["unlocked"]:
                    unlock_achievement(22)
                # 23: Earn over £200k while gambling
                if earnings >= 200_000 and not achievements[23]["unlocked"]:
                    unlock_achievement(23)
                # 24: Lose over £200k while gambling
                if losings >= 200_000 and not achievements[24]["unlocked"]:
                    unlock_achievement(24)
                # 25: Lose all your money while gambling
                if bankrupt and not achievements[25]["unlocked"]:
                    unlock_achievement(25)
                # 26: Go all in while gambling
                if allIn and not achievements[26]["unlocked"]:
                    unlock_achievement(26)
                # 27: Max out one color's upgrades
                if maxed_upgrades >= 1 and not achievements[27]["unlocked"]:
                    unlock_achievement(27)
                # 28: Max out 15 color upgrades
                if maxed_upgrades >= 15 and not achievements[28]["unlocked"]:
                    unlock_achievement(28)
                # 29: Max out ALL color upgrades (30)
                if maxed_upgrades >= 30 and not achievements[29]["unlocked"]:
                    unlock_achievement(29)
                # 30: Earn £1T
                if score >= 1_000_000_000_000 and not achievements[30]["unlocked"]:
                    unlock_achievement(30)
                # 31: Earn £1QD
                if score >= 1_000_000_000_000_000 and not achievements[31]["unlocked"]:
                    unlock_achievement(31)
                # 32: Claim your daily reward
                if claimed and not achievements[32]["unlocked"]:
                    unlock_achievement(32)
                # 33: Play for 1 hour
                if Time_Spent >= 3600 and not achievements[33]["unlocked"]:
                    unlock_achievement(33)
                # 34: Play for 5 hours
                if Time_Spent >= 5 * 3600 and not achievements[34]["unlocked"]:
                    unlock_achievement(34)
                # 35: Play for 10 hours
                if Time_Spent >= 10 * 3600 and not achievements[35]["unlocked"]:
                    unlock_achievement(35)
                # 36: Play for 50 hours
                if Time_Spent >= 50 * 3600 and not achievements[36]["unlocked"]:
                    unlock_achievement(36)
                # 37: Play for 100 hours
                if Time_Spent >= 100 * 3600 and not achievements[37]["unlocked"]:
                    unlock_achievement(37)
                # 38: Play for 500 hours
                if Time_Spent >= 500 * 3600 and not achievements[38]["unlocked"]:
                    unlock_achievement(38)
                # 39: Play for 1000 hours
                if Time_Spent >= 1000 * 3600 and not achievements[39]["unlocked"]:
                    unlock_achievement(39)

                # Mystery boxes
                titles_box, pets_box = draw_mystery_box_menu()
                if titles_box.collidepoint(mouse_x, mouse_y):
                    open_mystery_box("titles")
                elif pets_box.collidepoint(mouse_x, mouse_y):
                    open_mystery_box("pets")

                # Casino buttons
                if all_in_button.collidepoint((mouse_x, mouse_y)):
                    gamble(score)
                elif half_button.collidepoint((mouse_x, mouse_y)):
                    gamble(score // 2)

                # Daily reward
                if daily_reward_button.collidepoint((mouse_x, mouse_y)):
                    claim_daily_reward()

                # Achievements button
                if achievements_button.collidepoint((mouse_x, mouse_y)):
                    achievements_menu_open = not achievements_menu_open

                # quests menu button
                if quests_menu_button.collidepoint((mouse_x, mouse_y)):
                    quests_menu_open = not quests_menu_open

                # If achievements menu is open, check for close button
                if achievements_menu_open:
                    close_ach_rect = pygame.Rect(600 + ACHIEVEMENTS_MENU_WIDTH - 120, 200, 100, 40)
                    if close_ach_rect.collidepoint((mouse_x, mouse_y)):
                        achievements_menu_open = False

                # Prestige
                if prestige_button and prestige_button.collidepoint((mouse_x, mouse_y)):
                    prestige_menu_open = True
                if prestige_menu_open and close_button and close_button.collidepoint((mouse_x, mouse_y)):
                    prestige_menu_open = False
                if prestige_menu_open and prestige_button and prestige_button.collidepoint((mouse_x, mouse_y)) and score >= prestige_cost:
                    score -= prestige_cost
                    prestige_cost += 1000000
                    upgrades_bought = 0
                    maxed_upgrades = 0
                    extra_multiplier += 1
                    prestiges += 1
                    base_multiplier += prestiges
                    prestige_menu_open = False
                    score = 100
                    managers_owned = 0
                    extra_multiplier = 0
                    color_values = {
                        "green": 1, "red": 2, "orange": 3, "white": 4, "purple": 5, "blue": 6,
                        "yellow": 7, "cyan": 8, "magenta": 9, "beige": 10, "trueGreen": 11,
                        "trueRed": 12, "trueOrange": 13, "trueWhite": 14, "truePurple": 15,
                        "trueBlue": 16, "trueYellow": 17, "trueCyan": 18, "trueMagenta": 19,
                        "trueBeige": 20, "darkGreen": 21, "darkRed": 22, "darkOrange": 23,
                        "pearl": 24, "darkPurple": 25, "darkBlue": 26, "darkYellow": 27,
                        "teal": 28, "mulberry": 29, "tan": 30
                    }
                    color_lengths = {color: 0 for color in color_values}
                    color_speeds = {
                        "green": 5,  "red": 7, "orange": 9, "white": 11, "purple": 13, "blue": 15,
                        "yellow": 17, "cyan": 19, "magenta": 21, "beige": 23, "trueGreen": 25,
                        "trueRed": 27, "trueOrange": 29, "trueWhite": 31, "truePurple": 33,
                        "trueBlue": 35, "trueYellow": 37, "trueCyan": 39, "trueMagenta": 41,
                        "trueBeige": 43, "darkGreen": 45, "darkRed": 47, "darkOrange": 49,
                        "pearl": 51, "darkPurple": 53, "darkBlue": 55, "darkYellow": 57,
                        "teal": 59, "mulberry": 61, "tan": 63
                    }
                    color_costs = {color: value for color, value in color_values.items()}
                    color_owned = {color: False for color in color_values}
                    for i, color in enumerate(color_values):
                        globals()[f"draw_{color}"] = False
                        globals()[f"{color}_unlocked"] = i < 5 # Unlock the first 5 buttons initially

                    if prestiges >= 2:
                        parrot_owned = True
                        unlocked_pets.append("Parrot")

                    # Recalculate the multiplier after resetting
                    set_multiplier()

                elif prestige_menu_open and prestige_button.collidepoint((mouse_x, mouse_y)) and score < prestige_cost:
                    print("Not enough money to prestige!")

                # Input boxes
                if input_box.collidepoint((mouse_x, mouse_y)):
                    active_input_box = 'input_box'
                    color = color_active
                elif amount_input_box.collidepoint((mouse_x, mouse_y)):
                    active_input_box = 'amount_input_box'
                    amount_color = color_active
                else:
                    active_input_box = None
                    color = color_inactive
                    amount_color = color_inactive

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                save_game()
            elif event.key == pygame.K_F2:
                load_game()
            elif active_input_box == 'input_box':
                if event.key == pygame.K_RETURN:
                    entered_word = text.lower()
                    if entered_word == "awesome":
                        awesome = True
                    if entered_word == "shark":
                        unlocked_pets.append("Shark")
                        current_pet = "Shark"
                    elif entered_word == "!dev":
                        new_title3 = f"Developer"
                        unlocked_titles.append(new_title3)
                        score += 5000000000
                    elif entered_word.startswith("!money"):
                        try:
                            amount = int(entered_word.split()[1])
                            score += amount
                            print(f"Added £{amount} to score.")
                        except (IndexError, ValueError):
                            print("Invalid amount entered.")
                    elif entered_word.startswith("!prestige"):
                        try:
                            amount = int(entered_word.split()[1])
                            prestiges += amount
                            print(f"Added {amount} to prestiges.")
                        except (IndexError, ValueError):
                            print("Invalid amount entered.")
                    elif entered_word.startswith("!mult"):
                        try:
                            amount = int(entered_word.split()[1])
                            extra_multiplier += amount
                            print(f"Added {amount} to mult.")
                        except (IndexError, ValueError):
                            print("Invalid amount entered.")
                    elif entered_word.startswith("!time"):
                        try:
                            amount = int(entered_word.split()[1])
                            Time_Spent += amount
                            print(f"Added {amount} to time.")
                        except (IndexError, ValueError):
                            print("Invalid amount entered.")
                    elif entered_word.startswith("!title"):
                        try:
                            new_title = " ".join(entered_word.split()[1:]).title()  # Join parts and capitalize each word
                            if new_title in titles:
                                unlocked_titles.append(new_title)
                                current_title = new_title
                                print(f"Title changed to {new_title}.")
                            else:
                                print("Invalid title entered.")
                        except (IndexError, ValueError):
                            print("Invalid amount entered.")
                    elif entered_word.startswith("!pet"):
                        try:
                            pet_name = " ".join(entered_word.split()[1:]).title()  # Join parts and capitalize each word
                            if pet_name in pets:
                                unlocked_pets.append(pet_name)
                                current_pet = pet_name
                                print(f"Pet changed to {pet_name}.")
                            else:
                                print("Invalid pet name entered.")
                        except (IndexError, ValueError):
                            print("Invalid amount entered.")
                    if entered_word in used_words:
                        print("Error: This code has already been used.")
                    elif entered_word in secret_words:
                        reward = secret_words[entered_word]
                        score += reward
                        print(f"Congratulations! You earned £{reward} ")
                        used_words.add(entered_word)
                        use_word += 1
                    else:
                        print("Error: Invalid code.")
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            if active_input_box == 'input_box':
                pass

            elif active_input_box == 'amount_input_box':
                if event.key == pygame.K_RETURN:
                    try:
                        gamble_amount = int(amount_text)
                        gamble(gamble_amount)
                    except ValueError:
                        print("Invalid amount entered.")
                    amount_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    amount_text = amount_text[:-1]
                else:
                    amount_text += event.unicode

    # Buttons On Screen/Text UI

    screen.fill(colors["black"])

    pygame.draw.rect(screen, color, input_box, 2)
    text_surface = font.render(text, True, (colors["trueWhite"]))
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    task_green, color_lengths["green"], globals()["draw_green"] = draw_task("green", 50, 30, color_values["green"], globals()["draw_green"], color_lengths["green"], color_speeds["green"], globals()["green_unlocked"])
    task_red, color_lengths["red"], globals()["draw_red"] = draw_task("red", 105, 30, color_values["red"], globals()["draw_red"], color_lengths["red"], color_speeds["red"], globals()["red_unlocked"])
    task_orange, color_lengths["orange"], globals()["draw_orange"] = draw_task("orange", 160, 30, color_values["orange"], globals()["draw_orange"], color_lengths["orange"], color_speeds["orange"], globals()["orange_unlocked"])
    task_white, color_lengths["white"], globals()["draw_white"] = draw_task("white", 215, 30, color_values["white"], globals()["draw_white"], color_lengths["white"], color_speeds["white"], globals()["white_unlocked"])
    task_purple, color_lengths["purple"], globals()["draw_purple"] = draw_task("purple", 270, 30, color_values["purple"], globals()["draw_purple"], color_lengths["purple"], color_speeds["purple"], globals()["purple_unlocked"])
    task_blue, color_lengths["blue"], globals()["draw_blue"] = draw_task("blue", 325, 30, color_values["blue"], globals()["draw_blue"], color_lengths["blue"], color_speeds["blue"], globals()["blue_unlocked"])
    task_yellow, color_lengths["yellow"], globals()["draw_yellow"] = draw_task("yellow", 380, 30, color_values["yellow"], globals()["draw_yellow"], color_lengths["yellow"], color_speeds["yellow"], globals()["yellow_unlocked"])
    task_cyan, color_lengths["cyan"], globals()["draw_cyan"] = draw_task("cyan", 435, 30, color_values["cyan"], globals()["draw_cyan"], color_lengths["cyan"], color_speeds["cyan"], globals()["cyan_unlocked"])
    task_magenta, color_lengths["magenta"], globals()["draw_magenta"] = draw_task("magenta", 490, 30, color_values["magenta"], globals()["draw_magenta"], color_lengths["magenta"], color_speeds["magenta"], globals()["magenta_unlocked"])
    task_beige, color_lengths["beige"], globals()["draw_beige"] = draw_task("beige", 545, 30, color_values["beige"], globals()["draw_beige"], color_lengths["beige"], color_speeds["beige"], globals()["beige_unlocked"])
    task_trueGreen, color_lengths["trueGreen"], globals()["draw_trueGreen"] = draw_task("trueGreen", 50, 330, color_values["trueGreen"], globals()["draw_trueGreen"], color_lengths["trueGreen"], color_speeds["trueGreen"], globals()["trueGreen_unlocked"])
    task_trueRed, color_lengths["trueRed"], globals()["draw_trueRed"] = draw_task("trueRed", 105, 330, color_values["trueRed"], globals()["draw_trueRed"], color_lengths["trueRed"], color_speeds["trueRed"], globals()["trueRed_unlocked"])
    task_trueOrange, color_lengths["trueOrange"], globals()["draw_trueOrange"] = draw_task("trueOrange", 160, 330, color_values["trueOrange"], globals()["draw_trueOrange"], color_lengths["trueOrange"], color_speeds["trueOrange"], globals()["trueOrange_unlocked"])
    task_trueWhite, color_lengths["trueWhite"], globals()["draw_trueWhite"] = draw_task("trueWhite", 215, 330, color_values["trueWhite"], globals()["draw_trueWhite"], color_lengths["trueWhite"], color_speeds["trueWhite"], globals()["trueWhite_unlocked"])
    task_truePurple, color_lengths["truePurple"], globals()["draw_truePurple"] = draw_task("truePurple", 270, 330, color_values["truePurple"], globals()["draw_truePurple"], color_lengths["truePurple"], color_speeds["truePurple"], globals()["truePurple_unlocked"])
    task_trueBlue, color_lengths["trueBlue"], globals()["draw_trueBlue"] = draw_task("trueBlue", 325, 330, color_values["trueBlue"], globals()["draw_trueBlue"], color_lengths["trueBlue"], color_speeds["trueBlue"], globals()["trueBlue_unlocked"])
    task_trueYellow, color_lengths["trueYellow"], globals()["draw_trueYellow"] = draw_task("trueYellow", 380, 330, color_values["trueYellow"], globals()["draw_trueYellow"], color_lengths["trueYellow"], color_speeds["trueYellow"], globals()["trueYellow_unlocked"])
    task_trueCyan, color_lengths["trueCyan"], globals()["draw_trueCyan"] = draw_task("trueCyan", 435, 330, color_values["trueCyan"], globals()["draw_trueCyan"], color_lengths["trueCyan"], color_speeds["trueCyan"], globals()["trueCyan_unlocked"])
    task_trueMagenta, color_lengths["trueMagenta"], globals()["draw_trueMagenta"] = draw_task("trueMagenta", 490, 330, color_values["trueMagenta"], globals()["draw_trueMagenta"], color_lengths["trueMagenta"], color_speeds["trueMagenta"], globals()["trueMagenta_unlocked"])
    task_trueBeige, color_lengths["trueBeige"], globals()["draw_trueBeige"] = draw_task("trueBeige", 545, 330, color_values["trueBeige"], globals()["draw_trueBeige"], color_lengths["trueBeige"], color_speeds["trueBeige"], globals()["trueBeige_unlocked"])
    task_darkGreen, color_lengths["darkGreen"], globals()["draw_darkGreen"] = draw_task("darkGreen", 50, 630, color_values["darkGreen"], globals()["draw_darkGreen"], color_lengths["darkGreen"], color_speeds["darkGreen"], globals()["darkGreen_unlocked"])
    task_darkRed, color_lengths["darkRed"], globals()["draw_darkRed"] = draw_task("darkRed", 105, 630, color_values["darkRed"], globals()["draw_darkRed"], color_lengths["darkRed"], color_speeds["darkRed"], globals()["darkRed_unlocked"])
    task_darkOrange, color_lengths["darkOrange"], globals()["draw_darkOrange"] = draw_task("darkOrange", 160, 630, color_values["darkOrange"], globals()["draw_darkOrange"], color_lengths["darkOrange"], color_speeds["darkOrange"], globals()["darkOrange_unlocked"])
    task_pearl, color_lengths["pearl"], globals()["draw_pearl"] = draw_task("pearl", 215, 630, color_values["pearl"], globals()["draw_pearl"], color_lengths["pearl"], color_speeds["pearl"], globals()["pearl_unlocked"])
    task_darkPurple, color_lengths["darkPurple"], globals()["draw_darkPurple"] = draw_task("darkPurple", 270, 630, color_values["darkPurple"], globals()["draw_darkPurple"], color_lengths["darkPurple"], color_speeds["darkPurple"], globals()["darkPurple_unlocked"])
    task_darkBlue, color_lengths["darkBlue"], globals()["draw_darkBlue"] = draw_task("darkBlue", 325, 630, color_values["darkBlue"], globals()["draw_darkBlue"], color_lengths["darkBlue"], color_speeds["darkBlue"], globals()["darkBlue_unlocked"])
    task_darkYellow, color_lengths["darkYellow"], globals()["draw_darkYellow"] = draw_task("darkYellow", 380, 630, color_values["darkYellow"], globals()["draw_darkYellow"], color_lengths["darkYellow"], color_speeds["darkYellow"], globals()["darkYellow_unlocked"])
    task_teal, color_lengths["teal"], globals()["draw_teal"] = draw_task("teal", 435, 630, color_values["teal"], globals()["draw_teal"], color_lengths["teal"], color_speeds["teal"], globals()["teal_unlocked"])
    task_mulberry, color_lengths["mulberry"], globals()["draw_mulberry"] = draw_task("mulberry", 490, 630, color_values["mulberry"], globals()["draw_mulberry"], color_lengths["mulberry"], color_speeds["mulberry"], globals()["mulberry_unlocked"])
    task_tan, color_lengths["tan"], globals()["draw_tan"] = draw_task("tan", 545, 630, color_values["tan"], globals()["draw_tan"], color_lengths["tan"], color_speeds["tan"], globals()["tan_unlocked"])
    for i, color in enumerate(color_values):
        x_coord = 10 + (i % 10) * 60
        row = i // 10
        globals()[f"{color}_buy"], globals()[f"{color}_manager_buy"] = draw_buttons(color, x_coord, row, color_costs[color], color_owned[color], color_manager_costs[color], globals()[f"{color}_unlocked"],color_speeds[color], maxed_upgrades)
    display_score()
    display_InputCode = font.render('Input Codes Here:', True, colors["trueWhite"], colors["black"])
    screen.blit(display_InputCode, (720, 820))
    display_Casino = font.render("Chromatic Casino:", True, colors["trueWhite"], colors["black"])
    screen.blit(display_Casino,(amount_input_box.x + amount_input_box.width - 200, amount_input_box.y - 150))
    display_ach = font.render('Achievements Unlocked: ' + str(achievements_unlocked) + ' / ' + str(achievements_total), True, colors["trueRed"], colors["black"])
    screen.blit(display_ach, (425, 830))
    display_max = font.render('Upgrades Maxed: ' + str(maxed_upgrades) + ' / ' + "30", True, colors["trueRed"], colors["black"])
    screen.blit(display_max, (245, 830))
    display_box = font.render('Boxes Opened: ' + str(mystery_boxes_opened) + ' / ' + "50", True, colors["trueRed"], colors["black"])
    screen.blit(display_box, (245, 860))
    display_automators()
    display_ach = font.render('Prestiges: ' + str(prestiges), True, colors["trueRed"], colors["black"])

    screen.blit(display_ach, (425, 875))

    # Convert Time_Spent into hours, minutes, and seconds
    hours = Time_Spent // 3600
    minutes = (Time_Spent % 3600) // 60
    seconds = Time_Spent % 60

    # Format the time as HH:MM:SS
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"

    # Update the display for Time_Spent
    display_time = font.render(f'Time Spent: {formatted_time}', True, colors["trueRed"], colors["black"])
    screen.blit(display_time, (245, 875))

    display_mult = font.render('Multiplier: ' + str(total_multiplier), True, colors["trueRed"], colors["black"])
    screen.blit(display_mult, (425, 860))
    Title = font.render(f'Colors of Fortune Version: {version}' +str(), True, colors["trueWhite"], colors["black"])
    screen.blit(Title, (5, 5))
    creator = font.render('Creator: Connor E'+str(), True, colors["trueWhite"], colors["black"])
    screen.blit(creator, (770, 5))
    buy_more = font.render('Buy Upgrades:', True, colors["trueWhite"])
    screen.blit(buy_more, (5, 580))
    buy_managers = font.render('Buy Automators:', True, colors["trueWhite"])
    screen.blit(buy_managers, (10, 700))
    mystery_boxes = font.render('Mystery Boxes: ', True, colors["trueWhite"])
    screen.blit(mystery_boxes,(1250, 11))

    # Draw the "All In" and "1/2" buttons
    pygame.draw.rect(screen, colors["trueGreen"], all_in_button)
    all_in_text = font.render("All In", True, colors["white"])
    screen.blit(all_in_text, (all_in_button.x + 10, all_in_button.y + 5))

    pygame.draw.rect(screen, colors["trueRed"], half_button)
    half_text = font.render("1/2", True, colors["white"])
    screen.blit(half_text, (half_button.x + 25, half_button.y + 5))

    prestige_button = pygame.draw.rect(screen, colors["blue"], [20, 820, 150, 50])
    display_prestige_cost()

    # Blit the text surface onto the screen
    text_rect = text_surface.get_rect(center=(box1_coords[0] + box1_size[0] // 2, box1_coords[1] + box1_size[1] // 2))
    screen.blit(text_surface, text_rect)

    # Draw the box for the shop
    pygame.draw.rect(screen, colors["white"], (*box2_coords, *box2_size), 2)

    # Draw the casino frame
    pygame.draw.rect(screen, colors["white"], (*new_frame_coords, *new_frame_size), 2)

    # Update dropdown options based on unlocked titles
    dropdown_options_rects = []  # Reset list before re-populating
    for i, _ in enumerate(unlocked_titles):
        option_rect = dropdown_rect.copy()
        option_rect.y += (i + 1) * dropdown_rect.height  # Offset for each option
        dropdown_options_rects.append(option_rect)

    set_multiplier()
    draw_dropdown_menu()
    draw_pets_dropdown_menu()

    # Draw mystery box buttons
    titles_box, pets_box = draw_mystery_box_menu()

    # Draw the daily reward button
    daily = font.render('Daily Reward: ', True, colors["trueWhite"])
    screen.blit(daily, (700, 580))

    if can_claim_daily_reward():
        pygame.draw.rect(screen, colors["green"], daily_reward_button)
        daily_reward_text = font.render("Daily Reward ready", True, colors["black"])
        screen.blit(daily_reward_text, (daily_reward_button.x + (daily_reward_button.width - daily_reward_text.get_width()) // 2, daily_reward_button.y + 15))
    else:
        pygame.draw.rect(screen, colors["red"], daily_reward_button)
        daily_reward_text = font.render("Already Claimed", True, colors["black"])
        screen.blit(daily_reward_text, (daily_reward_button.x + (daily_reward_button.width - daily_reward_text.get_width()) // 2, daily_reward_button.y + 15))
        wait_time_text = font.render(f"Please wait {get_time_until_next_daily_reward()}", True, colors["black"])
        screen.blit(wait_time_text, (daily_reward_button.x + (daily_reward_button.width - wait_time_text.get_width()) // 2, daily_reward_button.y + 30))


    # Draw the amount input box inside the new frame
    pygame.draw.rect(screen, amount_color, amount_input_box, 2)
    amount_surface = font.render(amount_text, True, colors["trueWhite"])
    screen.blit(amount_surface, (amount_input_box.x + 5, amount_input_box.y + 5))
    amount_label = font.render('Enter Amount:', True, colors["trueWhite"])
    screen.blit(amount_label, (amount_input_box.x, amount_input_box.y - 20))

    # Draw Achievements Button
    pygame.draw.rect(screen, colors["purple"], achievements_button)
    ach_btn_text = font.render("Achievements", True, colors["white"])
    screen.blit(ach_btn_text, (achievements_button.x + (achievements_button.width - ach_btn_text.get_width()) // 2, achievements_button.y + 15))

    # Draw quests Menu Button (below achievements button)
    pygame.draw.rect(screen, colors["orange"], quests_menu_button)
    quests_btn_text = font.render("Quests", True, colors["white"])
    screen.blit(quests_btn_text, (quests_menu_button.x + (quests_menu_button.width - quests_btn_text.get_width()) // 2, quests_menu_button.y + 15))

    # Draw the flow minigame button
    pygame.draw.rect(screen, colors["yellow"], flow_minigame_button)
    flow_minigame_text = font.render("Flow Minigame", True, colors["black"]) 
    screen.blit(flow_minigame_text, (flow_minigame_button.x + (flow_minigame_button.width - flow_minigame_text.get_width()) // 2, flow_minigame_button.y + 15))

    # Draw the quests menu if open (simple menu, similar to achievements)
    if quests_menu_open:
        menu_rect = pygame.Rect(600, 180, ACHIEVEMENTS_MENU_WIDTH, ACHIEVEMENTS_MENU_HEIGHT)
        pygame.draw.rect(screen, colors["black"], menu_rect)
        pygame.draw.rect(screen, colors["trueWhite"], menu_rect, 3)

        # Draw title
        title_font = pygame.font.SysFont("Arial", 28, bold=True)
        title_text = title_font.render("Quests", True, colors["trueWhite"])
        screen.blit(title_text, (menu_rect.x + (menu_rect.width - title_text.get_width()) // 2, menu_rect.y + 10))

        # Draw close button (top-right)
        close_quests_rect = pygame.Rect(600 + ACHIEVEMENTS_MENU_WIDTH - 120, 190, 100, 40)
        pygame.draw.rect(screen, colors["red"], close_quests_rect)
        close_text = font.render("Close", True, colors["white"])
        screen.blit(close_text, (close_quests_rect.x + (close_quests_rect.width - close_text.get_width()) // 2, close_quests_rect.y + 10))

        # Handle close button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if close_quests_rect.collidepoint(pygame.mouse.get_pos()):
                quests_menu_open = False

        # --- Quests Menu Sections ---

        # Daily Quests Section
        daily_section_y = menu_rect.y + 60
        daily_title = font.render("Daily Quests", True, colors["trueYellow"])
        screen.blit(daily_title, (menu_rect.x + 40, daily_section_y))

        # --- Daily Quests Section ---

        # Define a larger pool of daily quests with progress keys and targets
        daily_quests_pool = [
            {"desc": "Earn £1,000,000", "key": "earn_money", "target": 1_000_000},
            {"desc": "Prestige 3 times", "key": "prestige", "target": 3},
            {"desc": "Open 10 mystery boxes", "key": "open_boxes", "target": 10},
            {"desc": "Gamble £10,000", "key": "gamble_money", "target": 10_000},
            {"desc": "Buy 5 automators", "key": "buy_automators", "target": 5},
            {"desc": "Buy 10 upgrades", "key": "buy_upgrades", "target": 10},
            {"desc": "Play for 30 minutes", "key": "play_time", "target": 1800},
            {"desc": "Unlock a new pet", "key": "unlock_pet", "target": 1},
            {"desc": "Unlock a new title", "key": "unlock_title", "target": 1},
            {"desc": "Claim your daily reward", "key": "claim_daily", "target": 1},
            # ...add more as needed...
        ]

        # Use a persistent random seed per day so quests don't change on redraw
        today_seed = int(datetime.datetime.now().strftime("%Y%m%d"))
        random.seed(today_seed)
        daily_quests_today = random.sample(daily_quests_pool, 3)
        random.seed()  # Reset random seed to not affect other game logic

        # --- Progress tracking for daily quests ---
        if "daily_quest_progress" not in globals():
            daily_quest_progress = {}

        # Only add missing keys for today's quests, never overwrite existing progress
        for quest in daily_quests_today:
            if quest["key"] not in daily_quest_progress:
                daily_quest_progress[quest["key"]] = 0

        # Update progress for each quest type (example logic, expand as needed)
        for quest in daily_quests_today:
            key = quest["key"]
            if key == "earn_money":
                daily_quest_progress[key] = min(score, quest["target"])
            elif key == "prestige":
                daily_quest_progress[key] = min(prestiges, quest["target"])
            elif key == "open_boxes":
                daily_quest_progress[key] = min(mystery_boxes_opened, quest["target"])
            elif key == "gamble_money":
                daily_quest_progress[key] = min(earnings + losings, quest["target"])
            elif key == "buy_automators":
                daily_quest_progress[key] = min(managers_owned, quest["target"])
            elif key == "buy_upgrades":
                daily_quest_progress[key] = min(upgrades_bought, quest["target"])
            elif key == "play_time":
                daily_quest_progress[key] = min(Time_Spent, quest["target"])
            elif key == "unlock_pet":
                daily_quest_progress[key] = 1 if len(unlocked_pets) > 1 else 0
            elif key == "unlock_title":
                daily_quest_progress[key] = 1 if len(unlocked_titles) > 1 else 0
            elif key == "claim_daily":
                daily_quest_progress[key] = 1 if claimed else 0
            # ...add more quest types as needed...

        # Display the 3 daily quests with progress bars
        for i, quest in enumerate(daily_quests_today):
            progress = daily_quest_progress[quest["key"]]
            target = quest["target"]
            completed = progress >= target
            quest_text = font.render(f"- {quest['desc']}", True, colors["white"])
            screen.blit(quest_text, (menu_rect.x + 60, daily_section_y + 30 + i * 38))
            # Draw progress bar
            bar_x = menu_rect.x + 60
            bar_y = daily_section_y + 50 + i * 38
            bar_width = 300
            bar_height = 12
            fill_width = int(bar_width * min(progress / target, 1.0))
            pygame.draw.rect(screen, colors["gray"], (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, colors["green" if completed else "yellow"], (bar_x, bar_y, fill_width, bar_height))
            # Draw progress text
            progress_text = font.render(f"{int(progress)}/{int(target)}", True, colors["white"])
            screen.blit(progress_text, (bar_x + bar_width + 10, bar_y - 2))
            # Draw checkmark if completed
            if completed:
                check_text = font.render("✓", True, colors["green"])
                screen.blit(check_text, (bar_x + bar_width + 60, bar_y - 2))

    # If achievements menu is open, draw it on top
    if achievements_menu_open:
        menu_rect = pygame.Rect(600, 180, ACHIEVEMENTS_MENU_WIDTH, ACHIEVEMENTS_MENU_HEIGHT)
        pygame.draw.rect(screen, colors["black"], menu_rect)
        pygame.draw.rect(screen, colors["trueWhite"], menu_rect, 3)

        # Draw title
        title_font = pygame.font.SysFont("Arial", 28, bold=True)
        title_text = title_font.render("Achievements", True, colors["trueWhite"])
        screen.blit(title_text, (menu_rect.x + (menu_rect.width - title_text.get_width()) // 2, menu_rect.y + 10))

        # Draw close button (top-right, slightly higher up) with outline
        close_ach_rect = pygame.Rect(600 + ACHIEVEMENTS_MENU_WIDTH - 120, 190, 100, 40)
        # Draw button fill
        pygame.draw.rect(screen, colors["red"], close_ach_rect)
        close_text = font.render("Close", True, colors["white"])
        screen.blit(close_text, (close_ach_rect.x + (close_ach_rect.width - close_text.get_width()) // 2, close_ach_rect.y + 10))

        # Set up a surface for scrolling (leave space for title)
        scroll_surface = pygame.Surface((menu_rect.width - 40, menu_rect.height - 90))
        scroll_surface.fill(colors["black"])

        # Draw achievements list onto the scroll surface
        for idx, (popup_title, popup_desc) in enumerate(popup_texts):
            unlocked = achievements[idx]["unlocked"]
            # Hide "Awesome Sauce" achievement (index 15) until unlocked
            if idx == 15 and not unlocked:
                display_title = "Hidden Achievement"
                display_desc = "Unlock the achievment to view"
            else:
                display_title = popup_title
                display_desc = popup_desc
            status = "Unlocked" if unlocked else "Locked"
            color_status = colors["trueGreen"] if unlocked else colors["trueRed"]
            title_text = font.render(f"{display_title}", True, colors["trueWhite"])
            desc_text = font.render(f"{display_desc}", True, colors["trueWhite"])
            status_text = font.render(status, True, color_status)
            y = idx * ACHIEVEMENT_ROW_HEIGHT - achievements_menu_scroll_offset
            if 0 <= y < scroll_surface.get_height() - ACHIEVEMENT_ROW_HEIGHT:
                scroll_surface.blit(title_text, (10, y))
                scroll_surface.blit(desc_text, (320, y))
                scroll_surface.blit(status_text, (scroll_surface.get_width() - 90, y))

        # Blit the scroll surface onto the menu (below the title)
        screen.blit(scroll_surface, (menu_rect.x + 20, menu_rect.y + 60))

        # Draw a simple scrollbar
        total_height = len(popup_texts) * ACHIEVEMENT_ROW_HEIGHT
        if total_height > scroll_surface.get_height():
            scrollbar_height = max(40, int(scroll_surface.get_height() * scroll_surface.get_height() / total_height))
            scrollbar_y = int(achievements_menu_scroll_offset * (scroll_surface.get_height() - scrollbar_height) / (total_height - scroll_surface.get_height()))
            pygame.draw.rect(screen, colors["gray"], (menu_rect.x + menu_rect.width - 15, menu_rect.y + 60 + scrollbar_y, 10, scrollbar_height))

    if popup_queue:
        if popup_timer == 0:
            popup_timer = pygame.time.get_ticks()
        popup_index = popup_queue[0]
        popup_surface = popups[popup_index]
        popup_rect = popup_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(popup_surface, popup_rect)
        # Show popup for popup_duration ms
        if pygame.time.get_ticks() - popup_timer > popup_duration:
            popup_queue.pop(0)
            popup_timer = 0

    if gamble_popup_queue:
        if gamble_popup_timer == 0:
            gamble_popup_timer = pygame.time.get_ticks()
        popup_index = gamble_popup_queue[0]
        popup_surface = gamble_popups[popup_index]
        # Position directly under the casino frame
        popup_x = new_frame_coords[0] + new_frame_size[0] // 2
        popup_y = new_frame_coords[1] + new_frame_size[1] + 25  # 25px below the frame
        popup_rect = popup_surface.get_rect(center=(popup_x, popup_y))
        screen.blit(popup_surface, popup_rect)
        if pygame.time.get_ticks() - gamble_popup_timer > gamble_popup_duration:
            gamble_popup_queue.pop(0)
            gamble_popup_timer = 0

    if box_popup_queue:
        if box_popup_timer == 0:
            box_popup_timer = pygame.time.get_ticks()
        popup_index = box_popup_queue[0]
        popup_surface = box_popups[popup_index]
        # Position near the mystery boxes (right side, just below the boxes)
        popup_x = 1250 + 75  # Centered under the boxes (box x + half width)
        popup_y = 180        # Just below the two box buttons
        popup_rect = popup_surface.get_rect(center=(popup_x, popup_y))
        screen.blit(popup_surface, popup_rect)
        if pygame.time.get_ticks() - box_popup_timer > box_popup_duration:
            box_popup_queue.pop(0)
            box_popup_timer = 0

    pygame.display.flip()

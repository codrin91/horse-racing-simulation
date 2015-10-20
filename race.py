#! /usr/bin/python

import math, os, random, sys, time
import pygame
from pygame.locals import *

pygame.init()

# Screen and track dimensions
DIM_X = 800
DIM_Y = 600
TRACK_START = 50
TRACK_END = 750
TRACK_LENGTH = TRACK_END - TRACK_START

# From coolors: http://coolors.co/app/1be7ff-6eeb83-e4ff1a-e8aa14-ff5714
BLUE = pygame.Color('#1BE7FF')
GREEN = pygame.Color('#6EEB83')
YELLOW = pygame.Color('#E4FF1A')
ORANGE = pygame.Color('#E8AA14')
RED = pygame.Color('#FF5714')
WHITE = pygame.Color('#FFFFFF')
GREY = pygame.Color('#3C3C3C')

# Font settings
FONT = pygame.font.SysFont('joystix', 36)

# Delay between screen updates
PACE = 0.25



class Horse():
    '''
    Represents a racing horse, including position, speed, color, name, and
    race history. 
    ''' 
    def __init__(self, name, speed, x, y, color):
        self.speed = speed
        self.x = x
        self.y = y
        self.color = color 
        self.races = 0
        self.wins = 0
        self.name = name
        self.odds = ''
    
    def move(self):
        '''
        Move the horse. The randomly chosen speed is used as a percentage of
        the track's length.
        '''
        distance = int(random.choice(self.speed) / 100.0 * TRACK_LENGTH)
        self.x += random.choice(self.speed)
    
    def add_result(self, won):
        '''
        Update the horse's race statistics and odds.
        '''
        if won:
            self.wins += 1
        self.races += 1
        
        # Calculate the new odds (in favor of the house)
        if self.wins == 0:
            self.odds = math.floor( (self.races + 1) / (self.wins + 1))
        else:
            self.odds = math.floor(self.races / self.wins)
       
       # Convert odds to a string, like "1:4" 
        self.odds = '1:' + str(int(self.odds))
    
    def draw(self, surface):
        '''
        Draw a horse, currently represented as a colored square.
        '''
        shape = Rect(self.x, self.y, 20, 20)
        pygame.draw.rect(surface, self.color, shape)
        
        # Draw label
        label = FONT.render(self.name, True, self.color)
        surface.blit(label, (10, self.y - 15))

def race(surface, lanes, horses, pace=0.75):
    '''
    Simulate a single race.
    Input: a list of Horses
    Returns: string for winner 
    ''' 
    # Simulate the race! 
    while max([horse.x for horse in horses]) <= TRACK_END:
        
        # Setup the background and track
        surface.fill(GREY)
        draw_track(surface, lanes)
        
        # Move the horses
        for horse in horses:
            horse.move()
            horse.draw(surface)
        
        pygame.display.flip()
        time.sleep(pace)
    
    winning_distance = max([horse.x for horse in horses])
    
    winners = []
        
    for horse in horses:
        if horse.x == winning_distance:
            winners.append(horse)
    
    if len(winners) > 1:
        winner = random.choice(winners)
    else:
        winner = winners[0]
    
    # Update results
    for horse in horses:
        if horse == winner:
            horse.add_result(won=True)
        else:
            horse.add_result(won=False)
    
    # Display string about winner
    winning_string = 'Horse ' + winner.name + ' won!'
    winner_display = FONT.render(winning_string, True, WHITE)
    surface.blit(winner_display, (200, 300))
    
    if len(winners) > 1:
        photofinish = FONT.render('(by a photo finish!)', True, WHITE)
        surface.blit(winner_display, (200, 340))
        
def summary(surface, horses):
    '''
    Display the number of wins for each horse and its updated odds.
    '''
    
    x = 75
    
    for horse in horses:
        y = 425
        name = FONT.render(horse.name, True, horse.color)
        surface.blit(name, (x, y))
        
        wins = FONT.render(str(horse.wins), True, horse.color)
        surface.blit(wins, (x, y + 36))
        
        odds = FONT.render(horse.odds, True, horse.color)
        surface.blit(odds, (x - 30, y + 72))
        
        # Increment x for next horse
        x += 150
    
    # Display the changes
    pygame.display.flip()

def draw_track(surface, lanes):
    '''
    Draw the track give a pygame surface and a list of lane positions.
    '''
    for lane in lanes:
        shape = Rect(TRACK_START, lane, TRACK_LENGTH, 2)
        pygame.draw.rect(surface, WHITE, shape)

if __name__ == '__main__':
    
    # Initialize the game
    clock = pygame.time.Clock()
    pygame.display.set_caption('The Silver Eagle Stakes')
    
    # Setup the surface 
    surface = pygame.display.set_mode((DIM_X, DIM_Y))
    surface.fill(GREY)
    
    lanes = [ y + 10 for y in range(0, 6*40, 40)]
    draw_track(surface, lanes)
   
    
    # Create the horses
    a = Horse('A', [21, 21, 21, 21, 22, 22, 23], TRACK_START, lanes[0] + 10, YELLOW)
    b = Horse('B', [17, 17, 20, 26, 26], TRACK_START, lanes[1] + 10, GREEN)
    c = Horse('C', [18, 18, 22, 24, 24], TRACK_START, lanes[2] + 10, ORANGE)
    d = Horse('D', [17, 20, 27], TRACK_START, lanes[3] + 10, BLUE)
    e = Horse('E', [14, 20, 28], TRACK_START, lanes[4] + 10, RED)
    
    horses = [a,b,c,d,e]
    
    for horse in horses:
        horse.x = TRACK_START
    
    pygame.display.flip()
    
    keep_racing = True
    while keep_racing:
        
        # Reset horse positions
        for horse in horses:
            horse.x = TRACK_START
        
        # Run the race
        winner_string = race(surface, lanes, horses, PACE)
        
        # Display winner and summaries
        pygame.display.flip()
        
        summary(surface, horses)
        
        # Wait for a game event
        while True:
            event = pygame.event.wait()
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                break
    

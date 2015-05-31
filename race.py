import random
import os
import time
import math

class Horse():
    
    def __init__(self, name, speed):
        self.speed = speed
        self.races = 0
        self.wins = 0
        self.name = name
        self.odds = ''
    
    def move(self):
        return random.choice(self.speed)
    
    def add_result(self, won):
        if won:
            self.wins += 1
        self.races += 1
        
        if self.wins == 0:
            self.odds = math.floor( (self.races + 1) / (self.wins + 1))
        else:
            self.odds = math.floor(self.races / self.wins)
        
        #if not self.odds == 1:
        #    self.odds -= 1
            
        self.odds = '1:' + str(int(self.odds))

def race(horses, track_length=70, fast=False):
    progress = [0 for i in range(len(horses))]
    
    while max(progress) <= track_length:
        os.system('clear')
        print('\n')
        print(' |' + 70 * '%')
        for i in range(len(horses)):
            horse = horses[i]
            progress[i] += horse.move()
            print(' |' + 70 * '-' + '|')
            print(' |' + (progress[i] - 1) * '*' + horse.name)
        print(' |' + 70 * '-' + '|')
        print(' |' + 70 * '%')
        if not fast:
            time.sleep(1)
    
    # Identify winner; flip coin if a tie
    
    winners = []
    
    for i in range(len(progress)):
        if progress[i] == max(progress):
            winners.append(i)
    
    if len(winners) > 1:
        winner = random.choice(winners)
    else:
        winner = winners[0]
    
    for i in range(len(progress)):
        won = winner == i
        horses[i].add_result(won)
    print('\n')
    winning_string = '\t\t\tHorse ' + horses[winner].name + ' won!'
    if len(winners) > 1:
        winning_string += ' (by a photo finish!)'
    
    print(winning_string)

def summary(horses):
    rows = {'names':'     |\t', 
           'wins':  'Wins |\t', 
           'odds':  'Odds |\t'}
    for horse in horses:
        rows['names'] += horse.name + '\t|\t'
        rows['wins'] += str(horse.wins) + '\t|\t'
        rows['odds'] += horse.odds + '\t|\t'
    print(rows['names'])
    print(rows['wins'])
    print(rows['odds'])

if __name__ == '__main__':
    
    b = Horse('B', [4,4,5,6,6])
    c = Horse('C', [5,5,5])
    d = Horse('D', [3,5,5,7])
    e = Horse('E', [4,5,6])
    a = Horse('A', [3,3,3,4,4,4,4,4,12])
    horses = [a,b,c,d,e]
    
    while True:
        #for i in range(1000):
        print('\n')
        print(70 * '%')
        race(horses, fast=False)
        print('\n')
        summary(horses)
        print(70 * '+')
        print('\n')
        raw_input('Press any key to race again!')
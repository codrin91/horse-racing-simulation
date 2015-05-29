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

def race(horses, track_length=80):
    progress = [0 for i in range(len(horses))]
    
    while max(progress) <= track_length:
        os.system('clear')
        print('\n')
        print(' |' + 80 * '%')
        for i in range(len(horses)):
            horse = horses[i]
            progress[i] += horse.move()
            print(' |' + 80 * '-' + '|')
            print(' |' + progress[i] * '*' + horse.name)
        print(' |' + 80 * '-' + '|')
        print(' |' + 80 * '%')
        time.sleep(.2)
    
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
    
    a = Horse('A', [4,5,6])
    b = Horse('B', [5,5,5])
    c = Horse('C', [3,5,7])
    d = Horse('D', [5,5,5])
    e = Horse('E', [4,4,4,4,4,4,4,4,4,12])
    horses = [a,b,c,d,e]
    
    while True:
        print('\n')
        print(80 * '%')
        race(horses)
        print('\n')
        summary(horses)
        print(80 * '+')
        print('\n')
        raw_input('Press any key to race again!')
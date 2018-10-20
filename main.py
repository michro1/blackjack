#!/usr/local/bin/python3

# Document: main.py
# Author:   Michelle Rosenberger
# Date:     November 28, 2017

# Import necessary modules
import random
import itertools    # Intertools performs Cartesian product of two sequences
import numpy as np
import matplotlib.pyplot as plt

CARD_VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10,
               10, 10, 10, 11]  # Add values to cards

CARD_NUMBERS = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen",
                "King", "Ace"]  # define the numbers of the deck

SUITS = ["Spade", "Diamond", "Heart", "Club"]  # define the suits of the deck

CARD_VALUE_LOOKUP = dict(zip(CARD_NUMBERS, CARD_VALUES))  # Combine values and cards

HIT = 1
DEAL = 2
STAY = 0

ACTIONS = ["s", "h"]

########################################

class Card:         # Create my deck of cards

    def __init__(self, number, suit):
        self.number = number
        self.suit = suit

    def __str__(self):
        return "%s of %s" % (self.number, self.suit)
    def __repr__(self):
        return self.__str__()

    def value(self):
        return CARD_VALUE_LOOKUP[self.number]

def draw_cards(n, deck):
    c = []
    for i in range(n):
        if len(deck) == 0:
            deck = fill_deck()
        c.append(deck.pop())
    return c


def fill_deck():    # combine numbers and suits to a deck
    deck = []
    for i in list(itertools.product(CARD_NUMBERS, SUITS)):
        deck.append(Card(i[0], i[1]))
    random.shuffle(deck)
    return deck

def play(n, player):
    cards = draw_cards(n, deck) # assign cards player
    player.extend(cards) # add values cards
    sum_player = sum(card.value() for card in player)
    return sum_player

##########################################

# Initialize
Q = {}
pstate = None
paction = None

##########################################
# define policies

def random_policy(epsilon, state):
    action = random.choice(ACTIONS)
    return action


def epsilon_greedy_policy(epsilon, state):
    if random.random() < epsilon: 
        return random_policy(epsilon, state)
    else:
        return best_policy(epsilon, state)


def best_policy(epsilon, state):
    if not state in Q:
        Q[state] = { 'h': 0, 's': 0}

    if Q[state]["h"] == Q[state]["s"]:
        action = random.choice(ACTIONS)
    elif Q[state]["h"] > Q[state]["s"]:
        action = "h"
    else:
        action = "s"

    return action

##########################################

# Q-learning
def QL(state, pstate, paction, action, reward, alpha): # n = new, p = previous, reward = reward_player
    if not pstate:
        pstate = state

    if not paction:
        paction = action

    if not pstate in Q:
        Q[pstate] = { 'h': 0, 's': 0}

    old = Q[pstate][paction]

    if state in Q:
        new = max(Q[state]['h'], Q[state]['s'])
    else:
        new = 0
    
    Q[pstate][paction] += alpha * (reward + new - old)


# Monte Carlo
def MC(state, pstate, paction, action, reward, alpha): # n = new, p = previous, reward = reward_player

    if not state in Q:
        Q[state] = { 'h': 0, 's': 0}

    Q[state][action] += alpha * (reward - Q[state][action])

# SARSA
def SARSA(state, pstate, paction, action, reward, alpha): # n = new, p = previous, reward = reward_player

    if not pstate:
        pstate = state

    if not paction:
        paction = action

    if not pstate in Q:
        Q[pstate] = { 'h': 0, 's': 0}

    old = Q[pstate][paction]

    if state in Q:
        new = max(Q[state]['h'], Q[state]['s'])
    else:
        new = 0
    
    Q[pstate][paction] += alpha * (reward + new - old)


##########################################

cards_dealer = []
cards_player = []
points_player = 0
points_dealer = 0
deck = fill_deck()

reward_dealer = []
reward_player = []

##########################################

def wins():
    if points_player > 21:
        reward_player.append(-1)
        reward_dealer.append(1)
    if points_player == 21:
        if points_dealer == 21:
            reward_player.append(0)
            reward_dealer.append(0)
        else:
            reward_player.append(1)
            reward_dealer.append(-1)
    if points_player < 21:
        if points_dealer < points_player:
            reward_player.append(1)
            reward_dealer.append(-1)
        elif points_dealer > points_player:
            reward_player.append(-1)
            reward_dealer.append(1)
        elif points_dealer == points_player:
            reward_player.append(0)
            reward_dealer.append(0)
    return reward_player, reward_dealer
    

##########################################
def epsiode(Name, interaction, policy, epsilon, alpha, update, percentage, numbers):
    
    global Q, cards_dealer, cards_player, points_player, points_dealer, deck, reward_dealer, reward_player, pstate, paction

    # Intialize everthing new for next 
    Q = {}
    pstate = None
    paction = None
    cards_dealer = []
    cards_player = []
    points_player = 0
    points_dealer = 0
    reward_dealer = []
    reward_player = []
    deck = fill_deck()

    reward_epsiode_player = []

    #interaction = int(input("Number of interactions"))

    for i in range(interaction):
        #print("New game started")
        points_dealer = play(DEAL, cards_dealer)
        points_player = play(DEAL, cards_player)
        #print("Cards of dealer are: %s and cards of player are: %s " % (cards_dealer, cards_player))
        action = None

        if points_dealer > 21:
            reward_dealer.append(-1)
            reward_player.append(1)
        
        elif points_dealer == 21:
            if points_player == 21:
                reward_dealer.append(0)
                reward_player.append(0)
            else:
                reward_dealer.append(1)
                reward_player.append(-1)
        
        elif points_dealer < 21:
            while points_player < 21:
                state = (points_player, points_dealer)
                action = policy(epsilon, state)
                if action == "s":
                    wins()
                    update((points_player, points_dealer), pstate, paction, action, reward_player[-1], alpha)
                    pstate = state
                    paction = action
                    break
                elif action == "h":
                    points_player = play(HIT, cards_player)
                    wins()
                    update((points_player, points_dealer), pstate, paction, action, reward_player[-1], alpha)
                    pstate = state
                    paction = action
                else:
                    print("Illegal choice.")
            if points_player > 21:
                reward_dealer.append(1)
                reward_player.append(-1)
            
            else:                         
                while points_dealer <= 17:
                    points_dealer = play(HIT, cards_dealer)

                if points_dealer > 21:
                    reward_dealer.append(-1)
                    reward_player.append(1)

                elif points_dealer > points_player:
                    reward_dealer.append(1)
                    reward_player.append(-1)

                elif points_dealer < points_player:
                    reward_dealer.append(-1)
                    reward_player.append(1)
                
                elif points_dealer == points_player:
                    reward_dealer.append(0)
                    reward_player.append(0)

        #print("Cards of dealer are: %s and cards of player are: %s " % (cards_dealer, cards_player))
        #print("Points dealer: %s, and points player %s" % (points_dealer, points_player))
        #print("Reward dealer is %s and reward player is %s" % (reward_dealer, reward_player))
        #input("")

        reward_epsiode_player.append(reward_player[-1])  #epsiodes won

        if action :
            update((points_player, points_dealer), pstate, paction, action, reward_player[-1], alpha)
            pstate = state
            paction = action

        # Needed for path percentag (plot)
        Win_player = reward_player.count(1)
        Loss_player = reward_player.count(-1)
        Tie_player = reward_player.count(0)
        Total_games = (Loss_player + Tie_player + Win_player)
        Percentage_won = 100*(Win_player / Total_games)
        percentage.append(Percentage_won)

        # empty cards
        cards_dealer = []
        cards_player = []

    # Count the total reward for each player after n rounds
    total_dealer = sum(reward_dealer)
    total_player = sum(reward_player) 
    Win_player = reward_player.count(1)
    Loss_player = reward_player.count(-1)
    Tie_player = reward_player.count(0)
    Total_games = (Loss_player + Tie_player + Win_player)
    Percentage_won = 100*(Win_player / Total_games)

    print("_________________")
    print(Name)
    print("%s steps played in %s episodes" % ((len(reward_player)), interaction ))
    #print("Total dealer:", total_dealer, "\nTotal player:", total_player)
    print("Statistics player: won: %s, lost: %s, tie: %s" % (Win_player, Loss_player, Tie_player))
    print("Percentage player won: %.4f%%" % percentage[-1])
    print("Epsiodes played: %s, episodes won: %s, episodes lost: %s" % (len(reward_epsiode_player), reward_epsiode_player.count(-1), reward_epsiode_player.count(1)))
    print("_________________")


    numbers.extend(list(range(1,(len(percentage)+1))))



##########################################
# Output first graph

MC_path_percentage_1 = []
MC_number_1 = []
QL_path_percentage_1 = []
QL_number_1 = []
S_path_percentage_1 = []
S_number_1 = []

# Best policy in SARSA, Q-Learning and Monte Carlo (1)
epsiode("SARSA", 50000, best_policy, 0.001, 0.1, SARSA, S_path_percentage_1, S_number_1)
epsiode("QL", 50000, best_policy, 0.001, 0.1, QL ,QL_path_percentage_1, QL_number_1)
epsiode("MC", 50000, best_policy, 0.001, 0.1, MC, MC_path_percentage_1, MC_number_1)

#Plot
fig, ax = plt.subplots()
ax.plot(S_number_1, S_path_percentage_1, 'k--', label='SARSA', color='red')
ax.plot(QL_number_1, QL_path_percentage_1, 'k:', label='Q LEARNING', color='blue')
ax.plot(MC_number_1, MC_path_percentage_1, 'k', label='MONTE CARLO', color='green')

plt.xlabel('number of steps')
plt.ylabel("percentage won")
plt.title("Best policy")

legend = ax.legend(loc='lower right', shadow=False, fontsize=10)
legend.get_frame().set_facecolor('0.75')
plt.show()

###############################################
# Output second graph

QL_path_percentage_best = []
QL_number_best = []
QL_path_percentage_epsilon = []
QL_number_epsilon = []
QL_path_percentage_random = []
QL_number_random = []


# Q learning with different policies (with epsilon = 0.01)
epsiode("QL with best", 50000, best_policy, 0.01, 0.001, QL, QL_path_percentage_best, QL_number_best)
epsiode("QL with epsilon greedy (epsilon = 0.001)", 50000, epsilon_greedy_policy, 0.01, 0.001, QL , QL_path_percentage_epsilon, QL_number_epsilon)
epsiode("QL with random", 50000, random_policy, 0.01, 0.001, QL, QL_path_percentage_random, QL_number_random)

# Plot
fig, ax = plt.subplots()
ax.plot(QL_number_best, QL_path_percentage_best, 'k--', label='Best policy', color='red')
ax.plot(QL_number_epsilon, QL_path_percentage_epsilon, 'k:', label='Epsilon greedy policy (0.01)', color='blue')
ax.plot(QL_number_random, QL_path_percentage_random, 'k', label='random policy', color='green')

plt.xlabel('number of steps')
plt.ylabel("percentage won")
plt.title("Q-learning with different policies")

legend = ax.legend(loc='lower right', shadow=False, fontsize=10)
legend.get_frame().set_facecolor('0.75')
plt.show()

###############################################
# Output third graph

QL_path_percentage_epsilon001 = []
QL_number_epislon_001 = []
QL_path_percentage_epsilon01 = []
QL_number_epsilon01 = []
QL_path_percentage_epsilon1 = []
QL_number_epsilon1 = []

# Q learning with different epsilons
epsiode("QL with epsilon greedy (epsilon = 0.001)", 50000, epsilon_greedy_policy, 0.001, 0.001, QL, QL_path_percentage_epsilon001, QL_number_epislon_001)
epsiode("QL with epsilon greedy (epsilon = 0.01)", 50000, epsilon_greedy_policy, 0.01, 0.001, QL ,QL_path_percentage_epsilon01, QL_number_epsilon01)
epsiode("QL with epsilon greddy (epsilon = 0.1)", 50000, epsilon_greedy_policy, 0.1, 0.001, QL, QL_path_percentage_epsilon1, QL_number_epsilon1)

# Plot
fig, ax = plt.subplots()
ax.plot(QL_number_epislon_001, QL_path_percentage_epsilon001, 'k--', label='Epsilon greedy policy (0.001)', color='red')
ax.plot(QL_number_epsilon01, QL_path_percentage_epsilon01, 'k:', label='Epsilon greedy policy (0.01)', color='blue')
ax.plot(QL_number_epsilon1, QL_path_percentage_epsilon1, 'k', label='Epsilon greedy policy (0.1)', color='green')

plt.xlabel('number of steps')
plt.ylabel("percentage won")
plt.title("Q-learning with epsilon greedy policy")

legend = ax.legend(loc='lower right', shadow=False, fontsize=10)
legend.get_frame().set_facecolor('0.75')
plt.show()
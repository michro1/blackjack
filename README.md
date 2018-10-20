# Blackjack \& Reinforcement Learning <!-- omit in toc -->

- [Overview](#overview)
- [Simplifications](#simplifications)
- [Theory](#theory)
    - [Q-learning](#q-learning)
    - [SARSA](#sarsa)
    - [Monte Carlo](#monte-carlo)

## Overview
An agent is set in a Blackjack environment, where he learns through reinforcement learning. Blackjack can be viewed as an episodic finite Markov Decision Process:
* The total reward in an episode equals zero.
* &gamma; = 0 is employed.
* The agent makes decisions based on this current cards and the cards of the dealer.

An ideal strategy for the agent will be to maximize the financial return (number of points) in the long run. Feedback will be given to the agent through the numerical rewards (set of payoffs).

Set of players = {Player, Dealer}  
Set of actions = {hit, stay}  
Set of payoffs = {V(win) = 1, V(lose) = -1, V(tie) = 0}  

Three different methods were used: 
* Q-learning
* SARSA
* Monte Carlo

with three different policies:
* best
* random
* &epsilon;-greedy

## Simplifications
* The agent can just choose between two actions: hit or stay
* The value of the ace is 11
* The time preference parameter is set to one (&gamma; = 1)
* Assumption of perfect information: all cards are open
* There is only one player

## Theory
For the agent to learn I applied Q-learning, SARSA and Monte Carlo. Afterwards I analyzed which method, which policy and which parameters yielded the best results.

### Q-learning
$$ Q(s,a) \leftarrow Q(s,a) + \alpha * [r + \gamma * max_{a'} Q(s',a') - Q(s,a)] $$
where *s* and *a* denote the previous and *s'* and *a'* the current state and action respectively. *Q* is the state-action value, which is always updated with the previous state-action combinations. &alpha; is the learning rate, *r* the instant reward &gamma; the discount factor which is set equal to 1 for simplificaiton.  

The first term on the right-hand side of the equation is the expected reward and the the second term is the actual reward.

### SARSA
$$ Q(s,a) \leftarrow Q(s,a) + \alpha * [r + \gamma * Q(s',a') - Q(s,a)] $$

SARSA is very similar to Q-learning but SARSA takes the effects of exploration into account when it updates the Q-values which can help avoid catastrohic results.

### Monte Carlo
$$ V(s) \leftarrow V(s) + \alpha * [R - V(s)] $$

Monte Carlo averages the sample returns without requiring previous knowledge of the dynamics of the environment. The steps are increment, analyzing the outcomes episode by episode.
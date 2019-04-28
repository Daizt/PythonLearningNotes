import gym
import matplotlib
import numpy as np
import sys	
from collections import defaultdict
from lib.envs.blackjack import BlackjackEnv
from lib import plotting

matplotlib.style.use('ggplot')

env = BlackjackEnv()
# Usage of this env:
# state = env.reset() : Start a new episode, and get an initial state
# state : Consist of (score, dealer_score, usable_ace) 
# next_state, reward, done, _ = env.step(action) : Take an action

def mc_prediction(policy, env, num_episodes, discount_factor=1.0):
	"""
	Monte Carlo prediction algorithm. Calculates the value function
	for a given policy using sampling.
	
	Args:
		policy: A function that maps an observation to action probabilities.
		env: OpenAI gym environment.
		num_episodes: Number of episodes to sample.
		discount_factor: Gamma discount factor.
	
	Returns:
		A dictionary that maps from state -> value.
		The state is a tuple and the value is a float.
	"""

	# Keeps track of sum and count of returns for each state
	# to calculate an average. We could use an array to save all
	# returns (like in the book) but that's memory inefficient.
	returns_sum = defaultdict(float)
	returns_count = defaultdict(float)
	
	# The final value function
	V = defaultdict(float)
	
	# for each episode
	for i_episode in range(1,num_episodes+1):
		# Print out which episode we're on, useful for debugging.
		if i_episode % 1000 == 0:
			print("\rEpisode {}/{}.".format(i_episode, num_episodes), end="")
			sys.stdout.flush()
			
		# Generate an episode
		# An episode is a list of (state, action, reward) tuples
		episode = []
		# reset the env to start a new episode, and get a initial state
		state = env.reset()
		for t in range(100):
			# pick an action accordding to policy
			action = policy(state)
			# take the action
			next_state, reward, done, _ = env.step(action)
			# record the trajectory
			episode.append((state, action, reward))
			if done:
				# print(episode[-1])
				break 
			state = next_state
			
			
		# Find all the states we've visited in this episode
		states_in_episode = set([x[0] for x in episode])
		for state in states_in_episode:
			# find the first occurrence of the state in the episode
			first_occurrence_idx = next((ith for ith, observation in enumerate(episode) if observation[0] == state))
			# sum up all rewards since the first occurrence
			G =  sum([obsv[2]*discount_factor**ith for ith,obsv in enumerate(episode[first_occurrence_idx:])])
			# record total returns of each states, and their first visit numbers
			returns_sum[state] += G
			returns_count[state] += 1
			V[state] = returns_sum[state]/returns_count[state]

	return V


def sample_policy(observation):
	"""
	A policy that sticks if the player score is > 20 and hits otherwise.
	"""
	score, dealer_score, usable_ace = observation
	return 0 if score >= 20 else 1

V_10k = mc_prediction(sample_policy, env, num_episodes=10000)
plotting.plot_value_function(V_10k, title="10,000 Steps")

V_500k = mc_prediction(sample_policy, env, num_episodes=500000)
plotting.plot_value_function(V_500k, title="500,000 Steps")
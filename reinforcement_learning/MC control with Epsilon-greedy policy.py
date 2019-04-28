import gym
import matplotlib
import numpy as np
import sys

from collections import defaultdict
if "../" not in sys.path:
  sys.path.append("../") 
from lib.envs.blackjack import BlackjackEnv
from lib import plotting

matplotlib.style.use('ggplot')

env = BlackjackEnv()

def make_epsilon_greedy_policy(Q, epsilon, nA):
	"""
	Creates an epsilon-greedy policy based on a given Q-function and epsilon.
	
	Args:
		Q: A dictionary that maps from state -> action-values.
			Each value is a numpy array of length nA (see below)
		epsilon: The probability to select a random action . float between 0 and 1.
		nA: Number of actions in the environment.
	
	Returns:
		A function that takes the observation as an argument and returns
		the probabilities for each action in the form of a numpy array of length nA.
	
	"""
	def policy_fn(observation):
		prob = np.zeros(nA, dtype=float)
		max_a = np.argmax(Q[observation])
		prob[max_a] = 1 - epsilon
		prob += epsilon/nA
		return prob
		
	return policy_fn
	
def mc_control_epsilon_greedy(env, num_episodes, discount_factor=1.0, epsilon=0.1):
	"""
	Monte Carlo Control using Epsilon-Greedy policies.
	Finds an optimal epsilon-greedy policy.
	
	Args:
		env: OpenAI gym environment.
		num_episodes: Number of episodes to sample.
		discount_factor: Gamma discount factor.
		epsilon: Chance the sample a random action. Float betwen 0 and 1.
	
	Returns:
		A tuple (Q, policy).
		Q is a dictionary mapping state -> action values.
		policy is a function that takes an observation as an argument and returns
		action probabilities
	"""
	
	# Keeps track of sum and count of returns for each state
	# to calculate an average. We could use an array to save all
	# returns (like in the book) but that's memory inefficient.
	returns_sum = defaultdict(float)
	returns_count = defaultdict(float)
	
	# The final action-value function.
	# A nested dictionary that maps state -> (action -> action-value).
	Q = defaultdict(lambda: np.zeros(env.action_space.n))
	
	# The policy we're following
	policy = make_epsilon_greedy_policy(Q, epsilon, env.action_space.n)
	
	# Implement this!
	# for each episode
	for i_episode in range(1, num_episodes+1):
		if i_episode%1000 == 0:
			print("\rEpisode {}/{}.".format(i_episode, num_episodes),end="")
			sys.stdout.flush()
			
		# Generate an episode
		episode = []
		state = env.reset()
		for t in range(100):
			# pick an action accordding to policy
			action = np.random.choice(range(env.action_space.n),1, p=policy(state))[0]
			# take the action
			next_state, reward, done, _ = env.step(action)
			# record the trajectory
			episode.append((state, action, reward))
			if done:
				break
			state = next_state
		
		# find all first-visit (state, action) pair and average their returns
		state_action_pair = set([tuple(x[0:2]) for x in episode])
		for state_action in state_action_pair:
			# find its first occurrence
			first_occurrence_idx = next((ith for ith, x in enumerate(episode) if tuple(x[0:2]) == state_action))
			# sum up all rewards since the first occurrence
			G = sum([observation[2]*discount_factor**ith for ith, observation in enumerate(episode[first_occurrence_idx:])])
			# record total returns of each (state, action) pair and their first-visit numbers
			returns_sum[state_action] += G
			returns_count[state_action] += 1
			# update Q(s,a) and epsilon-greedy policy
			Q[state_action[0]][state_action[1]] = returns_sum[state_action]/returns_count[state_action]
			# our policy is updated implicitly
			# policy = make_epsilon_greedy_policy(Q, epsilon, env.action_space.n)
			
	return Q, policy
	
Q, policy = mc_control_epsilon_greedy(env, num_episodes=500000, epsilon=0.1)

# For plotting: Create value function from action-value function
# by picking the best action at each state
V = defaultdict(float)
for state, actions in Q.items():
	print(state, actions)
	action_value = np.max(actions)
	V[state] = action_value
plotting.plot_value_function(V, title="Optimal Value Function")
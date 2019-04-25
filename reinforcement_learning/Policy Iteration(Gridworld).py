# Implement Policy Iteration in Python (Gridworld)

import numpy as np
import pprint
import sys
from lib.envs.gridworld import GridworldEnv

pp = pprint.PrettyPrinter(indent=2)
env = GridworldEnv()

# Taken from Policy Evaluation Exercise!

def policy_eval(policy, env, discount_factor=1.0, theta=0.00001):
	"""
	Evaluate a policy given an environment and a full description of the environment's dynamics.
	
	Args:
		policy: [S, A] shaped matrix representing the policy.
		env: OpenAI env. env.P represents the transition probabilities of the environment.
			env.P[s][a] is a list of transition tuples (prob, next_state, reward, done).
			env.nS is a number of states in the environment. 
			env.nA is a number of actions in the environment.
		theta: We stop evaluation once our value function change is less than theta for all states.
		discount_factor: Gamma discount factor.
	
	Returns:
		Vector of length env.nS representing the value function.
	"""
	# Start with a random (all 0) value function
	V = np.zeros(env.nS)
	while True:
		delta = 0
		# For each state, perform a "full backup"
		for s in range(env.nS):
			v = 0
			# Look at the possible next actions
			for a, action_prob in enumerate(policy[s]):
				# For each action, look at the possible next states...
				for  prob, next_state, reward, done in env.P[s][a]:
					# Calculate the expected value
					v += action_prob * prob * (reward + discount_factor * V[next_state])
			# How much our value function changed (across any states)
			delta = max(delta, np.abs(v - V[s]))
			V[s] = v
		# Stop evaluating once our value function change is below a threshold
		if delta < theta:
			break
	return np.array(V)
	
def policy_improvement(env, policy_eval_fn=policy_eval, discount_factor=1.0):
	"""
	Policy Improvement Algorithm. Iteratively evaluates and improves a policy
	until an optimal policy is found.
	
	Args:
		env: The OpenAI envrionment.
		policy_eval_fn: Policy Evaluation function that takes 3 arguments:
			policy, env, discount_factor.
		discount_factor: gamma discount factor.
		
	Returns:
		A tuple (policy, V). 
		policy is the optimal policy, a matrix of shape [S, A] where each state s
		contains a valid probability distribution over actions.
		V is the value function for the optimal policy.
		
	"""
	
	def q(state, V):
		"""
		Helper function to calculate the action values in a given state.
		Args:
			state: The state to consider (int)
			V: The value function to consider (Vector of length env.nS)
			
		Returns:
			Q: A vector of length env.nA containing the action values of
				each (state,action) pair
		"""
		Q = np.zeros(env.nA)
		for a in range(env.nA):
			for prob, next_state, reward, done in env.P[state][a]:
				Q[a] += prob * (reward + discount_factor * V[next_state])
		return Q

	# Initialize a random policy
	policy = np.ones([env.nS, env.nA])/env.nA
	
	while True:
		# Perform policy evaluation on previous policy
		V = policy_eval_fn(policy, env, discount_factor)
		
		# Policy stable flag
		# This will be set to False if we make any change to the previous policy
		policy_stable = True
		
		# Perform policy improvement
		# For each state, adjust the previous policy
		for s in range(env.nS):
			# The best action of previous policy
			prev_a = np.argmax(policy[s])
			
			# Find the best action of current policy 
			action_values = q(s,V)
			current_a = np.argmax(action_values)
			
			# Greedily update the policy
			policy[s] = np.eye(env.nA)[current_a]
			if current_a != prev_a:
				policy_stable = False

		# Check if policy is stable
		if policy_stable:
			break
	
	return policy, V
	

policy, v = policy_improvement(env)
print("Policy Probability Distribution:")
print(policy)
print("")

print("Reshaped Grid Policy (0=up, 1=right, 2=down, 3=left):")
print(np.reshape(np.argmax(policy, axis=1), env.shape))
print("")

print("Value Function:")
print(v)
print("")

print("Reshaped Grid Value Function:")
print(v.reshape(env.shape))
print("")

# Test the value function
expected_v = np.array([ 0, -1, -2, -3, -1, -2, -3, -2, -2, -3, -2, -1, -3, -2, -1,  0])
np.testing.assert_array_almost_equal(v, expected_v, decimal=2)
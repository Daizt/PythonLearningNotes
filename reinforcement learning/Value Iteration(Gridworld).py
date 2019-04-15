import numpy as np
import pprint
import sys
if "../" not in sys.path:
  sys.path.append("../") 
from lib.envs.gridworld import GridworldEnv

pp = pprint.PrettyPrinter(indent=2)
env = GridworldEnv()

def value_iteration(env, theta=0.0001, discount_factor=1.0):
	"""
	Value Iteration Algorithm.
	
	Args:
		env: OpenAI env. env.P represents the transition probabilities of the environment.
			env.P[s][a] is a list of transition tuples (prob, next_state, reward, done).
			env.nS is a number of states in the environment. 
			env.nA is a number of actions in the environment.
		theta: We stop evaluation once our value function change is less than theta for all states.
		discount_factor: Gamma discount factor.
		
	Returns:
		A tuple (policy, V) of the optimal policy and the optimal value function.		
	"""
	
	def q(state, V):
		"""
		A helper function that calculate all possible action values q(s,a) of a 
		state given current value functions V.
		
		Args:
			state: A specified state.
			V: Current value functions.
			
		Returns:
			Q of Size 1 x env.nS, which contain all the action values q(s,a).
		"""
		
		Q = np.zeros(env.nA)
		for a in range(env.nA):
			for prob, next_state, reward, done in env.P[state][a]:
				Q[a] += prob * (reward + discount_factor * V[next_state])
		return Q
		
	V = np.zeros(env.nS)
	policy = np.zeros([env.nS, env.nA])
	
	# update value functions until converge
	while True:
		delta = 0
		# for each state
		for state in range(env.nS):
			# calculate new value function
			v = np.max(q(state, V))
			# save the largest change among all state values
			delta = max(delta, np.abs(v - V[state]))
			# update value function
			V[state] = v
		if delta < theta:
			break

	# update policy
	for state in range(env.nS):
		policy[state] = np.eye(env.nA)[np.argmax(q(state, V))]
	
	return policy, V
	
policy, v = value_iteration(env)

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
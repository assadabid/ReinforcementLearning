# -*- coding: utf-8 -*-
"""SarsaLambda_LunarLander.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1W9qzw4Wt5bC_Xap9UroyYkv2MyxgYiYl
"""

!apt-get update -qq
!apt-get install -y build-essential
!apt-get install -y swig

!pip install gymnasium[box2d]

import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

env = gym.make("LunarLander-v2")

alpha = 0.1  # Learning rate
gamma = 0.95  # Discount factor
lambda_ = 0.8  # Eligibility trace decay factor
epsilon = 0.2  # Exploration factor
num_episodes = 2000  # Number of episodes

Q_table = {}
E_trace = {}  # Eligibility trace


def epsilon_greedy(state, epsilon):
    if np.random.random() < epsilon:
        return env.action_space.sample()
    else:
        return get_best_action(state)


def get_best_action(state):
    q_values = Q_table.get(tuple(state), np.zeros(env.action_space.n))
    return np.argmax(q_values)


def sarsa_lambda_update(state, action, reward, next_state, next_action):
    q_current = Q_table.get(tuple(state), np.zeros(env.action_space.n))
    q_next = Q_table.get(tuple(next_state), np.zeros(env.action_space.n))
    delta = reward + gamma * q_next[next_action] - q_current[action]

    e_current = E_trace.get(tuple(state), np.zeros(env.action_space.n))
    e_current[action] += 1  # Increment eligibility trace for the current state-action pair

    for s, q_values in Q_table.items():
        e_values = E_trace.get(s, np.zeros(env.action_space.n))
        Q_table[s] = q_values + alpha * delta * e_values  # Update rule using eligibility trace
        E_trace[s] = gamma * lambda_ * e_values  # Decay eligibility trace

    E_trace[tuple(state)] = e_current


returns = []
for episode in range(num_episodes):
    state, info = env.reset()
    action = epsilon_greedy(state, epsilon)
    total_reward = 0
    done = False
    while not done:
        next_state, reward, done, truncated, info = env.step(action)
        next_action = epsilon_greedy(next_state, epsilon)
        sarsa_lambda_update(state, action, reward, next_state, next_action)
        state = next_state
        action = next_action
        total_reward += reward
    returns.append(total_reward)
    if episode % 100 == 0:
        print(f"Episode {episode}, Total reward: {total_reward}")

plt.figure(figsize=(14, 5))
plt.plot(returns)
plt.xlabel('Episode')
plt.ylabel('Cumulative Reward')
plt.title('Returns per Episode (SARSA(λ) in Lunar Lander)')
plt.show()


def simulate_learned_strategy(num_simulations=100):
    time_steps_to_goal = []  # List to track the time steps to achieve the goal

    for simulation in range(num_simulations):
        state, info = env.reset()
        time_step = 0
        done = False
        while not done:
            action = get_best_action(state)
            next_state, reward, done, truncated, info = env.step(action)
            state = next_state
            time_step += 1
        time_steps_to_goal.append(time_step)

    average_time_steps = np.mean(time_steps_to_goal)
    print(f"Average time step calculated: {average_time_steps}")
    env.close()
    return average_time_steps


average_time_steps = simulate_learned_strategy(num_simulations=100)
print(f"Average time step to achieve the goal using the learned strategy: {average_time_steps}")

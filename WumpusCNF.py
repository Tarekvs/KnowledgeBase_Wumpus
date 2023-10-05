import gym
import random
import fh_ac_ai_gym

from KBcnf import *


# MAIN FILE ONLY USED TO MOVE WUMPUS AND ASK/TELL KNOWLEDGE BASE

wumpus_env = gym.make('Wumpus-v0')
observation = wumpus_env.reset()
kb = KnowledgeBaseCNF()


x,y  = [observation['x'], observation['y']]

# add the HornClause to the knowledge base
kb.tell(observation)
# print the Horn clauses in the knowledge base
wumpus_env.render()
#First Check is Wumpus in 1,0 FALSE
kb.print_kb()
print(kb.ask("W10"))
print("W10 Before moving up")


observation= wumpus_env.step(1)[0]
observation= wumpus_env.step(0)[0]
kb.tell(observation)
wumpus_env.render()
kb.print_kb()
#First Check is Wumpus in 1,0 TRUE

print(kb.ask("W10"))
print("W10 After moving up")

observation= wumpus_env.step(0)[0]
kb.tell(observation)
# First Check is Pit in 1,2 FALSE
wumpus_env.render()
kb.print_kb()
print(kb.ask("P12"))
print("P12 before circling around")


observation= wumpus_env.step(0)[0]
kb.tell(observation)
# print(kb.ask("P12"))
# print("P12 after circling around")



observation= wumpus_env.step(2)[0] 
observation= wumpus_env.step(0)[0]
kb.tell(observation)

observation= wumpus_env.step(0)[0]
kb.tell(observation)

observation= wumpus_env.step(2)[0]
observation= wumpus_env.step(0)[0]
kb.tell(observation)

observation= wumpus_env.step(0)[0]
kb.tell(observation)

observation= wumpus_env.step(2)[0]
observation= wumpus_env.step(0)[0]
wumpus_env.render()
kb.tell(observation)

observation= wumpus_env.step(0)[0]
kb.tell(observation)
wumpus_env.render()
kb.print_kb()
print(kb.ask("P12"))
print("P12 after circling around")


# wumpus_env.render()
# print("P12 after circling around")
# print(kb.ask("P12"))







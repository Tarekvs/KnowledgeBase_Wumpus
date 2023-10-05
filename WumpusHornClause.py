import gym
import random
import fh_ac_ai_gym

from KBhornclause import *
# MAIN FILE ONLY USED TO MOVE WUMPUS AND ASK/TELL KNOWLEDGE BASE

wumpus_env = gym.make('Wumpus-v0')
observation = wumpus_env.reset()
kb = KnowledgeBaseHorn()


x,y  = [observation['x'], observation['y']]

# add the HornClause to the knowledge base
kb.tell(observation)

# print the Horn clauses in the knowledge base
kb.ask("W10")


observation= wumpus_env.step(1)[0]
observation= wumpus_env.step(0)[0]
kb.tell(observation)
kb.ask("W10")


observation= wumpus_env.step(0)[0]
kb.tell(observation)
kb.ask("P12")
wumpus_env.render()


observation= wumpus_env.step(0)[0]
kb.tell(observation)


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
kb.tell(observation)

observation= wumpus_env.step(0)[0]
kb.tell(observation)

wumpus_env.render()



kb.print_kb()

kb.ask("P12")


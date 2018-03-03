# Executioner:
# State: {P, M, W, L, O}: {Pattern, Misses, Words, Letter, Opponent}
# Action: Add L to P or to M
# Transition: T({P, M, W, L, O}, A) => P', M', W', L', O
#       P', M' and W' are deterministic and follow hangman rules
#       L' is determined by the Guesser
#       O stays the same. I hope.
# Reward: R({P, M, L, W}, A) => 
#       1. G > 6  (Game lost)
#       2. H(W) (Maximize entropy of possible words)
#       3. |W| (Maximize number of possible words)
#       4. A adds to P (Made them guess a bad letter)

# Guesser:
# State: {P, M, W, L}: {Pattern, Misses, Words, LastLetter}
# Action: Pick a letter L'
# Transition: T({P, M, W, L, O}, A) => P', M', W', L', O
#       P' and M' are determined by the Executioner.
#       W is updated according to hangman rules.
#       L' is L' from the action
#       O stays the same. I hope.
# Reward: R({P, M, W, L}, A) => 
#       1. G > 6 = -1 (Game won)
#       2. 1 - H(W)  (Minimize entropy of possible words)
#       3. 1 - |W|  (Minimize number of possible words)
#       4. L in P' (Guessed a good letter)

from enum import Enum
import copy
import hangman_utils as utils

class State:
    def __init__(self, pattern, misses, words, letter):
        self.pattern = pattern
        self.misses = misses
        self.letter = letter
        self.words = words

    def copy(self):
        return copy.deepcopy(self)

class RewardFunction(Enum):
    GREEDY = 4
    COUNT = 3
    ENTROPY = 2
    VICTORY = 1

class Executioner:

    @staticmethod
    def reward(state, action):
        return 0

    @staticmethod
    def transition(state, action):
        s = state
        s_ = state.copy()
        # the miss action
        if action[0] == -1:
            s_.misses = s.misses + [s.letter]
        else:
            for a in action:
                assert s.pattern[a] == utils.BLANK, "tried to add to non blank space"
                s_.pattern = s_.pattern[:a] + s.letter + s_.pattern[a + 1:]


        s_.words = utils.get_matches(s_.pattern, s_.misses, s.words)

        s_.letter = Executioner.opponent().act(s_)
        return s_


    # returns a list of numbers. either [-1] for miss or 
    # a list of indices in the pattern
    @staticmethod
    def act(state):
        return 0

    @staticmethod
    def opponent():
        return Guesser()

class Guesser:
    @staticmethod
    def reward(state, action):
        return 0

    @staticmethod
    def transition(state, action):
        return state

    # returns a letter
    @staticmethod
    def act(state):
        return 'a'

    @staticmethod
    def opponent():
        return Executioner()

class Hangman:
    def __init__(self, words):
        self.executioner = Executioner()
        self.guesser = Geusser()
        self.words = words


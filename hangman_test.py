from hangman import *
import hangman_utils as utils


all_words = utils.load_words()
small_words = ["bee", "tee", "fee", "ben", "ten", "fen"]

def testStateCopy():
    s = State("_____", [], small_words, 'a')
    s_ = s.copy()
    s.letter = 'b'
    assert s.letter is 'b'
    assert s_.letter is 'a'


def testExecutionerTransition_AddToPattern():
    s = State("_____", [], small_words, 'a')
    assert Executioner.transition(s, [0]).pattern == "a____"
    assert Executioner.transition(s, [1]).pattern == "_a___"
    assert Executioner.transition(s, [0, 1, 3]).pattern == "aa_a_"
    s = State("b____", [], small_words, 'a')
    assert Executioner.transition(s, [1]).pattern == "ba___"
    s = State("b____", [], small_words, 'a')
    assert Executioner.transition(s, [1]).pattern == "ba___"

    try:
        s = State("b____", [], small_words, 'a')
        Executioner.transition(s, [0]).pattern == "ba___"
        assert False, "Failed to fail"
    except: 
        assert True

def testExecutionerTransition_AddToMisses():
    s = State("_____", [], small_words, 'a')
    assert Executioner.transition(s, [-1]).misses == ['a']
    s = State("_____", ['a'], small_words, 'b')
    assert Executioner.transition(s, [-1]).misses == ['a', 'b']

def testExecutionerTransition_NewWords():
    s = State("___", [], small_words, 'n')
    assert Executioner.transition(s, [2]).words == ["ben", "ten", "fen"]

    s = State("___", [], small_words, 'n')
    assert Executioner.transition(s, [-1]).words == ["bee", "tee", "fee"]

    s = State("___", [], small_words, 'e')
    assert Executioner.transition(s, [2]).words == []

def testExecutionerTransition_Opponent():
    s = State("___", [], small_words, 'n')
    assert Executioner.transition(s, [2]).letter == 'a'
        
def testAll():
    testStateCopy()
    testExecutionerTransition_AddToPattern()
    testExecutionerTransition_AddToMisses()
    testExecutionerTransition_NewWords()
    testExecutionerTransition_Opponent()

testAll()

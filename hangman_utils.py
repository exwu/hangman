import json

BLANK = "_"

def load_words():
    return [k for k in json.load(open("words.json"))]

def get_single_match(index, letter, words):
    return [word for word in words if len(word) > index and word[index] == letter]

def in_all_sets(word, sets):
    for word_set in sets:
        if word not in word_set:
            return False
    return True

def pattern_to_letter_index(pattern):
    # Spaces represent unmatched words
    constraints = []
    for i in range(len(pattern)):
        if not pattern[i] == BLANK:
            constraints.append((i, pattern[i]))
    return constraints

def get_words_of_length(length, words):
    return [word for word in words if len(word) == length]

def get_matches(pattern, misses, words):
    matches = get_words_of_length(len(pattern), words)

    # Remove words that have letters that have already been guessed
    matches = [word for word in matches if not has_any_char(misses, word)]

    # Remove words that don't fit the pattern
    constraints = pattern_to_letter_index(pattern)
    if len(constraints) > 0: 
        match_sets = [get_single_match(letter, index, matches) for letter, index in constraints]
        shortest = min(match_sets, key=lambda m: len(m))
        matches = [word for word in shortest if in_all_sets(word, match_sets)]
        
    # Remove words with letters that are already in the pattern
    matches = [match for match in matches if not has_extra_char(pattern, match)]
    return matches

def has_any_char(misses, word):
    return any([c in word for c in misses])


def has_extra_char(pattern, word):
    return any([c in pattern and pattern[i] != c for i, c in enumerate(word)])
    
all_letters = [char for char in "abcdefghijklmnopqrstuvwxyz"]
def add_constraints(base_pattern, letters):
    if not base_pattern and not pattern_length: 
        return[]
    if not base_pattern:
        base_pattern = "".join([BLANK for _ in range(pattern_length)])
    patterns = []
    for i in range(len(base_pattern)):
        # For each blank space
        if base_pattern[i] == BLANK:
            for letter in letters:
                # Replace that character
                new_pattern = "".join([c if i != j else letter for j, c in enumerate(base_pattern)])
                patterns.append(new_pattern)
    return patterns

def generate_patterns(base_pattern, num_constraints, letters):
    if (num_constraints == 1):
        return add_constraints(base_pattern, letters)
    new_patterns = add_constraints(base_pattern, letters)
    all_patterns = []
    for pattern in new_patterns:
        all_patterns += generate_patterns(pattern, num_constraints - 1, letters)
    # TODO: make this more efficient
    return list(set(all_patterns))

def matches_for_patterns(patterns, misses, words, base_pattern=None):
    if base_pattern:
        words = get_matches(base_pattern, misses, words)
    return {pattern: get_matches(pattern, misses, words) for pattern in patterns}

def best_patterns(patterns, misses, words, base_pattern=None):
    matches = matches_for_patterns(patterns, misses, words, base_pattern)
    sorted_patterns = sorted([pattern for pattern in patterns if len(matches[pattern]) > 0], key=lambda p: 0 - len(matches[p]))
    return [(pattern, len(matches[pattern])) for pattern in sorted_patterns]

def best_hangman_move(base_pattern, misses, letter, words):
    return best_patterns(generate_patterns(base_pattern, 1, letter), misses, words)[0]


words = load_words()





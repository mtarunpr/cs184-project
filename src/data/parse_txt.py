# Definitions, Theorems/Lemmas, Fixpoints, etc.
from pathlib import Path
import numpy as np


# Theorem class
class Theorem:
    # Theorem has name, statement, possible set of steps, and preamble
    name: str
    statement: str
    steps: list[str]
    preamble: list[str]

    # Given a preamble, we want to get a list of all facts, definitions, fixed points, theorems, lemmas, etc
    # We just want the name
    keywords: list[str]

    def __init__(
        self,
        name: str,
        statement: str,
        steps: list[str],
        preamble: list[str],
        keywords: list[str],
    ):
        self.name = name
        self.statement = statement
        self.steps = steps
        self.preamble = preamble
        self.keywords = keywords

    def __str__(self):
        curr_str = self.name
        for step in self.steps:
            curr_str += " / " + step

        return curr_str

    # Get a random data point from a theorem by randomly picking a number of steps
    # We then return these steps
    def get_random_state(self):
        curr_state = []

        if len(self.steps) > 0:
            num_states = np.random.randint(len(self.steps) + 1)

            for i in range(0, num_states - 1):
                curr_state.append(self.steps[i])

        return curr_state


# List of all docs and keys for import
FILES_ORDER = [
    "missing.v",
    "tactics.v",
    "division.v",
    "euclide.v",
    "permutation.v",
    "power.v",
    "gcd.v",
    "primes.v",
    "nthroot.v",
]
IMPORT_KEYS = [
    "missing",
    "tactics",
    "division",
    "euclide",
    "permutation",
    "power",
    "gcd",
    "primes",
    "nthroot",
]


import_strings = {}
keywords_map = {}


# Gets data from one file
def parse_file(file_name: str, import_strings, file_key, theorems, path, keywords_map):
    print("PARSING " + file_name)
    making_theorem = False
    curr_name = ""
    curr_title = ""
    curr_steps = []
    curr_file = []
    file = open(path / file_name, "r")
    preamble = []
    curr_keywords = []

    # Get all lines
    lines = file.readlines()

    for line in lines:
        # Skip out comments
        if line.startswith("(*"):
            continue

        # Get imports and add them to preamble
        if line.startswith("Require Import"):
            key = line[len("Require Import") + 1 : -2]
            if key in IMPORT_KEYS:
                preamble += import_strings[key]
                curr_keywords += keywords_map[key]
            else:
                preamble += [line.strip()]
            continue

        # We can skip Exports probably and empty lines
        if line.startswith("Export"):
            continue
        if len(line.strip()) == 0:
            continue

        # Otherwise add the line to our data
        curr_file.append(line.strip())

        if line.startswith("Fact"):
            index = 5
            end_index = index + 1
            while line[end_index] != ":":
                end_index += 1
            keyword = line[index:end_index]
            keyword = keyword.strip()
            curr_keywords.append(keyword)
            # print(keyword)
            continue

        if line.startswith("Definition"):
            index = 11
            end_index = index + 1
            while line[end_index] != "(":
                end_index += 1
            keyword = line[index:end_index]
            keyword = keyword.strip()
            curr_keywords.append(keyword)
            # print(keyword)
            continue

        if line.startswith("Fixpoint"):
            index = 9
            end_index = index + 1
            while line[end_index] != "(":
                end_index += 1
            keyword = line[index:end_index]
            keyword = keyword.strip()
            curr_keywords.append(keyword)
            # print(keyword)
            continue

        # Indications to start batching data to put into a block
        if line.startswith("Lemma") or line.startswith("Theorem"):
            making_theorem = True
            curr_title = line.strip()

            index = 0
            if line.startswith("Lemma"):
                index = 6
            else:
                index = 8

            end_index = 0
            while line[end_index] != ":":
                end_index += 1
            curr_name = line[index:end_index]
            curr_name = curr_name.strip()

            continue

        # If we finish a proof, then we make all of the values into a theorem
        if line.startswith("Qed.") and making_theorem:
            making_theorem = False

            new_theorem = Theorem(
                curr_name, curr_title, curr_steps, preamble, curr_keywords
            )

            # Add theorem and reset
            theorems.append(new_theorem)
            curr_keywords.append(curr_name)

            curr_name = ""
            curr_title = ""
            curr_steps = []

        # If in a bathc, add lines to the batch
        if making_theorem:
            curr_steps.append(line.strip())

    file.close()

    # Then we store the file as a preamble for future imports
    curr_file = preamble + curr_file
    import_strings[file_key] = curr_file
    keywords_map[file_key] = curr_keywords

    # for theorem in theorems:
    #     print(theorem.get_random_state())
    #     print("--------------")


# Iterate over all files to get data
def get_all_theorems(path):
    theorems: tuple[Theorem] = []
    for i, file_name in enumerate(FILES_ORDER):
        file_key = IMPORT_KEYS[i]
        parse_file(file_name, import_strings, file_key, theorems, path, keywords_map)

    return theorems


if __name__ == "__main__":
    theorems = get_all_theorems(Path(__file__).parent / "raw")
    print(theorems[-10].preamble)

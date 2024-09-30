# Name:
# Student Number:

# This file is provided to you as a starting point for the "wordchain.py" program of Project
# of CSI6208 in Semester 2, 2024.  It aims to give you just enough code to help ensure
# that your program is well structured.  Please use this file as the basis for your assignment work.
# You are not required to reference it.

# The "pass" command tells Python to do nothing.  It is simply a placeholder to ensure that the starter files run smoothly.
# They are not needed in your completed program.  Replace them with your own code as you complete the assignment.

# Import the necessary modules.
import json

import random
import urllib.request
from datetime import datetime

# This function repeatedly prompts for input until the user enters
# something at least one character long and entirely alphabetic.
def input_word(prompt):
    return input(prompt).lower()


def word_chain_game():
    api_key = "b7dghzb5k4j5ewthefzc6qjkp4gnwklxjf3ume4krcnfj28ul"
    chain = 0
    word_types = ["noun", "verb", "adjective"]
    player_names = []
    used_words = []
    word_count = {"noun": 0, "verb": 0, "adjective": 0}
    min_len = 3

    print("Welcome to WordChain!")

    while True:
        try:
            num_players = int(input("How many players (minimum of 2)?: "))
            if num_players >= 2:
                break
            print("Please enter a number 2 or greater")
        except ValueError:
            print("Please enter a valid number")

    for i in range(num_players):
        while True:
            name = input(f"Enter name of player {i+1}: ")
            if name in player_names:
                print("Name already taken, please enter a different name")
            else:
                player_names.append(name)
                break

    print()
    current_player = 0
    round = 0

    while True:
        player = player_names[current_player]
        word_type = random.choice(word_types)

        if chain == 0:
            starting_letter = random.choice("abcdefghijklmnopqrstuvwxyz").upper()
        else:
            starting_letter = used_words[-1][-1].upper()

        print(f"{player} is up next.")
        print(
            f"Enter {'an' if word_type[0] in 'aeiou' else 'a'} {word_type} beginning with \"{starting_letter}\" (min length {min_len})!"
        )
        word = input_word("> ")

        if len(word) < min_len:
            print(f'Word chain broken - "{word}" is too short (min length {min_len})!')
            break

        url = f"https://api.wordnik.com/v4/word.json/{word}/definitions"
        params = f"limit=5&includeRelated=false&useCanonical=false&includeTags=false&api_key={api_key}"

        try:
            full_url = f"{url}?{params}"
            with urllib.request.urlopen(full_url) as response:
                if response.getcode() == 200:
                    data = response.read().decode("utf-8")
                    definitions = json.loads(data)

                    word_type_map = {
                        "noun": ["noun"],
                        "verb": ["verb", "intransitive verb", "transitive verb"],
                        "adjective": ["adjective", "adverb"],
                    }

                    matching_def = next(
                        (
                            d
                            for d in definitions
                            if d.get("partOfSpeech") in word_type_map.get(word_type, [])
                        ),
                        None,
                    )

                    if matching_def and word[0].upper() == starting_letter:
                        chain += 1
                        used_words.append(word)
                        word_count[word_type] += 1
                        definition = matching_def.get("text", "No definition available")
                        definition = "".join(
                            char for char in definition if char not in "<>"
                        )
                        print(
                            f'Good job, {player} - "{word}" is a {word_type} defined as...'
                        )
                        print(
                            f"  • {definition[:60]}{'...' if len(definition) > 60 else ''}"
                        )
                        print()
                        print(
                            f"The word chain is now {chain} link{'s' if chain > 1 else ''} long!"
                        )
                    else:
                        print(
                            f'Word chain broken - "{word}" does not appear to be a {word_type}!'
                        )
                        break
                else:
                    print(f'Word chain broken - "{word}" could not verified!')
                    break
        except Exception as e:
            print(f"Error connecting to the API using simple validation")
            if len(word) > min_len and word not in used_words:
                chain += 1
                used_words.append(word)
                word_count[word_type] += 1
                print(f'Accepted "{word}" without verification')
                print(
                    f"The word chain is now {chain} link{'s' if chain > 1 else ''} long!"
                )
            else:
                print(
                    f'Word chain broken - "{word}" is too short or has been used before!'
                )
                break

        print()
        round += 1
        if round % (num_players * 2) == 0:
            min_len += 1
            print(f"Difficulty increased! New minimum word length: {min_len}")

        current_player = (current_player + 1) % num_players

    print()
    print(f"Final chain length: {chain}")
    print("Game log saved")

    log = {
        "players": num_players,
        "names": player_names,
        "chain": chain,
        "valid_nouns": word_count["noun"],
        "valid_verbs": word_count["verb"],
        "valid_adjectives": word_count["adjective"],
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    try:
        with open("logs.txt", "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(log)

    with open("logs.txt", "w") as f:
        json.dump(logs, f)

    random_word_url = "https://api.wordnik.com/v4/words.json/randomWord"
    random_word_params = f"api_key={api_key}"

    try:
        full_random_word_url = f"{random_word_url}?{random_word_params}"
        with urllib.request.urlopen(full_random_word_url) as random_word_response:
            if random_word_response.getcode() == 200:
                random_word_data = random_word_response.read().decode("utf-8")
                random_word = json.loads(random_word_data).get("word", "No word found")

                random_word_def_url = (
                    f"https://api.wordnik.com/v4/word.json/{random_word}/definitions"
                )
                full_random_word_def_url = f"{random_word_def_url}?{params}"
                with urllib.request.urlopen(
                    full_random_word_def_url
                ) as random_word_def_response:
                    if random_word_def_response.getcode() == 200:
                        random_word_def_data = random_word_def_response.read().decode(
                            "utf-8"
                        )
                        random_word_def = json.loads(random_word_def_data)[0].get(
                            "text", "No definition found"
                        )
                        # Remove HTML tags without using re
                        random_word_def = "".join(
                            char for char in random_word_def if char not in "<>"
                        )

                        print(
                            f"Random word of the day: {random_word} - {random_word_def}"
                        )
                    else:
                        print("Could not retrieve the definition for the random word")
            else:
                print("Could not retrieve a random word from Wordnik")
    except Exception as e:
        print(f"Error retrieving random word: {str(e)}")


if __name__ == "__main__":
    word_chain_game()

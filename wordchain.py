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


# This function repeatedly prompts for input until the user enters
# something at least one character long and entirely alphabetic.
# See the "The 'inputWord' Function" section of the assignment brief.
def input_word(prompt):
    return input(prompt).lower()


def word_chain_game():
    api_key = "b7dghzb5k4j5ewthefzc6qjkp4gnwklxjf3ume4krcnfj28ul"
    chain = 0
    word_types = ["noun", "verb", "adjective"]
    player_names = []
    used_words = []

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
        name = input(f"Enter name of player {i+1}: ")
        player_names.append(name)

    print()
    current_player = 0

    while True:
        player = player_names[current_player]
        word_type = random.choice(word_types)

        if chain == 0:
            starting_letter = random.choice(
                'abcdefghijklmnopqrstuvwxyz').upper()
        else:
            starting_letter = used_words[-1][-1].upper()

        print(f"{player} is up next.")
        print(f"Enter a {word_type} beginning with \"{starting_letter}\"!")
        word = input_word("> ")

        url = f"https://api.wordnik.com/v4/word.json/{word}/definitions"
        params = {
            "limit": 1,
            "includeRelated": "false",
            "useCanonical": "false",
            "includeTags": "false",
            "api_key": api_key
        }

        try:
            # Construct the full URL with parameters
            full_url = url + '?' + \
                '&'.join(f"{k}={v}" for k, v in params.items())

            # Make the request
            with urllib.request.urlopen(full_url) as response:
                if response.getcode() == 200:
                    # Read and decode the response
                    data = response.read().decode('utf-8')
                    definitions = json.loads(data)

                    word_type_map = {
                        "noun": ["noun"],
                        "verb": ["verb", "intransitive verb", "transitive verb"],
                        "adjective": ["adjective", "adverb"]
                    }

                    matching_def = next((d for d in definitions if d.get(
                        "partOfSpeech") in word_type_map.get(word_type, [])), None)

                    if matching_def and word[0].upper() == starting_letter:
                        chain += 1
                        used_words.append(word)
                        definition = matching_def.get(
                            'text', 'No definition available')
                        print(
                            f"Good job, {player} - \"{word}\" is a {word_type} defined as...")
                        print(
                            f"  • {definition[:60]}{'...' if len(definition) > 60 else ''}")
                        print()
                        print(
                            f"The word chain is now {chain} link{'s' if chain > 1 else ''} long!")
                    else:
                        print(
                            f"Word chain broken - \"{word}\" does not appear to be a {word_type}!")
                        break
                else:
                    print(
                        f"Word chain broken - \"{word}\" could not be verified !")
                    break
        except Exception as e:
            print(
                f"Word chain broken - An unexpected error occurred while verifying \"{word}\"!")
            print(f"Error details: {str(e)}")
            break

        print()
        current_player = (current_player + 1) % num_players

    print()
    print(f"Final chain length: {chain}")
    print("Game log saved.")

    log = {
        "players": num_players,
        "names": player_names,
        "chain": chain
    }

    try:
        with open("logs.txt", "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(log)

    with open("logs.txt", "w") as f:
        json.dump(logs, f)


if __name__ == "__main__":
    word_chain_game()

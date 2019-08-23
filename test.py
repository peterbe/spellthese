from string import ascii_lowercase
import random

from textblob import TextBlob
from textblob.en import Spelling

from boynames import names


def get_random_name():
    random_name = correct_name = random.choice(names).lower()

    random_letters = random.sample(list(ascii_lowercase), len(ascii_lowercase))
    for letter in random_letters:
        if letter in random_name:
            if random.random() > 0.5:
                # removal
                random_name = random_name.replace(letter, "", 1)
            elif random.random() > 0.5:
                # injection
                letters = list(random_name)
                letters.insert(random.randint(0, len(letters)), letter)
                random_name = "".join(letters)
            else:
                # swap
                p = random.randint(0, len(random_name) - 2)
                letters = list(random_name)
                a, b = letters[p : p + 2]
                letters[p] = b
                letters[p + 1] = a
                random_name = "".join(letters)
            break
    return correct_name, random_name


def demo(times=5):
    for i in range(times):
        correct, typo = get_random_name()
        print(f"RIGHT: {correct}\tTYPOED: {typo}")

def untrained(times=20):
    rights = 0
    print("ORIGIN         TYPO           RESULT         WORKED?")
    for i in range(times):
        correct, typo = get_random_name()
        b = TextBlob(typo)
        result = str(b.correct())
        right = correct == result
        if right:
            rights += 1
        print(f"{correct:<15}{typo:<15}{result:<15}{'Yes!' if right else 'Fail'}")

    print(f"Right {100 * rights/times:.1f}% of the time")


def trained(times=20):
    rights = 0
    path = "spelling-model.txt"
    spelling = Spelling(path=path)
    spelling.train(" ".join(names), path)
    print("ORIGIN         TYPO           RESULT         WORKED?")
    for i in range(times):
        correct, typo = get_random_name()
        b = spelling.suggest(typo)
        result = b[0][0]
        right = correct == result
        if right:
            rights += 1
        print(f"{correct:<15}{typo:<15}{result:<15}{'Yes' if right else 'Fail'}")
        # if not right:
        #     print(b)

    print(f"Right {100 * rights/times:.1f}% of the time")


def pretrained_adrian():
    import os
    path = "spelling-model-weighted.txt"
    assert os.path.isfile(path), path
    spelling = Spelling(path=path)
    b = spelling.suggest('darian')
    print(b)


if __name__ == "__main__":
    # # demo()
    print("UNTRAINED...")
    untrained()
    print("")
    print("TRAINED...")
    trained()
    # pretrained_adrian()

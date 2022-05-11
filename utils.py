import math
import os
import secrets
import string


class Entropy:

    TYPE_SIZE = {"upper": 26, "lower": 26,  "digit": 10, "special": 33}

    def _poolsize(password: str) -> int:
        types = dict.fromkeys(Entropy.TYPE_SIZE, False)
        pool = 0
        for char in password:

            # NOTE: if all types were recognized stop checking
            if all(types.values()):
                break
            if char.isupper():
                if types["upper"] is False:
                    types["upper"] = True
                    pool += 26
            elif char.islower():
                if types["lower"] is False:
                    types["lower"] = True
                    pool += 26
            elif char.isdigit():
                if types["digit"] is False:
                    types["digit"] = True
                    pool += 10
            else:
                if types["special"] is False:
                    types["special"] = True
                    pool += 33
        return pool

    def get_bits(password: str) -> int:
        size = Entropy._poolsize(password)
        length = len(password)
        possible_combs = size ** length
        entropy_bits = int(math.log2(possible_combs))
        return entropy_bits

    def get_strength(bits: int) -> str:
        if 0 <= bits < 64:
            return "Very week", bits
        elif 64 <= bits < 80:
            return "Week", bits
        elif 80 <= bits < 112:
            return "Moderate", bits
        elif 112 <= bits < 128:
            return "Strong", bits
        else:
            return "Very strong", bits


class PassGenerator:

    # NOTE: poolsize is 95.
    CHAR_POOL = string.ascii_letters + string.digits + string.punctuation + " "

    # NOTE: poolsize is 7776.
    WORD_POOL_FILE = os.path.join(
        os.getcwd(), "eff_wordlist/eff_large_wordlist.txt")
    SETUP: bool = False
    WORD_POOL_DICT = {}

    def setup():
        with open(PassGenerator.WORD_POOL_FILE, "r") as f:
            for line in f:
                num, word = line.strip().split("\t")
                PassGenerator.WORD_POOL_DICT[int(num)] = word
        PassGenerator.SETUP = True

    def new_password(length: int) -> str:
        password = []
        for _ in range(length):
            password.append(secrets.choice(PassGenerator.CHAR_POOL))

        password = "".join(password)
        return password

    def _simulate_five_dice() -> int:
        nums = []
        for _ in range(5):
            nums.append(secrets.choice(['1', '2', '3', '4', '5', '6']))
        return int("".join(nums))

    def new_pass_phrase(word_count: int, delimeter: str = " ") -> str:
        if PassGenerator.SETUP is False:
            PassGenerator.setup()

        password = []
        for _ in range(word_count):
            dice = PassGenerator._simulate_five_dice()
            password.append(PassGenerator.WORD_POOL_DICT.get(dice))
        password = delimeter.join(password)
        return password

    def _hash_func(x, y):
        return (x * y * 7) % 95

    def new_pass_point(pointer_list):
        password = []
        for x, y in pointer_list:
            password.append(chr(PassGenerator._hash_func(x, y) + 26))
        password = "".join(password)
        return password



#!/usr/bin/env python3
import getopt
import os
import sys

import pyperclip

from utils import PassGenerator


SHORT_OPTS = "hcyl:o:"
LONG_OPTS = ["help", "stdout", "yank", "length=", "output="]
DEFAULT_LENGTH = 16


def display_help():
    print("Usage: passgen <commands> <options>")
    print(
        "Commnads:",
        "\tw: create passWord",
        "\tp: create passPhrase",
        sep="\n"
    )
    print(
        "Options:",
        "\t-l <num>, --length <num>:\tchoose lenght of the password/phrase.",
        "\t-o <file>, --output <file>:\tthe output file to write in it.",
        "\t-y, --yank:\tyank password",
        "\t-c, --stdout:\twrite on standard output(will not be echoed !)",
        sep="\n"
    )
    print(
        f"\nWith no length, generate password/phrase of length {DEFAULT_LENGTH}")
    print("With no output method, write on standard output")
    print("Report bugs to: github.com/callmesia")


def write_to_file(file_path: str, text: str) -> bool:
    if not os.path.isabs(file_path):
        file_path = os.path.join(os.getcwd(), file_path)

    # NOTE: EAFP right?
    try:
        with open(file_path, "w") as f:
            f.write(text + "\n")
            return True
    except:
        return False


def main():
    length = DEFAULT_LENGTH
    method = PassGenerator.new_password
    out = print

    # NOTE: command setup phase
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        display_help()
        exit()
    elif sys.argv[1] == "w":
        pass
    elif sys.argv[1] == "p":
        method = PassGenerator.new_pass_phrase
    else:
        print(f"Invalid command: {sys.argv[1]} (see help for more info)")
        exit()

    try:
        # NOTE: option setup phase
        arguments, vals = getopt.getopt(sys.argv[2:], SHORT_OPTS, LONG_OPTS)
        for arg, val in arguments:
            if arg in ("-l", "--length"):
                if val.isdigit():
                    length = int(val)
                else:
                    print("Value for length should be digits!")
            if arg in ("-c", "--stdout"):
                out = print
            elif arg in ("-y", "--yank"):
                out = pyperclip.copy
            elif arg in ("-o", "--output"):
                out = write_to_file
                file_path = val
        generated_pass = method(length)

        # NOTE: output phase
        if out is write_to_file:
            res = out(file_path, generated_pass)
            if res is True:
                print(f"pass path: {file_path}")
            else:
                print("Cannot write pass in the given directory (Permission denied)")
        elif out is pyperclip.copy:
            out(generated_pass)
            print("Pass yanked successfully")
        else:
            print("Your pass is:\n")
            out(generated_pass)
    except getopt.error as err:
        print(err)


if __name__ == "__main__":
    main()


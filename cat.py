import argparse
import sys


def echo():
    """
    This function will print each line of text,
    which will be entered in the terminal.
    """
    for line in sys.stdin:
        if sys.stdin == "EOF":
            break
        else:
            sys.stdout.write(line)


def file_open(a):
    """
    This function will read and print file into the terminal.
    """
    print("fuck")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("a", nargs="?", default="None")
    parser.add_argument("b", nargs="?", default="None")
    parser.add_argument("c", nargs="?", default="None")

    args = parser.parse_args()

    #now, only echo
    if args.a == "None":
        echo()
    elif args.b == "None":
        file_open(args.a)


if __name__ == '__main__':
    main()

import argparse

def echo():
    """
    This function will print each line of text,
    which will be entered in the terminal.
    """
    while True:
        temp = input()
        if temp == "q":
            break
        else:
            print(temp)


def file_open(a):
    """
    This function will read and print file into the terminal.
    """


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

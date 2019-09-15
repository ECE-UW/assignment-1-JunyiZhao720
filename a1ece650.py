import sys

# YOUR CODE GOES HERE


def add():
    print("add() function not implemented!")


def change():
    print("change() function not implemented!")


def remove():
    print("remove() function not implemented!")


def graph():
    print("graph() function not implemented!")


# global------------ #
options = {'a': add, 'c': change, 'r': remove, 'g': graph}
error_msg = {
    'cmd': 'Commands not found! We only support a,c,r,g!'
}
# ------------global #


def parseline(instr):
    line = instr.rstrip().split(' ')
    return line


def main():
    # YOUR MAIN CODE GOES HERE

    # sample code to read from stdin.
    # make sure to remove all spurious print statements as required
    # by the assignment
    while True:
        line = parseline(sys.stdin.readline())
        print line

        cmd = line[0]
        if cmd in options:
            print 'current command: ', cmd
            options[cmd]()
        else:
            print error_msg['cmd']

    # return exit code 0 on successful termination
    # sys.exit(0)


if __name__ == '__main__':
    main()

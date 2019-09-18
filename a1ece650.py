import sys

# YOUR CODE GOES HERE


# global data----------- #
streetDic = {}
error_msg = {
    'cmd': 'Error: Commands not found! We only support a,c,r,g!',
    'format': 'Error: Please follow the format: <command> <street name> <camera positions>',
    'keys': 'Error: The street name already exists. Please re-enter the name or change existing one.',
    'noKeys': 'Error: The street name does not exist.'
}
# ------------global data#


def update():
    print("update() function not implemented!")


def add(line):
    # check format
    if len(line) != 3 or line[2] == '':
        print error_msg['format']
        return
    # check if the name already exists
    if line[1] in streetDic.keys():
        print error_msg['keys']
        return
    # adding
    streetDic[line[1]] = line[2]
    update()


def change(line):
    # check format
    if len(line) != 3 or line[2] == '':
        print error_msg['format']
        return
    # check if the name exists
    if line[1] not in streetDic.keys():
        print error_msg['noKeys']
        return
    # adding
    streetDic[line[1]] = line[2]
    update()


def remove(line):
    # check format
    if len(line) != 2 or line[1] == '':
        print error_msg['format']
        return
    # check if the name exists
    if line[1] not in streetDic.keys():
        print error_msg['noKeys']
        return
    # adding
    del streetDic[line[1]]
    update()


def graph(line):
    print("graph() function not implemented!")


# global constant----------- #
options = {'a': add, 'c': change, 'r': remove, 'g': graph}

# ------------global constant#


def parseline(instr):
    line = instr.strip().replace(' ', '')
    if line == '':
        return []
    # PARSE COMMAND
    cmd = line[0]
    line = line[1:]
    if cmd not in options.keys():
        return []
    if line == '':
        return [cmd]

    # PARSE STREET NAME
    i = 1
    street = ''
    for c in line:
        if c == '(':
            break
        street += c
        i += 1

    # PARSE VERTEX
    line = line[i-1:]
    if line == '':
        return [cmd, street]
    cameras = []
    open_bracket = False
    s = ''
    for c in line:
        if c == '(':
            # continuous two '('
            if open_bracket:
                return []
            open_bracket = True
            continue
        elif c == ')':
            # continuous two ')'
            if not open_bracket:
                return []
            open_bracket = False
            l = s.split(',')
            s = ''
            # check if the input length is correct
            print l
            if len(l) != 2:
                print "tuple error!", l
                return []
            cameras.append((float(l[0]), float(l[1])))
        else:
            s += c
    # print cmd + ' ' + street + ' ', cameras
    return [cmd, street, cameras]


def main():
    # YOUR MAIN CODE GOES HERE

    # sample code to read from stdin.
    # make sure to remove all spurious print statements as required
    # by the assignment
    while True:
        line = parseline(sys.stdin.readline())
        if len(line) > 3 or len(line) == 0:
            print error_msg['format']
            continue

        print line
        cmd = line[0]
        if cmd in options:
            options[cmd](line)
            print streetDic
        else:
            print error_msg['cmd']


if __name__ == '__main__':
    main()

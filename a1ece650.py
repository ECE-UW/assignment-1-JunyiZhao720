import math
import sys
# YOUR CODE GOES HERE


# global data----------- #
streetDic = {}
pubPoints = []
edgeDic = {}

error_msg = {
    'cmd': 'Error: Commands not found! We only support a,c,r,g!',
    'format': 'Error: Please follow the format: <command> <street name> <(x,y)>',
    'keys': 'Error: The street name already exists. Please re-enter the name or change existing one.',
    'noKeys': 'Error: The street name does not exist.'
}
# ------------global data#


def update():
    # update the new edges based on streetDic
    storeEdges()
    # initialize dic for visit check
    visited = {}
    for key in streetDic.keys():
        visited[key] = False

    # MAIN LOOP
    for key1 in edgeDic.keys():
        visited[key1] = True
        for key2 in edgeDic.keys():
            if visited[key2]:
                continue
            for entry1 in edgeDic[key1]:
                for entry2 in edgeDic[key2]:
                    result = intersectCal(entry1[0], entry1[1], entry2[0], entry2[1])
                    edgeDic[key1].remove(entry1)
                    # if emtpy
                    if result:
                        continue
                    # found new dots
                    else:
                        # edgeDic[key1].append((result[0], result[4]), (result[1], result[4]))

    print edgeDic


def storeEdges():
    for key in streetDic.keys():
        edgeDic[key] = []
        for i in range(len(streetDic[key]) - 1):
            edgeDic[key].append((streetDic[key][i], streetDic[key][i+1]))


def dis((x1, y1), (x2, y2)):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


def intersectCal((x1, y1), (x2, y2), (x3, y3), (x4, y4)):
    # COMMON POINT
    # check if points are x-same -> []
    if x1 == x2 and x3 == x4:
        return []
    elif x1 == x2 and x3 != x4:
        # edge 2
        a2 = (y4 - y3) / (x4 - x3)
        b2 = y3 - a2 * x3
        x = x1
        y = a2 * x + b2
    elif x1 != x2 and x3 == x4:
        # edge 1
        a1 = (y2 - y1) / (x2 - x1)
        b1 = y1 - a1 * x1
        x = x3
        y = a1 * x + b1
    else:
        # edge 1
        a1 = (y2 - y1) / (x2 - x1)
        b1 = y1 - a1 * x1
        # edge 2
        a2 = (y4 - y3) / (x4 - x3)
        b2 = y3 - a2 * x3
        # check if points are a-same -> []
        if a1 == a2:
            return []
        print a1, ' & ', b1
        print a2, ' & ', b2
        # check if a are the same -> []
        if a1 == a2:
            return []
        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1
        print x, ' , ', y

    # DISTANCE CHECK
    # check if dx1>d1, dx2>d1, dx3>d2, dx4>d2 -> []
    d1 = dis((x1, y1), (x2, y2))
    d2 = dis((x3, y3), (x4, y4))
    dx1 = dis((x, y), (x1, y1))
    dx2 = dis((x, y), (x2, y2))
    dx3 = dis((x, y), (x3, y3))
    dx4 = dis((x, y), (x4, y4))
    print d1, d2
    print dx1, dx2, dx3, dx4
    if dx1 > d1 or dx2 > d1 or dx3 > d2 or dx4 > d2:
        return []
    return [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x, y)]



def add(line):
    # check format
    if len(line) != 3 or line[2] == '' or len(line[2]) == 0:
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
    if len(line) != 3 or line[2] == '' or len(line[2]) == 0:
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
    del edgeDic[line[1]]
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
    # check if cmd is empty -> []
    # check if cmd is known commands -> []
    # check if lines after cmd are emtpy -> [cmd]
    cmd = line[0]
    line = line[1:]
    if cmd not in options.keys():
        return []
    if line == '':
        return [cmd]

    # PARSE STREET NAME
    i = 0
    street = ''
    for c in line:
        if c == '(':
            break
        street += c
        i += 1

    # PARSE VERTEX
    # check if street name is empty -> []
    # check if error brackets '(( or ))' -> []
    # check if tuple num is 2 -> []
    line = line[i:]
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


def masterCode():
    # sample code to read from stdin.
    # make sure to remove all spurious print statements as required
    # by the assignment
    while True:
        line = parseline(sys.stdin.readline())
        print len(line)
        if len(line) > 3 or len(line) == 0:
            print error_msg['format']
            continue
        cmd = line[0]
        if cmd in options:
            options[cmd](line)
        else:
            print error_msg['cmd']


def testCode():
    A = (3.0, 8.0)
    B = (5.0, 6.0)
    C = (4.0, 2.0)
    D = (4.0, 8.0)
    # storeIntoPubPoints(A, pubPoints)
    # storeIntoPubPoints(B, pubPoints)
    # storeIntoPubPoints(C, pubPoints)
    # storeIntoPubPoints(D, pubPoints)
    print intersectCal(A, B, C, D)
    print pubPoints
    #print storeIntoPubPoints(B, pubPoints)

def main():
    masterCode()
    # testCode()



if __name__ == '__main__':
    main()

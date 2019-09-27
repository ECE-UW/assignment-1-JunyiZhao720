import math
import sys
# YOUR CODE GOES HERE


# global data----------- #
streetDic = {}
pubPoints = {}
edgeDic = {}

error_msg = {
    'cmd': 'Error: Commands not found! We only support a,c,r,g!',
    'format': 'Error: Please follow the format: <command> <street name> <(x,y)>',
    'keys': 'Error: The street name already exists. Please re-enter the name or change existing one.',
    'noKeys': 'Error: The street name does not exist.'
}
# ------------global data#


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
        # check if a are the same -> []
        if a1 == a2:
            if x2 == x3 and y2 == y3:
                return [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x2, y2)]
            elif x1 == x4 and y1 == y4:
                return [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x1, y1)]
            else:
                return []
        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1

    # DISTANCE CHECK
    # check if dx1>d1, dx2>d1, dx3>d2, dx4>d2 -> []
    d1 = dis((x1, y1), (x2, y2))
    d2 = dis((x3, y3), (x4, y4))
    dx1 = dis((x, y), (x1, y1))
    dx2 = dis((x, y), (x2, y2))
    dx3 = dis((x, y), (x3, y3))
    dx4 = dis((x, y), (x4, y4))
    # print d1, d2
    # print dx1, dx2, dx3, dx4
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
    storeEdges()


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
    storeEdges()


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
    storeEdges()


def graph(line):

    # MAIN LOOP
    i = 0
    for current_key in edgeDic.keys():
        current_list = []
        for current_edge in edgeDic[current_key]:
            for compared_key in edgeDic.keys():
                if compared_key == current_key:
                    continue
                compared_list = edgeDic[compared_key][:]
                for compared_edge in edgeDic[compared_key]:
                    result = intersectCal(current_edge[0], current_edge[1], compared_edge[0], compared_edge[1])
                    if not result:  # if emtpy
                        continue
                    else:  # found new dots
                        entry11 = (result[0], result[4])
                        entry12 = (result[4], result[1])
                        entry21 = (result[2], result[4])
                        entry22 = (result[4], result[3])
                        if entry11[0] != entry11[1]:
                            current_list.append(entry11)
                        if entry12[0] != entry12[1]:
                            current_list.append(entry12)
                        compared_list.remove(compared_edge)
                        if entry21[0] != entry21[1]:
                            compared_list.append(entry21)
                        if entry22[0] != entry22[1]:
                            compared_list.append(entry22)
                edgeDic[compared_key] = compared_list
        edgeDic[current_key] = current_list
        i += 1

    # ELIMINATE DUPLICATION
    for key in edgeDic.keys():
        edgeDic[key] = list(dict.fromkeys(edgeDic[key]))

    # print 'Processed edge:', edgeDic
    # print 'Processed dots:', streetDic

    # EXTRACT VERTICES
    # store vertices for both easy for edge and vertex output
    vertex_dic = {}
    i = 1
    for key in edgeDic.keys():
        for edge in edgeDic[key]:
            if edge[0] not in pubPoints.values():
                while i in pubPoints.keys():
                    i += 1
                pubPoints[i] = edge[0]
                vertex_dic[edge[0]] = i
            else:  # store current dots and find its previous index
                for k, v in pubPoints.items():
                    # print 'trying to find:', v,  ' with ', edge[0]
                    if v == edge[0]:
                        vertex_dic[edge[0]] = k
            if edge[1] not in pubPoints.values():
                while i in pubPoints.keys():
                    i += 1
                pubPoints[i] = edge[1]
                vertex_dic[edge[1]] = i
            else:  # store current dots and find its previous index
                for k, v in pubPoints.items():
                    # print 'trying to find:', v, ' with ', edge[1]
                    if v == edge[1]:
                        vertex_dic[edge[1]] = k

    # OUTPUT
    print 'V = {'
    for key in vertex_dic:
        print ' ', vertex_dic[key], ': ', key
    print '}'
    print 'E = {'
    i = 0
    j = 0
    for key in edgeDic.keys():
        for edge in edgeDic[key]:
            if i != len(edgeDic.keys()) - 1 or j != len(edgeDic[key]) - 1:
                print ' <', vertex_dic[edge[0]], ',', vertex_dic[edge[1]], '>,'
            else:
                print ' <', vertex_dic[edge[0]], ',', vertex_dic[edge[1]], '>'
            j += 1
        i += 1
        j = 0
    print '}'
    # print vertex_dic
    # print pubPoints


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
            if len(l) != 2:
                return []
            cameras.append((float(l[0]), float(l[1])))
        else:
            # no '(' before actual content
            if not open_bracket:
                return []
            s += c
    # no ')' at end
    if open_bracket:
        return []
    return [cmd, street, cameras]


def masterCode():
    # sample code to read from stdin.
    # make sure to remove all spurious print statements as required
    # by the assignment
    while True:
        line = parseline(sys.stdin.readline())
        # print line
        if len(line) > 3 or len(line) == 0:
            print error_msg['format']
            continue
        cmd = line[0]
        if cmd in options:
            options[cmd](line)

        else:
            print error_msg['cmd']


def testCode():
    A = (2.0, 2.0)
    B = (4.0, 4.0)
    C = (4.0, 4.0)
    D = (5.0, 5.0)
    # storeIntoPubPoints(A, pubPoints)
    # storeIntoPubPoints(B, pubPoints)
    # storeIntoPubPoints(C, pubPoints)
    # storeIntoPubPoints(D, pubPoints)
    print intersectCal(A, B, C, D)
    # print storeIntoPubPoints(B, pubPoints)

def main():
    masterCode()
    # testCode()



if __name__ == '__main__':
    main()

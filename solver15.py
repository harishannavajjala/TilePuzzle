"""
Initial State:- is an 4*4 matrix (with distinct values from the range(0,16))
Goal State   :- [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]] . Goal state is pretty straight forward here.

successor function:- Any random state can have upto four successor states that generate from moves L,R,U,D. But if any of these newly
                        generated states are already visited previously then it would not be added to the fringe.

Cost function:-   Every newly generated state costs one unit cost i.e., one move.


Hueristic function:- Our heuristic function is a sum of g(s) and h(s). g(s) is the cost of reaching a state S and h(s) is the estimated
                    cost to the goal state. g(s) is 0 for initial state and is incrememented by 1 for next set of states and so on.
                    h(s) is the sum of Manhattan distance of all the tiles to their goal location.

"""

import sys
import copy

#This function appends newly generated states to the fringe
def appendToFringe(s_states,fringe):
    for state in s_states:
        fringe.append(state)

# This function checks if a given state is a goal state or not and returns a boolean value
def test_goal(current_state):
    if(current_state==[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]):
        return True

#This function gives the coordinates of the tile that is on the left side of tile 0
def findLeftTile(i,j):
    if(j==0):
        return (i,3)
    else:
        return (i,j-1)

#This function gives the coordinates of the tile that is on the right side of tile 0
def findRightTile(i,j):
    if(j==3):
        return (i,0)
    else:
        return (i,j+1)

#This function gives the coordinates of the tile that is on the top side of tile 0
def findTopTile(i,j):
    if(i==0):
        return  (3,j)
    else:
        return (i-1,j)

#This function gives the coordinates of the tile that is on the bottom side of tile 0
def findBottomTile(i,j):
    if(i==3):
        return (0,j)
    else:
        return (i+1,j)

#This function computes the manhattan distance of all the tiles to their respective goal locations
def findManhattanDist(i,j,locs):
    ig = locs[0]
    jg = locs[1]
    rowManh = abs(i-ig)
    colManh = abs(j - jg)

    if(rowManh == 3):
        rowManh = 1
    if (colManh == 3):
        colManh = 1

    return (rowManh+colManh)

#Computes the heuristic
def findHeuristic(current_state):
    locs = {1:[0,0],2:[0,1],3:[0,2],4:[0,3],5:[1,0],6:[1,1],7:[1,2],8:[1,3],9:[2,0],10:[2,1],11:[2,2],12:[2,3],13:[3,0],14:[3,1],15:[3,2],0:[3,3]}
    h =0
    for i in range(len(current_state)):
        for j in range(len(current_state)):
            h+=findManhattanDist(i,j,locs[current_state[i][j]])
    return h

#This function generates a new state
def generateNextState(current_state,i,j,index,g):
    global vsd
    next_state=copy.deepcopy(current_state)
    temp = next_state[i][j]
    next_state[i][j] = next_state[index[0]][index[1]]
    next_state[index[0]][index[1]] = temp
    if(next_state in vsd):
        return None
    h = findHeuristic(next_state)
    g +=1
    h = h + g
    return next_state,h,g

#This function generates and returns a new set of successor states for any given state
def successor(current_state,g,move):
    moves = {0:'L',1:'R',2:'U',3:'D'}
    flag = False
    s_states = []
    indexes = []

    #Identifies the position of 0 in the current_state
    for i in range(len(current_state)):
        if(0 in current_state[i]):
            for j in range(len(current_state[i])):
                if(current_state[i][j] == 0):
                    flag = True
                    break
            if flag:
                flag = False
                break

    #Figures out its adjacent tiles
    indexes.append(findRightTile(i, j))
    indexes.append(findLeftTile(i,j))
    indexes.append(findBottomTile(i, j))
    indexes.append(findTopTile(i,j))


    m = 0
    for index in indexes:
        ns = generateNextState(current_state,i,j,index,g)
        if ns != None:
            ns += (move + moves[m],)
            s_states.append(ns)
        m+=1
    return s_states

#This function selects a state from fringe which has least heuristic value
def findCurrentState(fringe):
    if(len(fringe)==1):
        x = fringe.pop(0)
        curr= x[0]
        g = x[2]
        move = x[3]
    else:
        minhue = fringe[0][1]
        curr = fringe[0][0]
        icurr = 0
        for i in range(1,len(fringe)):
            if(fringe[i][1]<minhue):
                minhue = fringe[i][1]
                icurr = i
        curr = fringe[icurr][0]
        g= fringe[icurr][2]
        move = fringe[icurr][3]
        fringe.pop(icurr)

    return curr,g,move

#Function to read input from the file
def read_initial_state():
    board = []
    file = open(sys.argv[1], "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        line = line.strip().split()
        if(len(line)>0):
            for l in range(len(line)):
                line[l] = int(line[l])
            board.append(line)

    return board

#This function checks if a given initial board is solvable or not.
def checkSolvability(initial_state):
    pi=0
    for i in range(len(initial_state)):
        if(0 in initial_state[i]):
            break
    row0 = i+1
    state = []
    for row in initial_state:
        state+=row

    for i in range(len(state)-1):
        for j in range(i+1,len(state)):
            if(state[i]!=0 and state[j]!=0 and state[i]>state[j]):
                pi+=1

    if(row0%2==0 and pi%2==0):
        return True
    elif(row0%2==1 and pi%2==1):
        return True
    else:
        return False



initial_state = read_initial_state()
cnt = 0
vsd = []
fringe = []
fringe.append((initial_state,0,0,''))
flag2 = False

flag = checkSolvability(initial_state)

if(flag):
    while len(fringe)>0:
        current_state,g,move = findCurrentState(fringe)
        vsd.append(current_state)
        if (test_goal(current_state)):
            print "Goal state found in",len(move),"moves"
            move = " ".join(list(move))
            print move
            flag2 = True
            break
        else:
            s_states=successor(current_state,g,move)
            appendToFringe(s_states,fringe)

    if(not flag2):
        print "No result"
if(not flag):
    print "NO RESULT"

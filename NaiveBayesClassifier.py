import sys
from collections import defaultdict
import copy
import operator
final = []
input_file = open("input.txt", "r")
output_file = open("output.txt", "w+")
line = input_file.readline()
player = defaultdict(list)
opponent = defaultdict(list)

#####################cost_matrix contains the initial weights of the 2d matrix
cost_matrix = []
cost_matrix.append([99,-8,8,6,6,8,-8,99])
cost_matrix.append([-8,-24,-4,-3,-3,-4,-24,-8])
cost_matrix.append([8,-4,7,4,4,7,-4,8])
cost_matrix.append([6,-3,4,0,0,4,-3,6])
cost_matrix.append(cost_matrix[3])
cost_matrix.append(cost_matrix[2])
cost_matrix.append(cost_matrix[1])
cost_matrix.append(cost_matrix[0])
# print cost_matrix

#####################player details stores the required details for all the following states for each player
class player_details(object):
    def __init__(self, player_to_move, cut_off_depth, current_board):
        self.player_to_move = player_to_move
        self.cut_off_depth = 0
        self.current_board = current_board
        self.player = player
        self.opponent = opponent
        self.children =[]
        self.utility_value = 0
        self.name = None
        self.parent = ""
        ######################-------------CHANGEEEEEEEE--------dicts store set of possible moves for each player
        self.player_black_next = defaultdict(list)
        self.player_white_next = defaultdict(list)
        # self.current_position_i
        # self.current_position_j
        self.result_black = self.player_black_next
        self.result_white = self.player_white_next
        self.pass_move_black = "no pass"
        self.pass_move_white = "no pass"
        self.location = ""
        self.list_letters = ['a','b','c','d','e','f','g','h']

    def get_player(self):
        return self.player_to_move

    def get_board(self):
        return self.current_board

    def get_depth(self):
        return self.cut_off_depth

    def print_object(self):
        print str("Player playing: "+str(self.player_to_move))
        print str("Current depth: " +str(self.cut_off_depth))
        print str("Player positions: "+ str(self.player))
        print str("Opponent positions: " + str (self.opponent))
        print str("Next available moves for player: "+str(self.player_black_next))
        print str("Next available moves for opponent: " + str(self.player_white_next))
        print str("Result of player a move for player: " + str(self.result_black))
        print str("Result of player a move for opponent: " + str(self.result_white))
        print str("Current board status: " + str(self.print_array()))
        print str("Passing??? " + str(self.name))
        print str("Parent: " + str(self.parent))

    def print_array(self):
        a = [['*','*','*','*','*','*','*','*'],['*','*','*','*','*','*','*','*'],['*','*','*','*','*','*','*','*'],['*','*','*','*','*','*','*','*'],['*','*','*','*','*','*','*','*'],['*','*','*','*','*','*','*','*'],['*','*','*','*','*','*','*','*'],['*','*','*','*','*','*','*','*']]
        if bool(self.player.keys()) == False and bool(self.opponent.keys()) == False:
            return
        for key_x in self.player.keys():
            a[key_x.i][key_x.j] = 'X'
        for key_o in self.opponent.keys():
            a[key_o.i][key_o.j] = 'O'
        # for list in a:
            # print list

    def calculate_utility(self):
        utility_value = 0
        if start_player[0] is 'X':
            for key_p in self.player.keys():
                utility_value += cost_matrix[key_p.i][key_p.j]
            for key_o in self.opponent.keys():
                utility_value -= cost_matrix[key_o.i][key_o.j]
        elif start_player[0] is 'O':
            for key_o1 in self.opponent.keys():
                utility_value += cost_matrix[key_o1.i][key_o1.j]
            for key_p1 in self.player.keys():
                utility_value -= cost_matrix[key_p1.i][key_p1.j]
        return utility_value

    def next_moves(self,current_player_dict,current_opponent_dict):
        object = copy.deepcopy(self)
        object.player_black_next = defaultdict(list)
        object.player_white_next = defaultdict(list)
        object.result_black = defaultdict(list)
        object.result_white = defaultdict(list)
        # depth = self.cut_off_depth
        # object.cut_off_depth = depth + 1
        # print "previous depth"
        # print depth
        # print "new depth"
        # print object.cut_off_depth
        # object.
        # if self.player_to_move in 'X':
        list_player = {}
        for key_player in current_player_dict.keys():
            list_player[position(key_player.i, key_player.j)] = 1
        # print "list player"
        # print list_player
        for key_player in current_player_dict.keys():
            current_i = key_player.i
            current_j = key_player.j
            temp_pos = position(current_i, current_j)
            list_opponent = {}
            flag = 0
            for key_opponent in current_opponent_dict.keys():
                list_opponent[position(key_opponent.i, key_opponent.j)] = 1
            # print "list opponent"
            # print list_opponent
            p = position(current_i - 1, current_j)
            while list_opponent.has_key(p):
                flag = 1
                p.set_i(p.get_i() - 1)
            if p.get_i()>= 0 and flag == 1:
                t = position(p.get_i(),p.get_j())
                if list_player.has_key(t) == 0:
                    object.player_black_next[temp_pos].append(position(p.get_i(), p.get_j()))
            p = position(current_i - 1, current_j - 1)
            while list_opponent.has_key(p):
                flag = 2
                p.set_i(p.get_i() - 1)
                p.set_j(p.get_j() - 1)
            if p.get_i() >= 0 and p.get_j() >= 0 and flag == 2:
                t = position(p.get_i(), p.get_j())
                if list_player.has_key(t) == 0:
                    object.player_black_next[temp_pos].append(position(p.get_i(), p.get_j()))
            p = position(current_i - 1, current_j + 1)
            while list_opponent.has_key(p):
                flag = 3
                p.set_i(p.get_i() - 1)
                p.set_j(p.get_j() + 1)
            if p.get_i() >= 0 and p.get_j() <= 7 and flag == 3:
                t = position(p.get_i(), p.get_j())
                if list_player.has_key(t) == 0:
                    object.player_black_next[temp_pos].append(position(p.get_i(), p.get_j()))
            p = position(current_i + 1, current_j)
            while list_opponent.has_key(p):
                flag = 4
                p.set_i(p.get_i() + 1)
            if p.get_i() <= 7 and flag == 4:
                t = position(p.get_i(), p.get_j())
                if list_player.has_key(t) == 0:
                    object.player_black_next[temp_pos].append(position(p.get_i(), p.get_j()))
            p = position(current_i + 1, current_j + 1)
            while list_opponent.has_key(p):
                flag = 5
                p.set_i(p.get_i() + 1)
                p.set_j(p.get_j() + 1)
            if p.get_i() <= 7 and p.get_j() <= 7 and flag == 5:
                t = position(p.get_i(), p.get_j())
                if list_player.has_key(t) == 0:
                    object.player_black_next[temp_pos].append(position(p.get_i(), p.get_j()))
            p = position(current_i + 1, current_j - 1)
            while list_opponent.has_key(p):
                flag = 6
                p.set_i(p.get_i() + 1)
                p.set_j(p.get_j() - 1)
            if p.get_i() <= 7 and p.get_j() >= 0 and flag == 6:
                t = position(p.get_i(), p.get_j())
                if list_player.has_key(t) == 0:
                    object.player_black_next[temp_pos].append(position(p.get_i(), p.get_j()))
            p = position(current_i, current_j + 1)
            while list_opponent.has_key(p):
                flag = 7
                p.set_j(p.get_j() + 1)
            if p.get_j() <= 7 and flag == 7:
                t = position(p.get_i(), p.get_j())
                if list_player.has_key(t) == 0:
                    object.player_black_next[temp_pos].append(position(p.get_i(), p.get_j()))
            p = position(current_i, current_j - 1)
            while list_opponent.has_key(p):
                flag = 8
                p.set_j(p.get_j() - 1)
            if p.get_j() >= 0 and flag == 8:
                t = position(p.get_i(), p.get_j())
                if list_player.has_key(t) == 0:
                    object.player_black_next[temp_pos].append(position(p.get_i(), p.get_j()))
        # print self.player_black_next
        # elif self.player_to_move in 'O':
        list_opponent = {}
        for key_opponent in current_opponent_dict.keys():
            list_opponent[position(key_opponent.i,key_opponent.j)] = 1
        # print "list opponent"
        # print list_opponent
        for key_opponent in current_opponent_dict.keys():
            current_i = key_opponent.i
            current_j = key_opponent.j
            temp_pos = position(current_i, current_j)
            list_player = {}
            flag = 0
            for key_player in current_player_dict.keys():
                list_player[position(key_player.i,key_player.j)] = 1
            p = position(current_i-1,current_j)
            while list_player.has_key(p):
                # print "1"
                flag = 1
                p.set_i(p.get_i()-1)
            if p.get_i() >= 0 and flag == 1:
                t = position(p.get_i(), p.get_j())
                if list_opponent.has_key(t) == 0:
                    object.player_white_next[temp_pos].append(position(p.get_i(),p.get_j()))
            p = position(current_i-1,current_j-1)
            while list_player.has_key(p):
                # print "2"
                flag = 2
                p.set_i(p.get_i()-1)
                p.set_j(p.get_j()-1)
            if p.get_i() >= 0 and p.get_j() >= 0and flag == 2:
                t = position(p.get_i(), p.get_j())
                if list_opponent.has_key(t) == 0:
                    object.player_white_next[temp_pos].append(position(p.get_i(),p.get_j()))
            p = position(current_i-1,current_j+1)
            while list_player.has_key(p):
                # print "3"
                flag = 3
                p.set_i(p.get_i()-1)
                p.set_j(p.get_j()+1)
            if p.get_i() >= 0 and p.get_j() <= 7 and flag == 3:
                t = position(p.get_i(), p.get_j())
                if list_opponent.has_key(t) == 0:
                # if list_opponent.get(p.get_i()) == None and list_opponent.get(p.get_j()) == None:
                    object.player_white_next[temp_pos].append(position(p.get_i(),p.get_j()))
            p = position(current_i + 1, current_j)
            while list_player.has_key(p):
                # print "4"
                flag = 4
                p.set_i(p.get_i() + 1)
            if p.get_i() <= 7 and flag == 4:
                t = position(p.get_i(), p.get_j())
                if list_opponent.has_key(t) == 0:
                # if list_opponent.get(p.get_i()) == None:
                    object.player_white_next[temp_pos].append(position(p.get_i(), p.get_j()))
            p = position(current_i + 1, current_j + 1)
            while list_player.has_key(p):
                # print "5"
                flag = 5
                p.set_i(p.get_i() + 1)
                p.set_j(p.get_j() + 1)
            if p.get_i() <= 7 and p.get_j() <= 7 and flag == 5:
                t = position(p.get_i(), p.get_j())
                if list_opponent.has_key(t) == 0:
                # if list_opponent.get(p.get_i()) == None and list_opponent.get(p.get_j()) == None:
                    object.player_white_next[temp_pos].append(position(p.get_i(), p.get_j()))
            p = position(current_i + 1, current_j - 1)
            while list_player.has_key(p):
                # print "6"
                flag = 6
                p.set_i(p.get_i() + 1)
                p.set_j(p.get_j() - 1)
            if p.get_i() <= 7 and p.get_j() >= 0 and flag == 6:
                t = position(p.get_i(), p.get_j())
                if list_opponent.has_key(t) == 0:
                # if list_opponent.get(p.get_i()) == None and list_opponent.get(p.get_j()) == None:
                    object.player_white_next[temp_pos].append(position(p.get_i(), p.get_j()))
            p = position(current_i, current_j + 1)
            while list_player.has_key(p):
                # print "7"
                flag = 7
                p.set_j(p.get_j()+1)
            if p.get_j() <= 7 and flag == 7:
                t = position(p.get_i(), p.get_j())
                if list_opponent.has_key(t) == 0:
                # if list_opponent.get(p.get_j()) == None:
                    object.player_white_next[temp_pos].append(position(p.get_i(), p.get_j()))
            p = position(current_i, current_j - 1)
            while list_player.has_key(p):
                # print "8"
                flag = 8
                p.set_j(p.get_j()-1)
            if p.get_j() >= 0 and flag == 8:
                t = position(p.get_i(), p.get_j())
                if list_opponent.has_key(t) == 0:
                # if list_opponent.get(p.get_j()) == None:
                    object.player_white_next[temp_pos].append(position(p.get_i(), p.get_j()))
        # print "\n\nafter next moves------ new object"
        # print object.print_object()
        if bool(object.player_black_next) == False:
            object.pass_move_black = "pass"
        if bool(object.player_white_next) == False:
            object.pass_move_white = "pass"
        return object

    ##### this function takes the i,j position and iterates through respective dict to find if the corresponding key is empty
    ##### if key empty then terminal state reached
    ###### NOTEEEEEEEEEEEE - the key in the dict is of type POSITION
    def check_terminal(self):
        if bool(self.children) == False:
            return True
        else:
            return False

    def result_of_move(self, key_move, each_move):
        # print "ENTEREDDDDDD RESULTTT------>"
        # print key_move
        # print each_move
        # print self.player_black_next
        # print self.player_white_next
        new_object = copy.deepcopy(self)
        if(self.player_to_move == 'X' and len(self.player_black_next)==0 and self.parent!="pass") :
            # print "ENTEREDDDDDDD PASS SECTION OF RESULT XXXXXX----->"
            new_object = copy.deepcopy(self)
            new_object.name = "pass"
            depth = self.cut_off_depth
            new_object.cut_off_depth = depth + 1
            new_object.parent = self.name
            # if self.player_to_move in 'X':
            new_object.player_to_move = 'O'
            new_object.location = "pass"
            # else:
            #     new_object.player_to_move = 'X'
        elif (self.player_to_move == 'O' and len(self.player_white_next)==0 and self.parent!="pass"):
            # print "ENTEREDDDDDDD PASS SECTION OF RESULT OOOOOOOO----->"
            new_object = copy.deepcopy(self)
            new_object.name = "pass"
            depth = self.cut_off_depth
            new_object.cut_off_depth = depth + 1
            new_object.parent = self.name
            new_object.location = "pass"
            # if self.player_to_move in 'X':
            new_object.player_to_move = 'X'
        elif key_move.i >= 0 and key_move.j >= 0 and each_move.i >= 0 and each_move.j >= 0:
            # print "entered modification part of result"
            if self.player_to_move in 'X':
                new_object = copy.deepcopy(self)
                ##################################### change cut off depth - 1 -------------------->
                new_object.player_to_move = 'O'
                depth = self.cut_off_depth
                new_object.cut_off_depth = depth + 1
                new_object.location = str(self.list_letters[each_move.j] + "" + str(each_move.get_i()+1))
                for value in new_object.result_black.itervalues():
                    try:
                        value.remove(each_move)
                    except ValueError:
                        pass
                new_object.player[each_move] = 1
                # print each_move
                if each_move.get_i() == key_move.get_i():
                    diffi = 0
                    diffj = key_move.j - each_move.j
                    # print str(str(diffi) + " i equal " + str(diffj))
                elif each_move.get_j() == key_move.get_j():
                    diffi = key_move.i - each_move.i
                    diffj = 0
                    # print str(str(diffi) + " j equal " + str(diffj))
                elif abs(each_move.i - key_move.i) == abs(each_move.j - key_move.j):
                    diffi = key_move.i - each_move.i
                    diffj = key_move.j - each_move.j

                while True:
                    # print position(each_move.i+diffi,each_move.j+diffj)
                    new_object.player[position(each_move.i + diffi, each_move.j + diffj)] = 1
                    new_object.opponent.pop(position(each_move.i + diffi, each_move.j + diffj), None)
                    new_object.player_black_next = defaultdict(list)
                    new_object.player_white_next = defaultdict(list)
                    new_object.result_white.pop(position(each_move.i + diffi, each_move.j + diffj), None)

                    if diffi > 0 and diffj == 0:
                        # print "going 1"
                        diffi -= 1
                    elif diffi < 0 and diffj == 0:
                        # print "going 2"
                        diffi += 1
                    elif diffi == 0 and diffj > 0:
                        # print "going 3"
                        diffj -= 1
                    elif diffi == 0 and diffj < 0:
                        # print "going 4"
                        diffj += 1
                    elif diffi > 0 and diffj > 0:
                        # print "going 5"
                        diffi -= 1
                        diffj -= 1
                    elif diffi > 0 and diffj < 0:
                        # print "going 6"
                        diffi -= 1
                        diffj += 1
                    elif diffi < 0 and diffj > 0:
                        # print "going 7"
                        diffi += 1
                        diffj -= 1
                    elif diffi < 0 and diffj < 0:
                        # print "going 8"
                        diffi += 1
                        diffj += 1
                    if diffi == 0 and diffj == 0:
                        break
            if self.player_to_move in 'O':
                new_object = copy.deepcopy(self)
                new_object.player_to_move = 'X'
                ##################################### change cut off depth - 1 -------------------->
                for value in new_object.result_white.itervalues():
                    try:
                        # print value
                        value.remove(each_move)
                    except ValueError:
                        pass
                new_object.opponent[each_move] = 1
                # print each_move
                if each_move.get_i() == key_move.get_i():
                    diffi = 0
                    diffj = key_move.j - each_move.j
                    # print str(str(diffi) + " i equal " + str(diffj))
                elif each_move.get_j() == key_move.get_j():
                    diffi = key_move.i - each_move.i
                    diffj = 0
                    # print str(str(diffi) + " j equal " + str(diffj))
                elif abs(each_move.get_i() - key_move.get_i()) == abs(each_move.get_j() - key_move.get_j()):
                    diffi = key_move.i - each_move.i
                    diffj = key_move.j - each_move.j

                while True:
                    # print position(each_move.i+diffi,each_move.j+diffj)
                    new_object.opponent[position(each_move.i + diffi, each_move.j + diffj)] = 1
                    new_object.player.pop(position(each_move.i + diffi, each_move.j + diffj), None)
                    new_object.player_white_next = defaultdict(list)
                    new_object.player_black_next = defaultdict(list)
                    new_object.result_black.pop(position(each_move.i + diffi, each_move.j + diffj), None)

                    if diffi > 0 and diffj == 0:
                        # print "going 1"
                        diffi -= 1
                    elif diffi < 0 and diffj == 0:
                        # print "going 2"
                        diffi += 1
                    elif diffi == 0 and diffj > 0:
                        # print "going 3"
                        diffj -= 1
                    elif diffi == 0 and diffj < 0:
                        # print "going 4"
                        diffj += 1
                    elif diffi > 0 and diffj > 0:
                        # print "going 5"
                        diffi -= 1
                        diffj -= 1
                    elif diffi > 0 and diffj < 0:
                        # print "going 6"
                        diffi -= 1
                        diffj += 1
                    elif diffi < 0 and diffj > 0:
                        # print "going 7"
                        diffi += 1
                        diffj -= 1
                    elif diffi < 0 and diffj < 0:
                        # print "going 8"
                        diffi += 1
                        diffj += 1
                    if diffi == 0 and diffj == 0:
                        break
        # print "print result_of move"
        # print new_object.print_object()
        return new_object
#######################class input state processess the initial inputs from the file
class input_state(object):
    def __init__(self, first_player, depth):
        self.first_player = first_player
        self.depth = depth

    def get_player(self):
        return self.first_player

    def get_depth(self):
        return self.depth
#####################class position is for getting the x,y value of the player on the given board
class position(object):
    def __init__(self,i,j):
        self.i = i
        self.j = j
    def get_i(self):
        return self.i
    def get_j(self):
        return self.j
    def set_i(self,i):
        self.i = i
    def set_j(self,j):
        self.j = j
    def __hash__(self):
        return hash((self.i, self.j))
    def __cmp__(self, other):
        if self.get_i() == other.get_i():
            return self.get_j() < other.get_j()
        return self.get_i() < other.get_i()
    def __lt__(self, other):
        return self.get_i() < other.get_i()
    def __repr__(self):
        return str(str(self.i) + " " + str(self.j))
    def __eq__(self, other):
        return self.i == other.get_i() and self.j == other.get_j()


###########################------------alpha beta pruning check functions---------------------->
###########################----------------result function not defined--------------->
###########################------------current state dont know what to pass and how to store in player details------------->
###########################----------------function alpha beta pruning not defined----------------->
###########################---------------------current state is object of the player_details class---------------->
def display(nodename,d,value,alpha,beta):
    if (alpha == (-sys.maxint - 1)):
        alphastr = str("-Infinity")
    else:
        alphastr = str(alpha)

    if (beta == sys.maxint):
        betastr = "Infinity"
    else:
        betastr = str(beta)
    if (value == sys.maxint):
        valuestr = "Infinity"
    elif (value == (-sys.maxint - 1)):
        valuestr = "-Infinity"
    else:
        valuestr = str(value)
    final.append("%s,%d,%s,%s,%s\n" % (nodename, d, valuestr, alphastr, betastr))


def sortpos(listofpos):
    xylist=[]
    for pos in listofpos:
        s=str(pos.i)+" "+str(pos.j)
        xylist.append(s)
    xylist.sort()
    sorted_list = []
    for xy in xylist:
        p = position(int(xy[0]),int(xy[2]))
        sorted_list.append(p)
    return sorted_list
def checkcutoff(state,cutoff_depth):
    if cutoff_depth<=state.cut_off_depth:
        return True
    else:
        return False

def evaluate(state):
    state.utility_value = state.calculate_utility()
    return state.utility_value

def print_value(v):
    if v == sys.maxint:
        return "inf"
    elif v == (-sys.maxint-1):
        return "-inf"
    else:
        return v

def max_value(current_state,alpha,beta):
    # print "INSIDE MAXXXXXXXXXXXXXX"
    flag = 2
    # state.print_object()
    # print str("current player " + str(current_state.player) + "current opponent " + str(current_state.opponent))
    current_state = current_state.next_moves(current_state.player, current_state.opponent)
    # print "new object after next moves"
    # current_state.print_object()
    if current_state.player_to_move == 'X':
        flag = 1
    else:
        flag = 0
    if flag == 1:
        for k, v in current_state.player_black_next.items():
            v = sortpos(v)
            current_state.player_black_next[k] = v
        # print operator.itemgetter(current_state.player_black_next.items())
        # data, key = data.get
        # for k in current_state.player_black_next:
        #     current_state.player_black_next[k].sort()
        # #print current_state.player_black_next
        # dict_gen = sorted(current_state.player_black_next.items(),key=lambda e:e[1][0])
        dict_gen = sorted(current_state.player_black_next.items(), key=operator.itemgetter(1))
        # current_state.player_black_next = dict_gen

    else:
        for k, v in current_state.player_black_next.items():
            v = sortpos(v)
            current_state.player_black_next[k] = v
        # for k in current_state.player_white_next:
        #     current_state.player_white_next[k].sort()
        # print current_state.player_white_next
        # dict_gen = sorted(current_state.player_white_next.items(), key=lambda e: e[1][0])
        dict_gen = sorted(current_state.player_black_next.items(), key=operator.itemgetter(1))
        # current_state.player_white_next = dict_gen
    # print
    # print dict_gen
    if (len(dict_gen) == 0 and current_state.parent == "pass"):
        current_state.children = []
    elif (len(dict_gen) == 0 and current_state.parent != "pass"):
        p = current_state.result_of_move(position(0, 0), position(0, 0))
        current_state.children.append(p)
        # print str("Current player after result of move: " + str(p.player))
    else:
        for each_action, each_move in dict_gen:
            each_move = sortpos(each_move)
            for each_position in each_move:
                # print each_position
                p1 = current_state.result_of_move(each_action, each_position)
                # p1.print_object()
                current_state.children.append(p1)
                # print current_state.result_of_move(each_action, each_position).print_object()
    if (checkcutoff(current_state, global_depth)):
        value = evaluate(current_state)
        if current_state.location == "":
            current_state.location = "root"
        # s = "%s,%d,%f,%f,%f\n" % (current_state.location, current_state.cut_off_depth, value, alpha, beta)
        # final.append(s)
        display(current_state.location, current_state.cut_off_depth, value, alpha, beta)
        # print("%s\t%d\t%f\t%f\t%f\n" % (current_state.location,current_state.cut_off_depth, value, alpha, beta))
        return value
    if(current_state.check_terminal()):
        value = current_state.calculate_utility()
        if current_state.location == "":
            current_state.location = "root"
        # s = "%s,%d,%f,%f,%f\n" % (current_state.location, current_state.cut_off_depth, value, alpha, beta)
        # final.append(s)
        display(current_state.location, current_state.cut_off_depth, value, alpha, beta)
        # print("%s\t%d\t%f\t%f\t%f\n" % (current_state.location,current_state.cut_off_depth, value, alpha, beta))
        return value
    v = sys.maxint

    for each_child in current_state.children:
        # print each_child.print_object()
        if current_state.location == "":
            current_state.location = "root"
        # s = "%s,%d,%f,%f,%f\n" % (current_state.location, current_state.cut_off_depth, v, alpha, beta)
        # final.append(s)
        display(current_state.location, current_state.cut_off_depth, v, alpha, beta)
        # print("%s\t%d\t%f\t%f\t%f\n" % (current_state.location,current_state.cut_off_depth, v, alpha, beta))
        v = max(v, min_value(each_child, alpha, beta))
        if v >= beta:
            current_state.utility_value = v
            if current_state.location == "":
                current_state.location = "root"
            # s = "%s,%d,%f,%f,%f\n" % (current_state.location, current_state.cut_off_depth, v, alpha, beta)
            # final.append(s)
            display(current_state.location, current_state.cut_off_depth, v, alpha, beta)
            return v
        alpha = max(alpha,v)
    current_state.utility_value = v
    if current_state.location == "":
        current_state.location = "root"
    # s = "%s,%d,%f,%f,%f\n" % (current_state.location, current_state.cut_off_depth, v, alpha, beta)
    # final.append(s)
    display(current_state.location, current_state.cut_off_depth, v, alpha, beta)
    return v

def min_value(current_state, alpha, beta):
    # print "INSIDE MINNNNNNNN"
    flag = 2
    # print str("current player " + str (current_state.player) + "current opponent " + str(current_state.opponent))
    current_state = current_state.next_moves(current_state.player, current_state.opponent)
    # current_state.print_object()
    if current_state.player_to_move == 'X':
        flag = 1
    else:
        flag = 0
    if flag == 1:
        for k, v in current_state.player_black_next.items():
            v = sortpos(v)
            current_state.player_black_next[k] = v
            # current_state.player_black_next[k].sort()
        # print current_state.player_black_next
        # dict_gen = sorted(current_state.player_black_next.items(), key=lambda e: e[1][0])
        dict_gen = sorted(current_state.player_black_next.iteritems(), key=operator.itemgetter(0))
        # current_state.player_black_next = dict_gen
    else:
        for k, v in current_state.player_black_next.items():
            v = sortpos(v)
            current_state.player_black_next[k] = v
        # for k in current_state.player_white_next:
        #     current_state.player_white_next[k].sort()
        # #print current_state.player_white_next
        # dict_gen = sorted(current_state.player_white_next.items(), key=lambda e:e[1][0])
        dict_gen = sorted(current_state.player_white_next.iteritems(), key=operator.itemgetter(1))
        # current_state.player_white_next = dict_gen
        # print dict(dict_gen) == current_state.player_black_next
    # print dict_gen
    if (len(dict_gen) == 0 and current_state.parent == "pass"):
        current_state.children = []
    elif (len(dict_gen) == 0 and current_state.parent != "pass"):
        current_state.children.append(current_state.result_of_move(position(0, 0), position(0, 0)))
    else:
        for each_action, each_move in dict_gen:
            each_move = sortpos(each_move)
            for each_position in each_move:
                # print each_position
                p1 = current_state.result_of_move(each_action, each_position)
                # p1.print_object()
                current_state.children.append(p1)

    if (checkcutoff(current_state, global_depth)):
        value = evaluate(current_state)
        if current_state.location == "":
            current_state.location = "root"
        # s = "%s,%d,%f,%f,%f\n" % (current_state.location, current_state.cut_off_depth, value, alpha, beta)
        # final.append(s)
        display(current_state.location, current_state.cut_off_depth, value, alpha, beta)
        return value
    if (current_state.check_terminal()):
        value = current_state.calculate_utility()
        if current_state.location == "":
            current_state.location = "root"
        # s = "%s,%d,%f,%f,%f\n" % (current_state.location, current_state.cut_off_depth, value, alpha, beta)
        # final.append(s)
        display(current_state.location, current_state.cut_off_depth, value, alpha, beta)
        return value
    v = -sys.maxint - 1
    for each_child in current_state.children:
        # print "children generated"
        # print each_child.print_object()
        if current_state.location == "":
            current_state.location = "root"
        # s = "%s,%d,%f,%f,%f\n" % (current_state.location, current_state.cut_off_depth, v, alpha, beta)
        # final.append(s)
        display(current_state.location, current_state.cut_off_depth, v, alpha, beta)
        v = min(v, max_value(each_child, alpha, beta))
        if v <= alpha:
            current_state.utility_value = v
            # s = "%s,%d,%f,%f,%f\n" % (current_state.location, current_state.cut_off_depth, v, alpha, beta)
            # final.append(s)
            display(current_state.location, current_state.cut_off_depth, v, alpha, beta)
            return v
        beta = min(beta, v)
    current_state.utility_value = v
    if current_state.location == "":
        current_state.location = "root"
    # s = "%s,%d,%f,%f,%f\n" % (current_state.location, current_state.cut_off_depth,v, alpha, beta)
    display(current_state.location, current_state.cut_off_depth, v, alpha, beta)
    return v
start = input_state(line, input_file.readline())
global_depth = start.get_depth()
global_depth = int(global_depth[0])
current_board = defaultdict(list)
start_player = start.get_player()
player_1 = player_details(start_player[0],0,current_board)
first_line = input_file.readline()
count = -1
while first_line:
    count += 1
    j = 0
    for i in first_line:
        if i in 'X':
            pos_object = position(count, j)
            player[pos_object] = 1
        elif i in 'O':
            pos_object = position(count, j)
            opponent[pos_object] = 1
        j += 1
    first_line = input_file.readline()

val = max_value(player_1,-sys.maxint-1,sys.maxint)
for child in player_1.children:
    if val == child.utility_value:
        output_file.write(child.print_array)
output_file.write('\nNode,Depth,Value,Alpha,Beta\n')
for line in final:
    output_file.write(line)
output_file.close
# print "returned value to main call"
# print val

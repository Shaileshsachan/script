import re
import sys
from pprint import pprint

arguments = sys.argv[1:]
r_list = []
i_list = []
my_dict = {}
router_list = []


def start(arguments):
    for i in arguments:
        with open(i, 'r') as f:
            line = f.readlines()
        last_line = (len(line))

    for line_no, itr in enumerate(line):
        if re.search('Logged', itr):
            r_list.append(line_no)
    r_list.append(last_line)
    get_intf_data(r_list, list(line))
    return r_list


def get_intf_data(r_list, line):  # handling Index out of range error
    for i in range(len(r_list)):
        if i == len(r_list) - 1:
            break
        else:
            l1 = line[r_list[i]:r_list[i+1]]
            l2 = handle(l1)
            router_list.append(l2)
    pprint(router_list)

def handle(l1):
    for i,j in enumerate(l1):
        if re.search('Logged', j):
            my_dict['Router'] = j.split()[2]
        if re.search('Physical', j):
            if i == [x for x in i_list]:
                print(i_list.append(i))
            my_dict['Interface'] = j.split()[2][:-1]
        if re.search('Carrier', j):
            my_dict['Drop'], my_dict['Error'] = ((j.split(',')[2]).split(':')[1]).strip(), ((j.split(',')[6]).split(':')[1]).strip()
    return my_dict


start(arguments)
import re
import sys
from pprint import pprint

arguments = sys.argv[1:]

Router = []
router_line = []
Interface = []
interface_line = []


def find_router(line):
    for i in range(len(line)):
        if re.findall('Logged', line[i]):
            router_name = line[i].split(' ')[2]
            Router.append(router_name[:-1])
            router_line.append(i)
        else:
            pass
    Router1 = find_interface(router_line[0], router_line[1], line, flag=0)

    Router2 = find_interface(router_line[1], len(line), line, flag=1)
    return Router1, Router2


def find_interface(start, end, line, flag):
    for count, i in enumerate(line):
        if start <= count < end:
            if re.findall('Physical', line[count]):
                interface_name = line[count].split(' ')[2]
                Interface.append(interface_name[:-1])
                interface_line.append(count)
            else:
                pass
    Drop_1, Error_1 = find_drop_error(interface_line[0], interface_line[1], line)
    if flag == 1:
        Drop_2, Error_2 = find_drop_error(interface_line[1], len(line), line)
    elif flag == 0:
        Drop_2, Error_2 = find_drop_error(interface_line[1], router_line[1], line)

    interface_line.clear()
    return Interface, Drop_1, Error_1, Drop_2, Error_2


def find_drop_error(start, end, line):
    global Drop, Error

    for count, i in enumerate(line):
        if start <= count < end:
            if re.findall('Carrier', line[count]):
                Drop, Error = ((line[count].split(',')[2]).strip()).split(':'), (line[count].split(',')[6]).split(':')
    return Drop[1].strip(), Error[1].strip()


def start(arguments):
    for count, file in enumerate(arguments):
        with open(file, 'r') as f:
            line = f.readlines()
            R1, R2 = find_router(line)
        if count == 0:
            R1_I1 = (Router[0], R1[0][0], R1[1], R1[2])
            R1_I2 = (Router[0], R1[0][1], R1[3], R1[4])
            R2_I1 = (Router[1], R2[0][2], R2[1], R2[2])
            R2_I2 = (Router[1], R2[0][3], R2[3], R2[4])
        elif count == 1:
            R11_I1 = (Router[2], R1[0][4], R1[1], R1[2])
            R11_I2 = (Router[2], R1[0][5], R1[3], R1[4])
            R21_I1 = (Router[3], R2[0][6], R2[1], R2[2])
            R21_I2 = (Router[3], R2[0][7], R2[3], R2[4])
    return [R1_I1, R1_I2, R2_I1, R2_I2], [R11_I1, R11_I2, R21_I1, R21_I2]


def difference():
    result1, result2 = start(arguments)      #result1 is list1 and result2 is list2
    for i,j in zip(result1, result2):
        drop_diff, erro_diff = (int(j[2])-int(i[2]), int(j[3])-int(i[3]))
        if drop_diff and erro_diff > 100:
            # print(i[0], j[0], i[1], j[1])
            print(i[0], i[1])                # Only printing Router, Interface from list1 because both are same
    # pprint(result1)
    # pprint(result2)

difference()
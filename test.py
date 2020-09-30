import os
import random
from Graph.timetable import timetable
from GLPK.genmod import genmod

def gencase(teachers, courses, rooms):
    e1 = list()
    e2 = list()

    e_check = list()

    for i in range(teachers - 1):
        c = random.randint(1, courses)
        index = random.randint(1, courses - c + 1)
        for j in range(1, c + 1):
            if index not in e_check:
                e_check.append(index)
            e1.append(('T' + str(i + 1), 'C' + str(index)))
            index = random.randint(index + 1, courses - (c - j) + 1)
    for i in range(1, courses + 1):
        if i not in e_check:
            e1.append(('T' + str(teachers), 'C' + str(i)))

    e_check = list()

    for i in range(rooms - 1):
        c = random.randint(1, courses)
        index = random.randint(1, courses - c + 1)
        for j in range(1, c + 1):
            if index not in e_check:
                e_check.append(index)
            e2.append(('R' + str(i + 1), 'C' + str(index)))
            index = random.randint(index + 1, courses - (c - j) + 1)
    for i in range(1, courses + 1):
        if i not in e_check:
            e2.append(('R' + str(rooms), 'C' + str(i)))

    ce1 = dict()
    for (t, c) in e1:
        st = int(t[1:]) - 1
        if st not in ce1:
            ce1[st] = [int(c[1:]) - 1]
        else:
            ce1[st].append(int(c[1:]) - 1)
    for i in range(teachers):
        if i not in ce1:
            ce1[i] = list()
    exce1 = dict()
    for i in ce1:
        exce1[i] = list()
        for j in range(courses):
            if j not in ce1[i]:
                exce1[i].append(j)

    ce2 = dict()
    for (r, c) in e2:
        sr = int(r[1:]) - 1
        if sr not in ce2:
            ce2[sr] = [int(c[1:]) - 1]
        else:
            ce2[sr].append(int(c[1:]) - 1)
    for i in range(rooms):
        if i not in ce2:
            ce2[i] = list()
    exce2 = dict()
    for i in ce2:
        exce2[i] = list()
        for j in range(courses):
            if j not in ce2[i]:
                exce2[i].append(j)

    return [e1, e2, exce1, exce2]

def count_timeslot(filename):
    f = open(filename, 'r')
    lines = f.readlines()

    largest_timeslot = 0
    for line in lines:
        c = line.split(' ')
        if len(c) == 5 and c[0] == 'result:':
            current_timeslot = int(c[4][5:].strip())
            if current_timeslot > largest_timeslot:
                largest_timeslot = current_timeslot
    
    f.close()

    f = open(filename, 'a')
    f.write('\nTimeslot used: ' + str(largest_timeslot + 1) + '\n')
    f.close()

if __name__ == "__main__":
    # Test case 1: 12 teachers, 40 courses, 30 rooms
    [e1, e2, exce1, exce2] = gencase(12, 40, 30)
    timeslots = timetable(e1, e2, 'graph_result1.txt')
    genmod(12, 40, 30, timeslots, exce1, exce2, 'gen1.mod')
    os.system('glpsol --model gen1.mod > glpk_result1.txt')
    count_timeslot('glpk_result1.txt')

    # Test case 2: 5 teachers, 12 courses, 3 rooms
    [e1, e2, exce1, exce2] = gencase(5, 12, 3)
    timeslots = timetable(e1, e2, 'graph_result2.txt')
    genmod(5, 12, 3, timeslots, exce1, exce2, 'gen2.mod')
    os.system('glpsol --model gen2.mod > glpk_result2.txt')
    count_timeslot('glpk_result2.txt')

    # Test case 3: 20 teachers, 50 courses, 60 rooms
    [e1, e2, exce1, exce2] = gencase(20, 50, 60)
    timeslots = timetable(e1, e2, 'graph_result3.txt')
    genmod(20, 50, 60, timeslots, exce1, exce2, 'gen3.mod')
    os.system('glpsol --model gen3.mod > glpk_result3.txt')
    count_timeslot('glpk_result3.txt')

    # Test case 4: 16 teachers, 60 courses, 48 rooms
    [e1, e2, exce1, exce2] = gencase(16, 60, 48)
    timeslots = timetable(e1, e2, 'graph_result4.txt')
    genmod(16, 60, 48, timeslots, exce1, exce2, 'gen4.mod')
    os.system('glpsol --model gen4.mod > glpk_result4.txt')
    count_timeslot('glpk_result4.txt')

    # Test case 5: 30 teachers, 90 courses, 48 rooms
    [e1, e2, exce1, exce2] = gencase(30, 90, 48)
    timeslots = timetable(e1, e2, 'graph_result5.txt')
    genmod(30, 90, 48, timeslots, exce1, exce2, 'gen5.mod')
    os.system('glpsol --model gen5.mod > glpk_result5.txt')
    count_timeslot('glpk_result5.txt')
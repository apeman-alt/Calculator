import math

def deg_to_rad(angle):
    #convert from degrees to radians
    angle /= 180
    angle *= math.pi
    return angle

def rad_to_deg(angle):
    #convert from radians to degrees
    angle /= math.pi
    angle *= 180
    return angle

def exponents(equation):
    equation3 = equation

    #remove unecessary operators
    for i in range(len(equation3)):
        if equation3[i] == '+' or equation3[i] == '-' or equation3[i] == '*' or equation3[i] == '/':
            equation3 = equation3.replace(equation3[i], ' ', 1)
    list = []
    list = equation3.split()

    #gather all expressions involving exponents ('^')
    list2 = []
    for i in list:
        if '^' in i: list2.append(i)
    #evaluate exponential expressions
    list3 = list2[:]
    answer = 1
    for i in range(len(list3)):
        list3[i] = list3[i].split('^')
        for j in range(len(list3[i])-1, -1, -1):
            answer = float(list3[i][j]) ** answer
        #replace exponential expression with answer
        equation = equation.replace(str(list2[i]), str(answer), 1)
        answer = 1

    return equation

def sin(equation, in_radian_mode):
    equation3 = equation

    #remove unecessary operators
    for i in range(len(equation3)):
        if equation3[i] == '+' or equation3[i] == '*' or equation3[i] == '/':
            equation3 = equation3.replace(equation3[i], ' ', 1)
    for i in range(1, len(equation3)):
        if equation[i] == '-':
            if i >= 1:
                if equation[i-1] != 'n':
                    equation3 = equation3.replace(equation3[i], ' ', 1)

    list = []
    list = equation3.split()

    list2 = []
    for i in list:
        if 'sin' in i: list2.append(i)

    list3=list2[:]
    for i in range(len(list3)):
        list3[i] = list3[i].replace('sin', '')

        #convert from degrees to radians if necessary
        if not in_radian_mode:
            angle = deg_to_rad(float(list3[i]))
        else:
            angle = float(list3[i])

        answer = math.sin(angle)
        equation = equation.replace('sin'+list3[i], str(answer))
    return equation

def cos(equation, in_radian_mode):
    equation3 = equation

    #remove unecessary operators
    for i in range(len(equation3)):
        if equation3[i] == '+' or equation3[i] == '*' or equation3[i] == '/':
            equation3 = equation3.replace(equation3[i], ' ', 1)
    for i in range(1, len(equation3)):
        if equation[i] == '-':
            if i >= 1:
                if equation[i-1] != 's':
                    equation3 = equation3.replace(equation3[i], ' ', 1)

    list = []
    list = equation3.split()

    list2 = []
    for i in list:
        if 'cos' in i: list2.append(i)

    list3=list2[:]
    for i in range(len(list3)):
        list3[i] = list3[i].replace('cos', '')

        #convert from degrees to radians if necessary
        if not in_radian_mode:
            angle = deg_to_rad(float(list3[i]))
        else:
            angle = float(list3[i])

        answer = math.cos(angle)
        equation = equation.replace('cos'+list3[i], str(answer))
    return equation

def tan(equation, in_radian_mode):
    equation3 = equation

    #remove unecessary operators
    for i in range(len(equation3)):
        if equation3[i] == '+' or equation3[i] == '*' or equation3[i] == '/':
            equation3 = equation3.replace(equation3[i], ' ', 1)
    for i in range(1, len(equation3)):
        if equation[i] == '-':
            if i >= 1:
                if equation[i-1] != 'n':
                    equation3 = equation3.replace(equation3[i], ' ', 1)

    list = []
    list = equation3.split()

    list2 = []
    for i in list:
        if 'tan' in i: list2.append(i)

    list3=list2[:]
    for i in range(len(list3)):
        list3[i] = list3[i].replace('tan', '')

        #convert from degrees to radians if necessary
        if not in_radian_mode:
            angle = deg_to_rad(float(list3[i]))
        else:
            angle = float(list3[i])

        try:
            answer = math.tan(angle)
        except:
            return 'Undefined'

        equation = equation.replace('tan'+list3[i], str(answer))
    return equation

def asin(equation, in_radian_mode):
    equation3 = equation

    #remove unecessary operators
    for i in range(len(equation3)):
        if equation3[i] == '+' or equation3[i] == '*' or equation3[i] == '/':
            equation3 = equation3.replace(equation3[i], ' ', 1)
    for i in range(1, len(equation3)):
        if equation[i] == '-':
            if i >= 1:
                if equation[i-1] != 'n':
                    equation3 = equation3.replace(equation3[i], ' ', 1)

    list = []
    list = equation3.split()

    list2 = []
    for i in list:
        if 'arcsin' in i: list2.append(i)

    list3=list2[:]
    for i in range(len(list3)):
        list3[i] = list3[i].replace('arcsin', '')
        answer = math.asin(float(list3[i]))

        #convert from radians to degrees if necessary
        if not in_radian_mode:
            answer = rad_to_deg(answer)

        equation = equation.replace('arcsin'+list3[i], str(answer))
    return equation


def acos(equation, in_radian_mode):
    equation3 = equation

    #remove unecessary operators
    for i in range(len(equation3)):
        if equation3[i] == '+' or equation3[i] == '*' or equation3[i] == '/':
            equation3 = equation3.replace(equation3[i], ' ', 1)
    for i in range(1, len(equation3)):
        if equation[i] == '-':
            if i >= 1:
                if equation[i-1] != 's':
                    equation3 = equation3.replace(equation3[i], ' ', 1)

    list = []
    list = equation3.split()

    list2 = []
    for i in list:
        if 'arccos' in i: list2.append(i)

    list3=list2[:]
    for i in range(len(list3)):
        list3[i] = list3[i].replace('arccos', '')
        answer = math.acos(float(list3[i]))

        #convert from radians to degrees if necessary
        if not in_radian_mode:
            answer = rad_to_deg(answer)

        equation = equation.replace('arccos'+list3[i], str(answer))
    return equation


def atan(equation, in_radian_mode):
    equation3 = equation

    #remove unecessary operators
    for i in range(len(equation3)):
        if equation3[i] == '+' or equation3[i] == '*' or equation3[i] == '/':
            equation3 = equation3.replace(equation3[i], ' ', 1)
    for i in range(1, len(equation3)):
        if equation[i] == '-':
            if i >= 1:
                if equation[i-1] != 'n':
                    equation3 = equation3.replace(equation3[i], ' ', 1)

    list = []
    list = equation3.split()

    list2 = []
    for i in list:
        if 'arctan' in i: list2.append(i)

    list3=list2[:]
    for i in range(len(list3)):
        list3[i] = list3[i].replace('arctan', '')
        answer = math.atan(float(list3[i]))

        #convert from radians to degrees if necessary
        if not in_radian_mode:
            answer = rad_to_deg(answer)

        equation = equation.replace('arctan'+list3[i], str(answer))
    return equation


def sqrt(equation):
    equation3 = equation

    #remove unecessary operators
    for i in range(len(equation3)):
        if equation3[i] == '+' or equation3[i] == '*' or equation3[i] == '/':
            equation3 = equation3.replace(equation3[i], ' ', 1)
    for i in range(1, len(equation3)):
        if equation[i] == '-':
            if i >= 1:
                if equation[i-1] != 't':
                    equation3 = equation3.replace(equation3[i], ' ', 1)

    list = []
    list = equation3.split()

    list2 = []
    for i in list:
        if 'sqrt' in i: list2.append(i)

    list3=list2[:]
    for i in range(len(list3)):
        list3[i] = list3[i].replace('sqrt', '')
        if float(list3[i]) < 0: return 'Undefined'
        answer = math.sqrt(float(list3[i]))
        equation = equation.replace('sqrt'+list3[i], str(answer))
    return equation

def ln(equation):
    equation3 = equation

    #remove unecessary operators
    for i in range(len(equation3)):
        if equation3[i] == '+' or equation3[i] == '*' or equation3[i] == '/':
            equation3 = equation3.replace(equation3[i], ' ', 1)
    for i in range(1, len(equation3)):
        if equation[i] == '-':
            if i >= 1:
                if equation[i-1] != 'n':
                    equation3 = equation3.replace(equation3[i], ' ', 1)

    list = []
    list = equation3.split()

    list2 = []
    for i in list:
        if 'ln' in i: list2.append(i)

    list3=list2[:]
    for i in range(len(list3)):
        list3[i] = list3[i].replace('ln', '')
        if float(list3[i]) <= 0: return 'Undefined'
        answer = math.log(float(list3[i]))
        equation = equation.replace('ln'+list3[i], str(answer))
    return equation


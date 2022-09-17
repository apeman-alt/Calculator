import math

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

def sin(equation):
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
        answer = math.sin(float(list3[i]))
        equation = equation.replace('sin'+list3[i], str(answer))
    return equation

def cos(equation):
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
        answer = math.cos(float(list3[i]))
        equation = equation.replace('cos'+list3[i], str(answer))
    return equation

def tan(equation):
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
        if float(list3[i])%(math.pi/2) == 0: return 'Undefined'
        answer = math.tan(float(list3[i]))
        equation = equation.replace('tan'+list3[i], str(answer))
    return equation


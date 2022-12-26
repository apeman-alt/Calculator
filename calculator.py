#VERSION: 1.11.2

#Josh Muszka
#May 22, 2022
#Last updated: December 26, 2022
#Calculator -- use it to solve arithmetic
#can perform any basic arithmetic operation on any rational value

#TODO: add order of operations
#TODO: when backspacing "sin(", "cos(", "sqrt(", etc., backspace the whole term instead of making user backspace each individual character
#BUG: exponent to the power of a function not parsing exponent properly ie. 3^ln(6) doesnt work
#BUG: evaluating really small inputs for ln ie. ln(0.000000001) crashes the program
#TODO: add keyboard input
#TODO: implicit multiplication
#TODO: get pi, e to remain as constants until calculation
#BUG: sin(pi), tan(pi) are undefined
#BUG: -1 doesnt work as input for functions (but 0-1 does)

import pygame, sys, time, math
import functions as f

####################################################################
                            #SETUP
####################################################################

#PYGAME CONFIG
pygame.init()
pygame.font.init()
btn_font = pygame.font.SysFont('Arial', 33)
display_font = pygame.font.SysFont('Arial', 40)
pygame.display.set_caption("Calculator")

#DISPLAY INFO
width, height = 360, 552
size = width, height
screen = pygame.display.set_mode(size)
FPS = 144
background_color = 0xFF, 0xE5, 0xAB 
line_color = 0x6E, 0x1D, 0x1D
btn_hovering_color = 0xFA, 0xE0, 0x96
btn_down_color = 0xCA, 0xB0, 0x66

#BUTTON SETUP
WIDTH = 5
HEIGHT = 6
board=[]
row = ('INV', 'RAD', 'π', 'e', '!')
board.append(row)
row = ['^','sin','cos','tan','AC']
board.append(row)
row = ('√',1,2,3,"+")
board.append(row)
row = ('(',4,5,6,"-")
board.append(row)
row = (')',7,8,9,"*")
board.append(row)
row = ('ln',".",0,"=","/")
board.append(row)

#print(board[1])

#CALCULATOR VARIABLES
display = '' #what gets displayed on calculator "screen"
equation = '' #the sequence of numbers and operators the user enters to be calculated
SYNTAX_ERROR = 'Syntax error'
UNDEFINED = 'Undefined'
in_inverse_mode = False #to toggle between inverse and normal trig functions
in_radian_mode = True #to toggle between radian and degree measurements


####################################################################
                        #CALCULATION CODE
####################################################################

#check for valid brackets
def bracket_check(equation):

    #count # of open and close brackets
    open_count = 0
    close_count = 0

    for i in range(len(equation)):
        if equation[i] == '(': open_count+=1
        if equation[i] == ')': close_count+=1

    if open_count == close_count: #if there's the same number of open and closed brackets
        open_count = 0
        close_count = 0

        #if the number of closed brackets ever exceeds the number of open brackets, then the bracket sequence must be invalid
        for i in range(len(equation)):
            if equation[i] == '(': open_count += 1
            elif equation[i] == ')': close_count += 1

            if close_count > open_count: 
                return False

    else: return False

    return True

def simplify_brackets(equation):
    index_list = []
    for i in range(len(equation)-1):
        if equation[i] == ')':
            if  equation[i+1] == '(':
                substr1 =  equation[0:i+1]
                substr2 = equation[i+1:]
                #equation = substr1 + '*' + substr2
                index_list.append(i+1)
            elif equation[i+1].isdigit():
                substr1 =  equation[0:i+1]
                substr2 = equation[i+1:]
                #equation = substr1 + '*' + substr2
                index_list.append(i+1)
        elif equation[i].isdigit():
            if equation[i+1] == '(':
                substr1 =  equation[0:i+1]
                substr2 = equation[i+1:]
                #equation = substr1 + '*' + substr2
                index_list.append(i+1)

    for i in range(len(index_list)-1, -1, -1):
        index = index_list[i]
        substr1 = equation[0:index]
        substr2 = equation[index:]
        equation = substr1 + '*' + substr2

    return equation

#main calculation code
def evaluate_expression(equation):
    #parse numlist
    #parse oplist
    #answer = numlist[0]
    #loop to get answer

    if equation[0] == '(' and equation[len(equation)-1]:
        equation = equation.replace(equation[0], '')
        equation = equation.replace(equation[len(equation)-1], '')

    #evaluate transcendental expressions
    equation = f.exponents(equation) #exponents
    equation = f.asin(equation, in_radian_mode) #sine inverse
    equation = f.acos(equation, in_radian_mode) #cosine inverse
    equation = f.atan(equation, in_radian_mode) #tangent inverse
    equation = f.sin(equation, in_radian_mode) #sine
    equation = f.cos(equation, in_radian_mode) #cosine
    equation = f.tan(equation, in_radian_mode) #tangent
    equation = f.sqrt(equation) #square root
    equation = f.ln(equation) #natural logarithm

    #NEW POTENTIALLY BROKEN CODE#
    op_list = []
    num_list = []
    equation2 = equation

    #generate num_list
    for i in range(len(equation2)):
        if equation2[i] == '+' or equation2[i] == '-' or equation2[i] == '*' or equation2[i] == '/':
            equation2 = equation2.replace(equation2[i], ' ', 1)
    num_list = equation2.split()

   #generate op_list
    for i in range(len(equation)):
        if equation[i].isdigit() or equation[i] == '.': equation = equation.replace(equation[i], ' ', 1)
    op_list = equation.split()

    #account for negative numbers
    for i in range(len(op_list)):
        if len(op_list[i]) == 2:
            if op_list[i] == '+-' or op_list[i] == '-+': 
                op_list[i] = '-'

            elif op_list[i] == '*-':
                op_list[i] = '*'
                num_list[i+1] = '-' + num_list[i+1]

            elif op_list[i] == '/-':
                op_list[i] = '/'
                num_list[i+1] = '-' + num_list[i+1]

            elif op_list[i] == '--':
                op_list[i] = '+'

            elif op_list[i] == '++':
                op_list[i] = '+'

            elif op_list[i] == '*+':
                op_list[i] = '*'

            elif op_list[i] == '/+':
                op_list[i] = '/'

            else: return SYNTAX_ERROR
        if len(op_list[i]) > 2: return SYNTAX_ERROR

    #check if all numbers are valid
    for i in range(len(num_list)):
        try: float(num_list[i])
        except: return SYNTAX_ERROR

    #check if num_list = op_list + 1
    #(check if user typed in a full equation, and not something such as: 6+9-3*)
    if len(num_list) != len(op_list)+1: return SYNTAX_ERROR

    answer = float(num_list[0])
    for i in range(len(op_list)):
        if op_list[i] == '+': answer += float(num_list[i+1])
        elif op_list[i] == '-': answer -= float(num_list[i+1])
        elif op_list[i] == '*': answer *= float(num_list[i+1])
        elif op_list[i] == '/': 
            try: 
                answer /= float(num_list[i+1])
            except ZeroDivisionError:
                return UNDEFINED

    answer = round_num(answer)
    return answer

def calculate(equation):

    if equation[0] == '-': equation = '0' + equation
    elif equation[0] == '+': equation = '0' + equation
    elif equation[0] == '*' or equation[0] == '/' or equation[0] == '^': return SYNTAX_ERROR
    elif equation[0] == '.': equation = '0+0' + equation
    else: equation = '0+' + equation

    equation = '(' + equation + ')'

    #check if brackets are valid
    if not bracket_check(equation): 
        return SYNTAX_ERROR

    #simplify brackets
    equation = simplify_brackets(equation)

    #count number of bracket pairs
    n=0
    for i in range(len(equation)):
        if equation[i] == '(':
            n+=1
    #evaluate each bracket pair
    substr1 = ''
    substr2 = ''
    while n > 0:
        for i in range(len(equation)-1, -1, -1):
            if equation[i] == '(':
                for j in range(i, len(equation)):
                    if equation[j] == ')':
                        substr1 = equation[i:j+1]
                        substr2 = str(evaluate_expression(substr1))
                        break
                break

        eq_fragments = equation.split(substr1,1)

        if len(eq_fragments) == 1:
            equation = eq_fragments[0] + substr2
        else:
            equation = eq_fragments[0] + substr2 + eq_fragments[1]
        n-=1 

        print(equation)
    
    #answer = evaluate_expression(equation)
    answer = equation
    return answer

#rounding final answer
def round_num(num):

    #round number to 7 decimal places, unless that makes the number 0 
    if abs(num) > 0.0000001:
        num = round(num, 7)

    #remove unecessary zeroes from end of number:

    num = str(num)
    length = len(num)

    while num[length-1] == '0': #while the last digit of the number is 0
        num = num[:(length-1)]
        length = len(num)

    if num[length-1] == '.': num = num[:(length-1)] #remove uncessecary decimal place

    return num
    

#when user clicks a button
def button_click(x,y):
    global display
    global equation
    global in_inverse_mode
    global in_radian_mode

    if int(y) > 120:
        #convert x,y positions to positions on grid
        x = int((x/width)*WIDTH)
        y = int(((y-120)/(height-120))*HEIGHT)

        input = str(board[y][x])

        #if user clicks a number, 
        if input.isdigit():
            equation += input
            display = equation

        #if user clicks ., +, -, *, or /
        if input == '.' or input == '+' or input == '-' or input == '*' or input == '/':
            equation += input
            display = equation

        #if user clicks AC
        if input == 'AC':
            equation = ''
            display = equation

        #if user clicks ( or )
        if input == '(' or input == ')':
            equation += input
            display = equation

        #if user clicks sin, cos, tan, or ln
        if input == 'sin' or input == 'cos' or input == 'tan' or input == 'ln':
            equation += input + '('
            display = equation

        #if user clicks sin-1
        if input == 'sin-1':
            equation += 'arcsin('
            display = equation

        #if user clicks cos-1
        if input == 'cos-1':
           equation += 'arccos('
           display = equation

        #if user clicks tan-1
        if input == 'tan-1':
            equation += 'arctan('
            display = equation

        #if user clicks ^
        if input == '^':
            equation += input
            display = equation

        #if user clicks √
        if input == '√':
            equation += 'sqrt('
            display = equation

        #if user clicks π
        if input == 'π':
            equation += str(math.pi)
            display += 'π'

        #if user clicks e
        if input == 'e':
            equation += str(math.e)
            display += 'e'

        #if user clicks !

        #if user clicks INV
        if input == "INV":
            if in_inverse_mode:
                in_inverse_mode = False
                board[1][1] = "sin"
                board[1][2] = "cos"
                board[1][3] = "tan"
            else:
                in_inverse_mode = True
                board[1][1] = "sin-1"
                board[1][2] = "cos-1"
                board[1][3] = "tan-1"

        #if user clicks RAD
        if input == "RAD":
            if in_radian_mode:
                in_radian_mode = False
            else:
                in_radian_mode = True

        #if user clicks =
        if input == "=":
            if equation != '': display = str(calculate(equation)) #if equation is not null // if user has entered something
            equation = display
            if display == UNDEFINED: equation = ''
            if display == SYNTAX_ERROR: equation = ''

def backspace():
    global display
    global equation

    if len(equation) > 0:
        length = len(equation)-1
        equation = equation.replace(equation[length], '', 1)
        display = equation


####################################################################
                        #DISPLAY CODE
####################################################################

info_font = pygame.font.SysFont('Arial', 18)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            left, middle, right = pygame.mouse.get_pressed()
            if left:
                x,y = pygame.mouse.get_pos() #get mouse position when user clicks
                button_click(x,y)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                backspace()

    screen.fill(background_color)

    #resize display if necessary:
    if len(str(display)) > 15:
        size = 40 * (15/len(str(display)))
        display_font = pygame.font.SysFont('Arial', int(size))
    else: display_font = pygame.font.SysFont('Arial', 40)


    #draw gridlines
    for i in range(WIDTH):
        for j in range(HEIGHT):
            x1 = (width/WIDTH)*i
            y1 = ((height-120)/HEIGHT)*j

            box_w = width/WIDTH
            box_h = (height-120)/HEIGHT
            mouse_x, mouse_y = pygame.mouse.get_pos()

            #draw button backpanels
            if mouse_x > x1 and mouse_x < x1+box_w and mouse_y > y1+120 and mouse_y < y1+120+box_h: 
                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(screen, btn_down_color, pygame.Rect(x1, y1+120, box_w, box_h))
                else:
                    pygame.draw.rect(screen, btn_hovering_color, pygame.Rect(x1, y1+120, box_w, box_h))

            else: pygame.draw.rect(screen, background_color, pygame.Rect(x1, y1+120, box_w, box_h))

            #draw dividing lines
            pygame.draw.line(screen, line_color, (x1,0+120), (x1,height+120), 4)
            pygame.draw.line(screen, line_color, (0,y1+120), (width, y1+120), 4)

            #draw text
            text = btn_font.render(str(board[j][i]), False, (0, 0, 0))
            text_rect = text.get_rect(center=(x1+box_w/2+4,y1+120+box_h/2+4)) #center text within respective boxes
            screen.blit(text, text_rect)

    text = display_font.render(str(display), False, (0,0,0)) #display user input on panel
    screen.blit(text, (10,10))

    if in_radian_mode:
        text = info_font.render("RAD", False, (0,0,0)) #show radian mode
    else:
        text = info_font.render("DEG", False, (0,0,0)) #show degree mode
    screen.blit(text, (width-100, 100))

    if in_inverse_mode:
        text = info_font.render("INV", False, (0,0,0)) #show inverse mode
    else:
        text = info_font.render("TRIG", False, (0,0,0)) #show trig mode
    screen.blit(text, (width-50, 100))

    #draw border
    pygame.draw.line(screen, line_color, (0,0), (0,height-2), 4)
    pygame.draw.line(screen, line_color, (0,0), (width-2,0), 4)
    pygame.draw.line(screen, line_color, (width-2, 0), (width-2, height-2), 4)
    pygame.draw.line(screen, line_color, (0, height-2), (width-2, height-2), 4)

    time.sleep(1/FPS)
    pygame.display.update()

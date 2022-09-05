#Josh Muszka
#May 22, 2022
#Last updated: September 4, 2022
#Calculator -- use it to solve arithmetic
#can perform any basic arithmetic operation on any rational value

#TODO: allow user to enter any number of operators in a row (+ and - only)
#TODO: error catching if user doesn't enter a full equation (when numbers and operators don't match)
#TODO: error catching if user presses = with no equation entered

import pygame, sys, time

####################################################################
                            #SETUP
####################################################################

#PYGAME CONFIG
pygame.init()
pygame.font.init()
btn_font = pygame.font.SysFont('Arial', 40)
display_font = pygame.font.SysFont('Arial', 40)
pygame.display.set_caption("Calculator")

#DISPLAY INFO
width, height = 360, 480
size = width, height
screen = pygame.display.set_mode(size)
FPS = 144
background_color = 0xFF, 0xE5, 0xAB 
line_color = 0x6E, 0x1D, 0x1D
btn_hovering_color = 0xFA, 0xE0, 0x96
btn_down_color = 0xCA, 0xB0, 0x66

#BUTTON SETUP
GRID = 4
board=[] #0 if space hasn't been filled, 1 if filled by x, -1 if filled by o
row = [1,2,3,"+"]
board.append(row)
row = [4,5,6,"-"]
board.append(row)
row = [7,8,9,"*"]
board.append(row)
row = [".",0,"=","/"]
board.append(row)

#CALCULATOR VARIABLES
display = '' #what gets displayed on calculator "screen"
equation = '' #the sequence of numbers and operators the user enters to be calculated


####################################################################
                        #CALCULATION CODE
####################################################################

#main calculation code
def calculate(equation):
    global display

    #parse numlist
    #parse oplist
    #answer = numlist[0]
    #loop to get answer

    if equation[0] == '-': equation = '0' + equation
    elif equation[0] == '+': equation = '0' + equation
    elif equation[0] == '*' or equation[0] == '/': return 'Error: Incomplete equation'
    elif equation[0] == '.': equation = '0+0' + equation
    else: equation = '0+' + equation

    #NEW POTENTIALLY BROKEN CODE#
    op_list = []
    num_list = []
    equation2 = equation

   #generate op_list
    for i in range(len(equation)):
        if equation[i].isdigit() or equation[i] == '.': equation = equation.replace(equation[i], ' ', 1)
    op_list = equation.split()

    for i in range(len(op_list)):
        if len(op_list[i]) == 2:
            if op_list[i][0] == op_list[i][1]: op_list[i] = '+'
            else: op_list[i] = '-'


    #generate num_list
    for i in range(len(equation2)):
        if equation2[i] == '+' or equation2[i] == '-' or equation2[i] == '*' or equation2[i] == '/':
            equation2 = equation2.replace(equation2[i], ' ', 1)
    num_list = equation2.split()


    #END NEW POTENTIALLY BROKEN CODE#

    answer = float(num_list[0])
    for i in range(len(op_list)):
        if op_list[i] == '+': answer += float(num_list[i+1])
        elif op_list[i] == '-': answer -= float(num_list[i+1])
        elif op_list[i] == '*': answer *= float(num_list[i+1])
        elif op_list[i] == '/': 
            try: 
                answer /= float(num_list[i+1])
            except ZeroDivisionError:
                return 'Undefined'

    answer = round_num(answer)
    return answer


#rounding final answer
def round_num(num):
        
    num = round(num, 7) #round number to 7 decimal places

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

    if int(y) > 120:
        #convert x,y positions to positions on grid
        x = int((x/width)*GRID)
        y = int(((y-120)/(height-120))*GRID)

        input = str(board[y][x])

        #if user clicks a number, ., +, -, *, or /
        if y <= 2 and x <= 2 or board[y][x] == 0 or board[y][x] == '.' or board[y][x] == '+' or board[y][x] == '-' or board[y][x] == '*' or board[y][x] == '/':
            equation += input
            display = equation
                    

        #if user clicks =
        if (board[y][x] == "="):
            display = str(calculate(equation))
            equation = display
            if display == 'Undefined': equation = '0'




####################################################################
                        #DISPLAY CODE
####################################################################

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            left, middle, right = pygame.mouse.get_pressed()
            if left:
                x,y = pygame.mouse.get_pos() #get mouse position when user clicks
                button_click(x,y)

    screen.fill(background_color)

    #resize display if necessary:
    if len(str(display)) > 15:
        size = 40 * (15/len(str(display)))
        display_font = pygame.font.SysFont('Arial', int(size))
    else: display_font = pygame.font.SysFont('Arial', 40)


    #draw gridlines
    for i in range(GRID):
        for j in range(GRID):
            x1 = (width/GRID)*i
            y1 = ((height-120)/GRID)*j

            box_w = width/GRID
            box_h = (height-120)/GRID
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

    text = display_font.render(str(display), False, (0,0,0))
    screen.blit(text, (10,10))

    #draw border
    pygame.draw.line(screen, line_color, (0,0), (0,height-2), 4)
    pygame.draw.line(screen, line_color, (0,0), (width-2,0), 4)
    pygame.draw.line(screen, line_color, (width-2, 0), (width-2, height-2), 4)
    pygame.draw.line(screen, line_color, (0, height-2), (width-2, height-2), 4)

    time.sleep(1/FPS)
    pygame.display.update()

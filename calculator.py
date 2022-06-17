#Josh Muszka
#May 22, 2022
#Last updated: June 16, 2022
#Calculator -- use it to solve arithmetic
#can perform any basic arithmetic operation on any rational value

#BUG: buttons slightly vertically misaligned
#BUG: -0.0
#BUG: clear answer when entering new number after calculating
#BUG: rounding off really small values (not technically a bug, but fix it)
#BUG: clicking numbers repeats number on display, but calculation performs just fine
#TODO: add repeated decimal indicator
#TODO: dynamic button colors

#TODO: CLEAN UP CODE
#TODO: DOCUMENT CODE
#TODO: dynamic display resizing

#TODO: negative number support

import pygame, sys, time

####################################################################
                            #SETUP
####################################################################

#PYGAME CONFIG
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 40)
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

#CALCULATION VARIABLES
number = 0
input = ''
display = ''
num_list = []
operator_list = ['+']


####################################################################
                        #CALCULATION CODE
####################################################################

#rounding final answer
def round_num(num):
    num = round(num, 7) #round number to 14 decimal places

    #remove unecessary zeroes from end of number:
    num = str(num)
    length = len(num)

    while num[length-1] == '0': #while the last digit of the number is 0
        num = num[:(length-1)]
        length = len(num)

    if num[length-1] == '.': num = num[:(length-1)] #remove uncessecary decimal place

    return num



#main calculation code
def calculate(x,y):
    global input
    global display
    global number
    global num_list
    global operator_list

    if int(y) > 120:
                    #convert x,y positions to positions on grid
                    x = int((x/width)*GRID)
                    y = int((y/(height-80))*GRID)

                    #if user clicks a number
                    if y < 4 and x < 3 or board[y-1][x] == 0:
                        input = str(input) + str(board[y-1][x]) #get input
                        display += input
                    
                    #if user clicks .
                    if board[y-1][x] == '.':
                        input = str(input) + '.' #get input
                        display += input

                    #if user clicks +
                    if board[y-1][x] == '+':
                        display+='+'
                        number = str(number)+'+'+str(input)
                        input = '' 
                        operator_list.append('+')

                    #if user clicks -
                    if board[y-1][x] == '-':
                        display+='-'
                        number = str(number)+'-'+str(input)
                        input = '' 
                        operator_list.append('-')
                    
                    #if user clicks *
                    if board[y-1][x] == '*':
                        display+='*'
                        number = str(number)+'*'+str(input)
                        input = '' 
                        operator_list.append('*')

                    #if user clicks /
                    if board[y-1][x] == '/':
                        display+='/'
                        number = str(number)+'/'+str(input)
                        input = '' 
                        operator_list.append('/')

                    #if user clicks =
                    if (board[y-1][x] == "="):
                        number = str(number)+'+'+str(input)

                        #parse numbers from number
                        number = number.replace('+', ' ')
                        number = number.replace('-', ' ')
                        number = number.replace('*', ' ')
                        number = number.replace('/', ' ')
                        num_list = number.split()
                        input = ''

                        #get total
                        total = 0
                        for i in range(len(num_list)-1):
                            if operator_list[i] == '+':
                                total += float(num_list[i+1])
                            if operator_list[i] == '-':
                                total -= float(num_list[i+1])
                            if operator_list[i] == '*':
                                total *= float(num_list[i+1])
                            if operator_list[i] == '/':
                                total /= float(num_list[i+1])
                        display = round_num(total)




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
                calculate(x,y)

    screen.fill(background_color)



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
            text = my_font.render(str(board[j][i]), False, (0, 0, 0))
            text_rect = text.get_rect(center=(x1+box_w/2+4,y1+120+box_h/2+4)) #center text within respective boxes
            screen.blit(text, text_rect)

    text = my_font.render(str(display), False, (0,0,0))
    screen.blit(text, (10,10))

    #draw border
    pygame.draw.line(screen, line_color, (0,0), (0,height-2), 4)
    pygame.draw.line(screen, line_color, (0,0), (width-2,0), 4)
    pygame.draw.line(screen, line_color, (width-2, 0), (width-2, height-2), 4)
    pygame.draw.line(screen, line_color, (0, height-2), (width-2, height-2), 4)

    time.sleep(1/FPS)
    pygame.display.update()
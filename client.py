import pygame
#game.py
#surface = screen	
from grid import Grid	

width, height = 389, 580
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("FindMyMines")
##########################################################################
import threading

def create_thread(target): #thread --> sending keepalive packets/collection
#useful only when main is running
	thread = threading.Thread(target = target)
	thread.daemon = True
	thread.start()

import socket
#192.168.1.111
hostname = socket.gethostname()    

HOST = socket.gethostbyname(hostname) 
PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#listen is on server side
sock.connect((HOST,PORT))

def receive_data():
	while True:
		data = sock.recv(1024).decode()
		#1024= byte lenght (can receieve) --> 1Magabyte
		print(data)

create_thread(receive_data)
##########################################################################
grid = Grid() #grid is object of ckass Grid

#grid.set_cell_value(1,1,'x')

grid.print_grid()
running = True
player = 0

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:	
			#print(pygame.mouse.get_pressed())
			if pygame.mouse.get_pressed()[0]:
				mouse = pygame.mouse.get_pos()
				cellX, cellY = mouse[0]//64, mouse[1]//64
				xGrid = mouse[0]//64
				yGrid = mouse[1]//64
				grid.get_mouse(xGrid,yGrid,player)
				grid.check_bomb(xGrid,yGrid,player)

				send_data = '{}-{}'.format(xGrid,yGrid).encode() 
				sock.send(send_data)
				#print(grid.moves)
				if grid.switch_player:
					if player == 0:
						player = 1
					else:
						player = 0
				#xpos = int((mouse[0])/64.0)
				#ypos = int((mouse[1])/64.0)
				#boardh[ypos][xpos]=True
				grid.print_grid()

	screen.fill((0,0,0))

	grid.drawBoard(screen)

	pygame.display.flip()







import pygame
#game.py
#surface = screen	
from grid import Grid	

width, height = 389, 580
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("FindMyMines")

#########################################################################
import threading

def create_thread(target): #thread --> sending keepalive packets/collection
#useful only when main is running
	thread = threading.Thread(target = target)
	thread.daemon = True
	thread.start()

import socket

hostname = socket.gethostname()  

HOST = socket.gethostbyname(hostname) 
PORT = 5555
connection_established = False
conn,addr = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#AF_INET is IPV4 #SOCK_STREAM is TCP
sock.bind((HOST,PORT))
sock.listen(1) #listen to connection
#if 5 players then sock.listen(5)
def receieve_data():
	while True:
		data = conn.recv(1024).decode()
		print(data)

def waiting_for_connection(): 
	global connection_established, conn, addr
	conn,addr = sock.accept() #Wait for connection, it is a blocking method
	print('Client is connected')
	connection_established = True
	receieve_data()

create_thread(waiting_for_connection)
#############################################################################

grid = Grid() #grid is object of ckass Grid

#grid.set_cell_value(1,1,'x')

grid.print_grid()
running = True
player = 0

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN and connection_established:	#not grid.game_over
			#print(pygame.mouse.get_pressed())
			if pygame.mouse.get_pressed()[0]:
				mouse = pygame.mouse.get_pos()
				print(mouse[0]//64 ,mouse[1]//64)
				xGrid = mouse[0]//64
				yGrid = mouse[1]//64
				grid.get_mouse(xGrid,yGrid,player)
				grid.check_bomb(xGrid,yGrid,player)

				send_data = '{}-{}'.format(xGrid,yGrid).encode() #this returns string #send data to socket
				conn.send(send_data) #conn object is create when client is connected

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







from PyQt5 import uic, QtWidgets
from pyfirmata import Arduino
from random import randrange
import pygame
from time import sleep


pygame.init()
PONTOS = 0
JOGOS = 0
PINOS = [8, 9, 10]
selected_pin = randrange(8, 11)
board = ''


def toca_som(som):
	pygame.mixer.music.load(som)
	pygame.mixer.music.play()


def verifica(selected_pin, this_pin):
	global PONTOS, JOGOS
	JOGOS += 1
	if JOGOS == 10:
		JOGOS = PONTOS = 0
		gui2.lb_pontuacao.setText(f'Pontuação: {PONTOS} / {JOGOS}')
	if selected_pin == this_pin:
		PONTOS += 10
		toca_som('sons/resposta_certa.mp3')
		gui2.lb_pontuacao.setText(f'Pontuação: {PONTOS} / {JOGOS}')
	else:
		toca_som('sons/resposta_errada.mp3')
		gui2.lb_pontuacao.setText(f'Pontuação: {PONTOS} / {JOGOS}')
	board.digital[selected_pin].write(1)
	sleep(0.5)
	board.digital[selected_pin].write(0)


def btn_led1_click():
	global board, selected_pin, JOGOS
	verifica(selected_pin, PINOS[0])
	selected_pin = randrange(8, 11)


def btn_led2_click():
	global board, selected_pin, JOGOS
	verifica(selected_pin, PINOS[1])
	selected_pin = randrange(8, 11)


def btn_led3_click():
	global board, selected_pin, JOGOS
	verifica(selected_pin, PINOS[2])
	selected_pin = randrange(8, 11)


def btn_comecar_click():
	global board
	nome = gui.in_nome.text()
	port = gui.in_port.text()

	if (nome and port) and port.isnumeric() == True:
		try:
			board = Arduino(f'COM{int(port)}')
			gui2.lb_nome.setText(f'Nome do jogador: {nome}')
			gui2.lb_pontuacao.setText(f'Pontuação: {PONTOS} / {JOGOS}')
			gui2.btn_led1.clicked.connect(btn_led1_click)
			gui2.btn_led2.clicked.connect(btn_led2_click)
			gui2.btn_led3.clicked.connect(btn_led3_click)
			gui2.show()
			gui.hide()
		except:
			toca_som('sons/tente_novamente.mp3')
	else:
		toca_som('sons/tente_novamente.mp3')


app = QtWidgets.QApplication([])
gui = uic.loadUi('ui/Gui1.ui')
gui.setFixedSize(850, 550)
gui2 = uic.loadUi('ui/Gui2.ui')
gui2.setFixedSize(850, 550)

gui.btn_comecar.clicked.connect(btn_comecar_click)

gui.show()
app.exec()

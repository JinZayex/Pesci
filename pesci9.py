"""
  11     #...............................................................................
1111     #...............................................................................
  11     #...................INTRODUZIONE.............
  11     #...............................................................................
111111   #...............................................................................
         #...............................................................................
"""
import pygame, sys, time

pygame.init()

SCREEN_W = 720
SCREEN_H = 720

WIDTH = 520
HEIGHT = 520
WINDOW = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("PESCI")

BLACK = (0, 0, 0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLUE = (0,0,255)

"""
 2222     #......................................................................................
22  22    #......................................................................................
   22     #....................CLASSI E FUNZIONI.................
  22      #......................................................................................
222222    #......................................................................................

"""

#Generare una classe Square con gli attributi x,y,colore e velocity(lunghezza dei "passi" fatti dal quadrato)
class Square:
    def __init__(self,x,y,color,vel):
        self.x = x
        self.y = y
        self.img = pygame.draw.rect(WINDOW,color,[self.x, self.y, 20, 20], 0) 
        self.vel = vel
    #Disegna quadrato
    def move(self, window):
        window.blit(self.img, (self.x, self.y))
        for square in self.squares:
            square.draw(window)

def reverse(lista):
    reversed_lista = lista.reverse()
    return reversed_lista

"""
 3333     #......................................................................................
33  33    #......................................................................................
   333    #....................VARIABILI GLOBALI..............................
33  33    #........ ..(creazione di liste, "pace" e "recinzione").......................................................
 3333     #......................................................................................
 
"""
#coordinates boundaries
(bound1x, bound1y) = ( (SCREEN_W-WIDTH)//2,(SCREEN_H-HEIGHT)//2 +20) 
(bound2x,  bound2y) = ( (SCREEN_W-((SCREEN_W-WIDTH)//2),  (SCREEN_H-HEIGHT)//2+20))
(bound3x, bound3y) = ((SCREEN_W-((SCREEN_W-WIDTH)//2),  (SCREEN_H-(SCREEN_H-HEIGHT)//2)))
(bound4x, bound4y) = ((SCREEN_W-WIDTH)//2,(SCREEN_H-(SCREEN_H-HEIGHT)//2))

coordinates = [(bound1x, bound1y),
    (bound2x,  bound2y),
    (bound3x, bound3y),
    (bound4x, bound4y)
    ]

"""
LISTE.....
"""
#Genera una lista con le x-coordinate di ogni singolo quadrato**
#(quadrato 1 ---ha----> x_coord = x[0],
# quadrato 2 ---ha----> x_coords = x[1] and so on...)

x = []
for i in range(SCREEN_W//2+20, (SCREEN_W-(SCREEN_W - WIDTH)//2+ 40), 20):
    x.append(i)

x_green = []
for i in range(SCREEN_W//2-40, (SCREEN_W-WIDTH)//2-60, -20):
    x_green.append(i)

x_ball = x + x_green
for i in range(len(x_ball)):
    x_ball[i] += -10

#Genera liste con y-coord (stesso valore legato a quadrato green e quadrato white, _________ si differenziano per x_coord  e vel opposta )
y = []
for i in range(SCREEN_H//2, SCREEN_H- (SCREEN_H-HEIGHT)//2,20):
    y.append(i)

y_up = []
for i in range(SCREEN_H//2, (SCREEN_H-HEIGHT)//2, -20):
    y_up.append(i)

y_ball = []
for i in range(len(y)-1,-1,-1): 
    y_ball.append(y[i])


#Genera lista con gli step (vel) di ogni quadrato (l'inverso sarà il valore del quadrato green sulla stessa riga),
#Ogni quadrato, nel momento in cui tocca boundaries, inverte vel
#Questo crea confini (l'effetto "rimbalzo") e ha bisogno di essere unico per ogni oggetto quadrato
vels = []
for i in range(HEIGHT//40):
    vels.append(20)


#Genera lista contente tutti gli oggetti white square, con le caratteristiche sopra riportate
#La lista avrà lunghezza 13. I quadrati bianchi sono 1 (angolo) + 12 * 2 = 25  (25 sono anche i quadrati green)
squares = []
for k in range(HEIGHT//40):
    square = Square(x[k],y[k], WHITE, vels[k])
    squares.append(square)


PACE = 0.006

"""
44  44    #......................................................................................
44  44    #......................................................................................
444444    #.....................MAIN LOOP..................
    44    #......................................................................................
    44    #......................................................................................

"""

def main(PACE):

    run = True
    while run:
        #...EVENTI.........................................
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            print("Quit!")
            pygame.quit()

        #...AUGM and REDUC PACE.........................................
        if keys[pygame.K_z]:
            PACE *= 2
            print(f'Pace reduct, current pace: {PACE}')
            
        if keys[pygame.K_m]:
            PACE /= 2
            print(f"Pace augm, current pace:  {PACE}")
            

        """                                                    555555
        #..........|°°°°°°°°°°°°°^^^°°°°°°°°°°°°°°°|.........  55       .........................
        #..........|......DRAWING ON SCREEN........|.......    555555
        #..........|_______________________________|..........      55  ..........................
                              ---------                        555555
        """                                                          
        WINDOW.fill(BLACK)

        BOUNDARIES = pygame.draw.polygon(WINDOW, GREEN, coordinates, True)

        for square in range(len(squares)):
            #Genera movimento, decrementando x_coord del generico square white e del generico square green
            x[square] -= vels[square]
            x_green[square] += vels[square]

            #Fa rimbalzare il quadrato (sia il white che il green "inverso") quando tocca confini... BOINK! 
            if (x[square]< bound1x) or (x[square] + 20 > bound2x):
                print("       Boink!")
                x[square] += vels[square]
                x_green[square] -= vels[square] 

                vels[square] = -vels[square]
                x[square] -= vels[square]
                x_green[square] += vels[square]
                
                """
            elif x_green[square] < (SCREEN_W - WIDTH)//2 or (x_green[square]+20)> WIDTH + (SCREEN_W-WIDTH)//2:
                x_green[square] -= vels[square] 
                vels[square] = -vels[square]
                x_green[square] += vels[square]
                """
                
            #Disegna sullo schermo file di quadrati indipendenti!
            white_squares= Square(x[square],y[square],WHITE, vels[square])
            white_squares_up= Square(x[square],y_up[square],WHITE, vels[square])
            green_squares= Square(x_green[square],y[square],GREEN, vels[square])
            green_squares_up= Square(x_green[square],y_up[square],GREEN, vels[square])
            #ball = Square(x_ball[square], y_ball[square], YELLOW,vels[square])


            time.sleep(PACE)
        pygame.display.update()

    
main(PACE)     

#RISOLUZIONE PROBLEMA --> quadrato in alto a dx mancante
"""
abbassare il tetto della green boundaries 
(nota che whitesquares e whitesquares up hanno controllo dello stesso quadrato, cioè la punta della freccia)
---> uno sovrascrive l'altro
"""

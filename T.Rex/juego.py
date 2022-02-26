import random
import pygame



Corriendo = [pygame.image.load('Imagenes/Dino1run1.png'),
             pygame.image.load('Imagenes/Dino1idle.png'),
             pygame.image.load('Imagenes/Dino1run2.png'),
             pygame.image.load('Imagenes/Dino1run2.png'),
             pygame.image.load('Imagenes/Dino1run1.png'),
             pygame.image.load('Imagenes/Dino1idle.png')]

Salto = [pygame.image.load('Imagenes/Dino1idle.png'),
         pygame.image.load('Imagenes/Dino1idle.png'),]

Enemigo =[pygame.image.load('Imagenes/Dino2run1.png'),
            pygame.image.load('Imagenes/Dino2idle.png'),
            pygame.image.load('Imagenes/Dino2run2.png'),
            pygame.image.load('Imagenes/Dino2run2.png'),
            pygame.image.load('Imagenes/Dino2run1.png'),
            pygame.image.load('Imagenes/Dino2idle.png')]

#Colores#
BlueSky= (9, 187, 214)
Orange= (242,172,81)
BlueNigth= (25, 37, 56)
#Pantalla#
w=1200
h=800
#FPS#
FPS = 30

x=0
i= 0
j=0
z=0
k=0
ox=w+200
px=250
py=460
corriendo= True
obstaculo= True
salto = False
bajar=False
gameover = False

def recargaPantalla():
    #Variables globales
    global salto
    global x
    global i
    global z
    global j
    global ox
    global gameover
    if z <=200:
        Pantalla.fill(BlueSky)
        if z==200:
            j+=1
        
    elif z>200 and z<290 :
        Pantalla.fill(Orange)
        
    elif z>=290 and z<530:
        Pantalla.fill(BlueNigth)
    elif z>=530:
        j+=1
        z=0
    

    #Fondo en movimiento
    x_relativa = x % fondo.get_rect().width
    Pantalla.blit(fondo, (x_relativa - fondo.get_rect().width, 0))
    if x_relativa < w:
        Pantalla.blit(fondo, (x_relativa, 0))
        pygame.display.flip()
        z += 1;

    if gameover == True:
        x+=0
            
    if j ==0 and gameover == False:
        x -= 15
    if j ==1 and gameover == False:
        x -= 20
    if j >=2 and gameover == False:
        x -= 25
    if salto == False:
        if keys[pygame.K_SPACE]:
            salto = True
    if keys[pygame.K_5] and gameover == True:
        x=0
        i= 0
        j=0
        z=0
        gameover = False
    
    

class Jugador(pygame.sprite.Sprite):
    
    def __init__(self):
        global salto
        super().__init__()
        self.image=pygame.transform.scale(Salto[0], (150, 175))
        self.rect = self.image.get_rect() 
        if salto == False:
            self.rect.center = (px , py)
            

    def update(self):
        global corriendo
        global salto
        global i
        global j
        global k
        global py
        global px
        global bajar
        if corriendo == True:
            self.image=pygame.transform.scale(Corriendo[i], (150, 175))
            if i>=5 :
                i=-1
            i += 1
        if salto == True and gameover == False:
            corriendo = False   
            self.rect.center = (px , py)    
            if py > 220 and bajar ==False:
                self.image=pygame.transform.scale(Salto[0], (150, 175))
                py -=30
            else:
                self.image=pygame.transform.scale(Salto[1], (150, 175))
                if bajar == False:
                    k+=1
                if k>=9:    
                    bajar = True
                    py +=30
                    if py == 460:
                        salto=False
                        corriendo= True
                        bajar = False
                        self.rect.center = (px , py)    
                        k=0
                
           
class Obstaculo(pygame.sprite.Sprite):
    
    def __init__(self):    
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Imagenes/Dino2idle.png'), (120, 120))

        self.rect = self.image.get_rect()              
       
    def update(self):
        global i
        global j
        global ox
        global gameover
        
        
        self.rect.center = (ox , 480)
        if gameover == True:
            ox+=0
            
        if j ==0 and gameover == False:
            ox -= 22
        if j ==1 and gameover == False:
            ox -= 27
        if j >=2 and gameover == False:
            ox -= 32
            
        if ox < 10:
            ox=1400
        self.image =pygame.transform.scale(Enemigo[i], (120, 120))
        if i==5:
                i=-1
        i += 1 
        
       


#Caracteristicas del Juego#
pygame.init()
Pantalla = pygame.display.set_mode((w,h))
Clock = pygame.time.Clock()

#Grupos de Sprites#
sprites= pygame.sprite.Group()
enemigos = pygame.sprite.Group()

#Instancias#
jugador = Jugador()
sprites.add(jugador)

obstaculo = Obstaculo()
enemigos.add(obstaculo)


    
fondo=pygame.image.load('Imagenes/Escenario.png')

icono=pygame.image.load('Imagenes/Dino1idle.png')
pygame.display.set_icon(icono)
pygame.display.set_caption('T-rex Runner')
pygame.mixer.music.load('Sonidos/Musica1.mp3')
pygame.mixer.music.play(-1)
#Fondo#


#Mantener juego abierto#
ejecutando = True

#Bucle de acciones y controles
while ejecutando:
    #FPS
    keys = pygame.key.get_pressed()
    Clock.tick(16)

    #Bucle del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False
    
    sprites.update()
    enemigos.update()
    colision = pygame.sprite.spritecollide(jugador, enemigos,False)
    if colision:
        corriendo= False
        gameover = True 
        jugador.image = pygame.transform.scale(pygame.image.load('Imagenes/Dino1D.png'), (150, 175))
    recargaPantalla()
    sprites.draw(Pantalla)
    enemigos.draw(Pantalla)
    
    
    pygame.display.flip()
    
    # Control del audio
    #Baja volumen
    if keys[pygame.K_9] and pygame.mixer.music.get_volume() > 0.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)
    #Sube volumen
    if keys[pygame.K_0] and pygame.mixer.music.get_volume() < 1.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.01)

pygame.quit()
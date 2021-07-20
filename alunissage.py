import pygame
from pygame import display
import os


#initialisation des variables
global HEIGHT
global WIDTH
global HAUTEUR_SOL
global X0
global Y0
# Abscisse du LEM
global XL
# Ordonnées du LEM
global YL
# Vitesse descendante du LEM
global VY
# Simulation de la pesanteur avec l'augmentation de la vitesse
global DELTA_VY
global ARRET
# Nombre de frames par seconde
global FPS
# Vrai quand on appui sur la barre espace
global BURST
# Vitesse max tolérée pour l'atterissage sans dommage
global VMAX_LANDING
# Landed est vrai lorsqu'on a réussi à atterrir avec le LEM
global LEM_LANDED
# Fonte utilsée pour écrire des textes sur l'écran
global FONT
# Nombre de litres de fuel restant
global FUEL
# Nombre de litres consommés par unité de temps avec les
# rétros fusées
global DELTA_FUEL
# Vrai si le LEM explose
global LEM_EXPLODED


def atterrissage():
    global YL,VY,DELTA_VY, LEM_LANDED, LEM_EXPLODED, BURST
    if ( YL>=Y0-HAUTEUR_SOL ):
        # Si la vitesse est inferieur à V_MAX_LANDING
        # alors on atterri
        if ( VY <= V_MAX_LANDING ):
            DELTA_VY = 0
            YL=Y0-HAUTEUR_SOL
            LEM_LANDED=True
            BURST = False
        # Sinon on explose le module
        else :
            LEM_EXPLODED=True
            BURST = False
            
        
    # C'est de la triche !!
    #if (VY>=0.07 and YL==Y0-HAUTEUR_SOL):
    #    YL = 10
    #     VY = 0
    

def display_background():
    WIN.fill( (0,0,0))
    pygame.draw.rect(WIN , (255,255,255),pygame.Rect(X0,Y0,WIDTH,HAUTEUR_SOL))

def display_element():
    global BURST,XL,YL,VY,FONT,FUEL,LEM_EXPLODED
    if ( not LEM_EXPLODED ):
        WIN.blit(LEM,(XL,YL))
    else:
        imgExplode = FONT.render('BOOM ! BOOM !' , True, (255,255,255))
        WIN.blit( imgExplode , (XL,YL))    
        
    # Si on est en mode combustion
    # On affiche une flamme jaune qui sort du moteur
    if ( BURST ):
        pygame.draw.polygon( WIN ,(255,255,0) , [(XL+20 , YL+55 ) , ( XL+25 , YL+80 ) ,  (XL+30, YL+55)])
    # On affiche sur l'écran la vitesse ascentionnelle
    strVY = str('{0:.2f}'.format(-VY))
    imgVitesse = FONT.render('Vitesse ascentionnelle : '+ strVY , True, (255,255,255))
    WIN.blit( imgVitesse , ( 20,20))
    # On affiche le carburant restant
    imgFuel = FONT.render('Litres carburant restant : '+ str(FUEL) , True, (255,255,255))
    WIN.blit( imgFuel , ( 20,50))
    
    
    
    
def compute_element_pos(  ):
    global VY,YL,BURST, FUEL, DELTA_FUEL
    key = pygame.key.get_pressed()
    if ( key[ pygame.K_SPACE ]):
        if FUEL > 0 :
            VY -= DELTA_VY
            BURST = True
            FUEL -= DELTA_FUEL
        if FUEL <= 0:
            BURST = False
            FUEL = 0
            VY += DELTA_VY
    else:
        VY += DELTA_VY
        BURST = False
    YL += VY
    
pygame.init()
WIN = pygame.display.set_mode((800,500))

HEIGHT = 500
WIDTH = 800
HAUTEUR_SOL =50
X0 = 0
Y0 = HEIGHT-HAUTEUR_SOL
XL = WIDTH/2
YL = 10
LEM = pygame.image.load(os.path.join('images','lem-appolo11.png'))
LEM = pygame.transform.scale( LEM , (50,60))
VY = 0
DELTA_VY = 0.003
V_MAX_LANDING = 0.5
LEM_LANDED = False
LEM_EXPLODED = False
clock = pygame.time.Clock() 
FPS = 60
BURST = False
FONT = pygame.font.SysFont('chalkduster.ttf', 24)
FUEL = 6000
DELTA_FUEL = 20



run = True
while run:
    
    # On gère les frames par secondes
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    
    display_background()
    if ( not LEM_LANDED and not LEM_EXPLODED ):
        compute_element_pos()
    
    display_element()
    atterrissage()
    pygame.display.update()

pygame.quit
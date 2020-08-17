import random
import sys #for exiting game sys.exit
import pygame
from pygame.locals import * #basic pygame imports
pygame.mixer.init()

#global variables
FPS=32
SCREENWIDTH=289
SCREENHEIGHT=511
SCREEN=pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY=SCREENHEIGHT*0.8
GAME_SPRITES= {}
GAME_SOUNDS= {}
PLAYER='gallery/images/bird.png'
BACKGORUND='gallery/images/background.png'
PIPE='gallery/images/pipe.png'

def welcomeScreen():
    #shows welocome images on screen
    playerx=int(SCREENWIDTH/5) #x-corinate of bird
    playery=int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    basex=0
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],( 0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx, playery))
                SCREEN.blit(GAME_SPRITES['base'],(basex, GROUNDY))
                pygame.display.update() 
                FPSCLOCK.tick(FPS) 


def getrandompipe():
    #for two pipe
    pipeheight=GAME_SPRITES['pipe'][0].get_height()
    offset=int(SCREENHEIGHT/3)
    y2=offset+random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()-1.2*offset))
    pipex=SCREENWIDTH+10
    y1=pipeheight-y2+int(offset)
    pipe = [
        {'x':pipex, 'y':-y1},
        {'x':pipex, 'y': y2} 
    ]
    return pipe
u
def iscollide(playerx, playery, upperpipe, lowerpipe):
    if playery> GROUNDY -25 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperpipe:
        pipeheight=GAME_SPRITES['pipe'][0].get_height()
        if(playery<pipeheight + pipe['y'] and abs(playerx-pipe['x'])<GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerpipe:
        if(playery + GAME_SPRITES['player'].get_height() > pipe['y']) and (abs(playerx-pipe['x'])<GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    return False


def mainGame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENWIDTH/2)
    basex=0

    #create 2 pipes for blittigng on screen
    newpipe1=getrandompipe()
    newpipe2=getrandompipe()

    #list of upper pipes
    upperpipe=[
        {'x': SCREENWIDTH+200, 'y':newpipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newpipe2[0]['y']}
    ]

    #list of lower pipes
    lowerpipe=[
        {'x': SCREENWIDTH+200, 'y':newpipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newpipe2[1]['y']}
    ]
    pipevelx=-4
    playervely=-9
    playermaxvely=10
    playerminvely=-8
    playeraccy=1
    playerflapaccv= -8 #velocity while flapping
    playerflapped=False #true when bird flapping

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    playervely=playerflapaccv
                    playerflapped=True
                    GAME_SOUNDS['wing'].play()

            crashtest=iscollide(playerx, playery, upperpipe, lowerpipe)

            if crashtest:
                return
        
            #check for score
            playermidpos=playerx+GAME_SPRITES['player'].get_width()/2
            for pipe in upperpipe:
                pipemidpos=pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
                if pipemidpos<=playermidpos <pipemidpos + 4:
                    score+=1
                    print(f"your score is {score}")
                    GAME_SOUNDS['point'].play()

            if playervely < playermaxvely and not playerflapped:
                playervely+=playeraccy

            if playerflapped:
                playerflapped=False
            playerheight=GAME_SPRITES['player'].get_height()
            playery=playery+min(playervely, GROUNDY-playery-playerheight)

            #moving pipes to the left
            for upperpip, lowerpip in zip(upperpipe, lowerpipe):
                upperpip['x'] +=pipevelx
                lowerpip['x'] +=pipevelx
 
            #adding pipe 
            if 0<upperpipe[0]['x']<5:
                newpipe=getrandompipe()
                upperpipe.append(newpipe[0])
                lowerpipe.append(newpipe[1])

            #if pipe out of screen remove it
            if upperpipe[0]['x']< -GAME_SPRITES['pipe'][0].get_width():
                upperpipe.pop(0)
                lowerpipe.pop(0)

            SCREEN.blit(GAME_SPRITES['background'], (0, 0))
            for upperpip, lowerpip in zip(upperpipe, lowerpipe):
                SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpip['x'], upperpip['y']))
                SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpip['x'], lowerpip['y']))
            SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
            SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
            mydigits = [int(x) for x in list(str(score))]
            width=0
            for digit in mydigits:
                width+=GAME_SPRITES['numbers'][digit].get_width()
            Xoffset=(SCREENWIDTH - width)/2

            for digit in mydigits:
                SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
                Xoffset+=GAME_SPRITES['numbers'][digit].get_width()
            pygame.display.update ()
            FPSCLOCK.tick(FPS)






        


if __name__ == "__main__":
    #game will start from here
    pygame.init() #initialise pygame modules
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')

    #game images

    GAME_SPRITES['numbers']=(
        pygame.image.load('gallery/images/0.png').convert_alpha(),
        pygame.image.load('gallery/images/1.png').convert_alpha(),
        pygame.image.load('gallery/images/2.png').convert_alpha(),
        pygame.image.load('gallery/images/3.png').convert_alpha(),
        pygame.image.load('gallery/images/4.png').convert_alpha(),
        pygame.image.load('gallery/images/5.png').convert_alpha(),
        pygame.image.load('gallery/images/6.png').convert_alpha(),
        pygame.image.load('gallery/images/7.png').convert_alpha(),
        pygame.image.load('gallery/images/8.png').convert_alpha(),
        pygame.image.load('gallery/images/9.png').convert_alpha(),
    )
    GAME_SPRITES['base']=pygame.image.load('gallery/images/base.png').convert_alpha()
    GAME_SPRITES['pipe']= (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
    pygame.image.load(PIPE).convert_alpha()
    )

    #game sound
    GAME_SOUNDS['die']=pygame.mixer.Sound('gallery/sound/die.wav')
    GAME_SOUNDS['hit']=pygame.mixer.Sound('gallery/sound/hit.wav')
    GAME_SOUNDS['point']=pygame.mixer.Sound('gallery/sound/point.wav')
    GAME_SOUNDS['swoosh']=pygame.mixer.Sound('gallery/sound/swoosh.wav')
    GAME_SOUNDS['wing']=pygame.mixer.Sound('gallery/sound/wing.wav') 

    GAME_SPRITES['background'] = pygame.image.load(BACKGORUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()
     

    while True:
        welcomeScreen() #shows welcome screen till press
        mainGame() #main game function


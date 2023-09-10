from pygame import *
from random import *
from math import *

init()
print("C'est parti ! Le premier à 8 points gagne")
hauteuréc=800
largeuréc=800

screen = display.set_mode([hauteuréc,largeuréc])
bg=image.load("fond.png").convert()
running=True
run2=True

class Bonus(sprite.Sprite):
    def __init__(self):
        super (Bonus,self).__init__()
        self.surf=Surface((10,10))
        self.ran=randint(0,3)
        if self.ran==1:
            self.surf.fill((255,215,0))
        elif self.ran==0:
            self.surf.fill((0,255,0))
        elif self.ran==2:
            self.surf.fill((0,0,0))
        else:
            self.surf.fill((255,0,0))
        self.rect=self.surf.get_rect(center=(randint(0.12*largeuréc,0.87*largeuréc),randint (50,hauteuréc)))

class Txt(sprite.Sprite):
    def __init__(self,img,pos):
        super (Txt,self).__init__()
        self.ran=randint(0,3)
        self.image = image.load(img).convert()
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.mask =mask.from_surface( self.image )
        self.rect=self.image.get_rect(center=pos)

class Player(sprite.Sprite):
    def __init__(self,position,clr,numpl):
        super(Player, self).__init__()
        self.ready=0
        self.listeperso=["luffy","mariopixel","goku","luigi","dracofeu","bouteille_de_pont","chat","N'Golo_Kanté"]
        self.pret=0
        self.bonus=[1,1,0]
        self.clr=clr
        self.capa=0
        self.perso=0
        self.posdep=position
        self.vitesse=3
        self.numpl=numpl
        self.vie=100
        self.bdv=Barre_de_vie(self.numpl,self)
        Bdv.add(self.bdv)
        self.bdm=Barre_de_mana(self.numpl,self)
        Bdm.add(self.bdm)
        self.fdbv=Fond_de_barre(self,10)
        fdbm=Fond_de_barre(self,30)
        all_sprites.add(fdbm,self.fdbv,self.bdm,self.bdv)

        if self.numpl==1:
            self.keys=[K_UP,K_DOWN,K_LEFT,K_RIGHT,K_SPACE]#[K_KP8,K_KP2,K_KP4,K_KP6,K_KP0]
            self.dir='lt'
            self.image = image.load(self.listeperso[self.perso]+"3.png").convert()
            self.image.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect=self.image.get_rect(center=self.posdep)

        else:
            self.keys=[K_w,K_s,K_a,K_d,K_v]
            self.dir='rt'
            self.image = image.load(self.listeperso[self.perso]+"1.png").convert()
            self.image.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect=self.image.get_rect(center=self.posdep)

    def update(self,pressed_keys,jeu):
        if jeu==1:
            if pressed_keys[self.keys[0]]:
                self.rect.move_ip(0, -self.vitesse)
                if self.rect.top <= 0:
                    self.rect.top = 0
            if pressed_keys[self.keys[1]]:
                self.rect.move_ip(0, self.vitesse)
                if self.rect.bottom >= hauteuréc:
                    self.rect.bottom = hauteuréc
            if pressed_keys[self.keys[2]]:
                self.rect.move_ip(-self.vitesse, 0)
                if self.rect.left < 0:
                    self.rect.left = 0
                self.dir='lt'
                self.image = image.load(self.listeperso[self.perso]+"3.png").convert()
                self.image.set_colorkey((255, 255, 255), RLEACCEL)
            if pressed_keys[self.keys[3]]:
                self.rect.move_ip(self.vitesse, 0)
                if self.rect.right > largeuréc:
                    self.rect.right =largeuréc
                self.dir='rt'
                self.image = image.load(self.listeperso[self.perso]+"1.png").convert()
                self.image.set_colorkey((255, 255, 255), RLEACCEL)
            if pressed_keys[self.keys[4]]:
                if self.bonus[2]==0:
                    if self.capa>=15:
                        self.bdfeu()
                        self.capa-=15
                else:
                    if self.capa>=35:
                        self.tete_chercheuse()
                        self.capa-=35
        else:
            if self.ready==1:
                screen.blit(self.check.image,self.check.rect)


            if pressed_keys[self.keys[2]]and self.pret>=15 and self.ready==0:
                self.perso-=1
                if self.perso<0:
                    self.perso+=8
                self.pret=0

            if pressed_keys[self.keys[3]] and self.pret>=15 and self.ready==0:
                self.perso+=1
                if self.perso>7:
                    self.perso=0
                self.pret=0

            if self.numpl==1:
                self.image = image.load(self.listeperso[self.perso]+"3.png").convert()
                self.image.set_colorkey((255, 255, 255), RLEACCEL)
                self.rect=self.image.get_rect(center=self.posdep)

            else:
                self.image = image.load(self.listeperso[self.perso]+"1.png").convert()
                self.image.set_colorkey((255, 255, 255), RLEACCEL)
                self.rect=self.image.get_rect(center=self.posdep)

            if pressed_keys[self.keys[4]] and self.pret>=20:
                if self.ready==1:
                    self.ready=0
                    self.check.kill()
                elif self.ready==0:
                    self.ready=1
                    self.check=Txt("check.png",(largeuréc/2,hauteuréc/2))
                    self.check.rect=self.image.get_rect(center=((self.posdep[0]-20,self.posdep[1]-45)))
                self.pret=0
            self.pret+=1

    def bdfeu(self):
        nvbdf=Bdf(self)
        if self.numpl==1:
            bdf1.add(nvbdf)
        else:
            bdf2.add(nvbdf)
            team2.add(nvbdf)
        all_sprites.add(nvbdf)
    def tete_chercheuse(self):
        nvtc=Tete_chercheuse(self)
        if self.numpl==1:
            bdf1.add(nvtc)
        else:
            bdf2.add(nvtc)
            team2.add(nvtc)
        all_sprites.add(nvtc)

class Bdf (sprite.Sprite):
    def __init__(self,pl):
        super (Bdf, self).__init__()
        self.surf=Surface((5,5))
        self.surf.fill(pl.clr)
        (x,y,z,w)=(pl.rect)
        self.rect=self.surf.get_rect(center=(x+(z/2),y+(w/2)))
        self.pl=pl
        mixer.music.load("son2.mp3")
        mixer.music.play(loops=1)
        self.num=self.pl.dir
        self.sp=self.pl.bonus[1]
        if self.num=='rt':
            self.num=1
        else:
            self.num=-1
    def update(self):
        self.rect.move_ip(self.num*2*self.sp,0)
        if self.rect.right*self.num >(largeuréc/2+largeuréc/2*self.num):
            self.kill()

class Tete_chercheuse (sprite.Sprite):
    def __init__(self,pl):
        super (Tete_chercheuse,self).__init__()
        self.surf=Surface((5,5))
        self.surf.fill(pl.clr)
        (x,y,z,w)=(pl.rect)
        self.rect=self.surf.get_rect(center=(x+(z/2),y+(w/2)))
        self.pl=pl
        self.num=self.pl.dir
        self.posexact=(self.rect[0],self.rect[1])
        self.compteur=0
        if self.num=='rt':
            self.num=1
        else:
            self.num=-1
    def update(self):
        (x,y,z,w)=self.pl.ennemi.rect
        xba=(self.rect[0]-(x+z/2))
        yba=(self.rect[1]-(y+w/2))
        dist=sqrt(xba**2+yba**2)
        self.posexact=(self.posexact[0]-xba/dist*2,self.posexact[1]-yba/dist*2)
        self.rect=self.surf.get_rect(center=(self.posexact[0],self.posexact[1]))
        self.compteur+=1
        if self.compteur>=500:
            self.kill()



class Barre_de_vie (sprite.Sprite):
    def __init__(self,numpl,pl):
        if numpl==2:
            numpl=-1
        self.ref=pl
        self.numpl=numpl
        super(Barre_de_vie,self).__init__()
        self.surf=Surface((100,10))
        self.surf.fill((int((100-self.ref.vie)*5.1),255,0))
        self.rect=self.surf.get_rect(center=(largeuréc/2+(largeuréc/4)*self.numpl,10))
    def update(self):
        self.surf=Surface((self.ref.vie,10))
        if self.ref.vie>=50:
            self.surf.fill((int((100-self.ref.vie)*5.1),255,0))
        elif self.ref.vie>0:
            self.surf.fill((255,int(self.ref.vie*5.1),0))
        else:
            self.surf.fill((0,255,0))

class Barre_de_mana (sprite.Sprite):
    def __init__(self,numpl,pl):
        if numpl==2:
            numpl=-1
        self.ref=pl
        self.numpl=numpl
        super(Barre_de_mana,self).__init__()
        self.surf=Surface((100,10))
        self.surf.fill((0,255,100))
        self.rect=self.surf.get_rect(center=(0.5*largeuréc+(0.25*largeuréc)*self.numpl,30))
    def update(self):
        self.surf=Surface((self.ref.capa/2,10))
        self.surf.fill((19,166,216))

class Fond_de_barre(sprite.Sprite):
    def __init__(self,pl,hauteur):
        self.ref=pl
        if self.ref.numpl==2:
            self.numpl=-1
        else:
            self.numpl=self.ref.numpl
        super(Fond_de_barre,self).__init__()
        self.surf=Surface((110,20))
        self.surf.fill(self.ref.clr)
        self.rect=self.surf.get_rect(center=(0.5*largeuréc+(0.25*largeuréc)*self.numpl,hauteur))

clock = time.Clock()
ADDbonus=USEREVENT+1
time.set_timer(ADDbonus,7500)
score1=0
score2=0
replay=Txt("message.png",(largeuréc/2,hauteuréc/2))
Bdv=sprite.Group()
Bdm=sprite.Group()
all_sprites =sprite.Group()
Joueurs=sprite.Group()
Bdv=sprite.Group()
Bdm=sprite.Group()
all_sprites =sprite.Group()
tiret=Txt("tiret.png",(largeuréc/2,20))
def try_again():
    global ADDbonus,Bdv,Bdm,all_sprites,joueur1,joueur2,team1,team2,bdf1,bdf2,bnus,clock,bn,Bns,running,run2,affscore1,affscore2
    for entity in Joueurs:
        entity.kill()
        for entity in all_sprites:
            entity.kill()

    joueur2=Player((0.125*largeuréc,0.5*hauteuréc),(184,29,222),2)
    joueur1=Player((0.875*largeuréc,0.5*hauteuréc),(29,222,84),1)
    joueur1.ennemi=joueur2
    joueur2.ennemi=joueur1

    Joueurs.add(joueur2)
    Joueurs.add(joueur1)

    team1=sprite.Group()
    team1.add(joueur1)
    bdf1=sprite.Group()

    team2=sprite.Group()
    team2.add(joueur2)
    bdf2=sprite.Group()
    Bns=sprite.GroupSingle()


    bn=Bonus()
    Bns.add(bn)
    all_sprites.add(bn)


    ready=Txt("ready.png",(largeuréc/2,hauteuréc/2))
    clav=Txt("clavier.png",(largeuréc/2,hauteuréc/2))
    affscore1=Txt("point"+str(score1)+".png",(largeuréc/2+score1*11+12,20))
    affscore2=Txt("point"+str(score2)+".png",(largeuréc/2-score2*11-12,20))
    menu=True
    while menu:
        for evt in event.get():

            if evt.type == QUIT:
                running,menu,run2 = False,False,False
        screen.blit(bg,(0,0))
        touches=key.get_pressed()

        joueur1.update(touches,0)
        joueur2.update(touches,0)
        screen.blit(joueur1.image, joueur1.rect)
        screen.blit(joueur2.image, joueur2.rect)
        screen.blit(ready.image,ready.rect)
        screen.blit(clav.image,clav.rect)
        clock.tick(100)
        display.flip()
        if joueur1.ready+joueur2.ready==2:
            menu=False

try_again()

while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
        elif evt.type==ADDbonus:
            joueur1.bonus=[1,1,0]
            joueur2.bonus=[1,1,0]
            all_sprites.remove(bn)
            bn=Bonus()
            Bns.add(bn)
            all_sprites.add(bn)
    screen.blit(bg,(0,0))
    screen.blit(affscore1.image,affscore1.rect)
    screen.blit(affscore2.image,affscore2.rect)
    screen.blit(tiret.image,tiret.rect)

    touches=key.get_pressed()

    for entity in all_sprites:
        entity.update()
        screen.blit(entity.surf, entity.rect)

    for entity in Joueurs:
        entity.update(touches,1)
        screen.blit(entity.image,entity.rect)

    if sprite.spritecollide(joueur1,bdf2,True):
        joueur1.vie-=10
        if joueur1.vie<=0:
            screen.blit(joueur1.fdbv.surf,joueur1.fdbv.rect)
            win=Txt("player 2 wins.png",((largeuréc/2,hauteuréc/4)))
            score2+=1
            screen.blit(win.image,win.rect)
            print('joueur 1 perd !',score2,"-",score1)
            run2=False
    if sprite.spritecollide(joueur2,bdf1,True):
        joueur2.vie-=10
        if joueur2.vie<=0:
            screen.blit(joueur2.fdbv.surf,joueur2.fdbv.rect)
            win=Txt("player 1 wins.png",(largeuréc/2,hauteuréc/4))
            score1+=1
            screen.blit(win.image,win.rect)
            print('joueur 2 perd !',score2,"-",score1)
            run2=False
    joueur1.capa+=0.5*joueur1.bonus[0]
    if joueur1.capa>200:
        joueur1.capa=200
    joueur2.capa+=0.5*joueur2.bonus[0]
    if joueur2.capa>200:
        joueur2.capa=200

    if sprite.spritecollide(joueur1,Bns,True):
        if bn.ran==1:
            joueur1.bonus=[2,1,0]
        elif bn.ran==0:
            joueur1.vie+=30
            if joueur1.vie>100:
                joueur1.vie=100
        elif bn.ran==2:
            joueur1.bonus=[1,1,1]
        else:
            joueur1.bonus=[1,1.5,0]
        bnus=0
    if sprite.spritecollide(joueur2,Bns,True):
        if bn.ran==1:
            joueur2.bonus=[2,1.,0]
        elif bn.ran==0:
            joueur2.vie+=30
            if joueur2.vie>100:
                joueur2.vie=100
        elif bn.ran==2:
            joueur2.bonus=[1,1,1]
        else:
            joueur2.bonus=[1,1.5,0]

        bnus=0
    clock.tick(100)
    display.flip()

    if run2==False:
        touche2=touches
        if score1==8:
            print ('joueur 1 gagne la partie !',score2,'- 8')
            running=False
        elif score2==8:
            print('joueur 2 gagne la partie ! 8 -',score1)
            running=False
        while not (touche2[K_n] or  touche2[K_o] or running==False) :
            for evt in event.get():
                if evt.type == QUIT:
                    running = False
            touche2=key.get_pressed()

            screen.blit(replay.image,replay.rect)

            clock.tick(100)
            display.flip()
        if touche2[K_n]:
            running=False
        if touche2[K_o]:
            try_again()
            run2=True
quit()
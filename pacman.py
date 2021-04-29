import pygame
import random
import time
pygame.init()

font = pygame.font.SysFont('Calibri', 25, True, False)
font2 = pygame.font.SysFont('Calibri', 45, True, False)
size=(800,600)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
pacman_1 = pygame.image.load("pacman_1.png")
pacman_3r = pygame.image.load("pacman_3r.png")
pacman_3l = pygame.image.load("pacman_3l.png")
pacman_3u = pygame.image.load("pacman_3u.png")
pacman_3d = pygame.image.load("pacman_3d.png")
duch_1d = pygame.image.load("duch_1d.png")
duch_1u = pygame.image.load("duch_1u.png")
duch_1l = pygame.image.load("duch_1l.png")
duch_1r = pygame.image.load("duch_1r.png")
duch_2d = pygame.image.load("duch_2d.png")
duch_2u = pygame.image.load("duch_2u.png")
duch_2l = pygame.image.load("duch_2l.png")
duch_2r = pygame.image.load("duch_2r.png")
duch_3d = pygame.image.load("duch_3d.png")
duch_3u = pygame.image.load("duch_3u.png")
duch_3l = pygame.image.load("duch_3l.png")
duch_3r = pygame.image.load("duch_3r.png")
duch_4d = pygame.image.load("duch_4d.png")
duch_4u = pygame.image.load("duch_4u.png")
duch_4l = pygame.image.load("duch_4l.png")
duch_4r = pygame.image.load("duch_4r.png")
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pacman")
muz_start = pygame.mixer.Sound("pacman_beginning.wav")
muz_nom = pygame.mixer.Sound("pacman_chomp.wav")
muz_bonus = pygame.mixer.Sound("pacman_eatfruit.wav")
muz_smierc = pygame.mixer.Sound("pacman_death.wav")
muz_duchsm = pygame.mixer.Sound("pacman_eatghost.wav")
muz_zyc = pygame.mixer.Sound("pacman_extrapac.wav")
done=False
clock = pygame.time.Clock()

aktorzy = pygame.sprite.Group()
duchy = pygame.sprite.Group()
punkty = pygame.sprite.Group()
bonusy = pygame.sprite.Group()
wynik = 0
poziom = 1
poczatek = True
dod_z = 0

class plytka:

    def __init__(self,x,y):
        self.pozx = x
        self.pozy = y
        self.sizex = 40
        self.sizey = 40
        self.sciany = [0,0,0,0]
        self.st = 0
        self.spawn = False
        self.dost = False

    def up_st(self):
        self.st = self.sciany[0] + self.sciany[1] + self.sciany[2] + self.sciany[3]

plt = []
def init_map():
    del plt[:]
    for j in range(0,13):
        for i in range(0,15):
            pn = plytka(100+40*i,60+40*j)
            plt.append(pn)
init_map()

class punkt(pygame.sprite.Sprite):
    def __init__(self,n):
        super().__init__()
        self.pozn = n
        self.image = pygame.Surface([3,3])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = plt[self.pozn].pozx + 20
        self.rect.y = plt[self.pozn].pozy + 20

class bonus(pygame.sprite.Sprite):
    def __init__(self,n):
        super().__init__()
        self.pozn = n
        self.image = pygame.Surface([7,7])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

class Wierzcholek:
    def __init__(self,n):
        self.pozn = n
        self.sasiedzi = []
        self.odl = -1
        self.prev = None

    def nowy_sasiad(self,wier):
        self.sasiedzi.append(wier)

    def jacy_sasiedzi(self):
        return self.sasiedzi

def wyznacz_drogi(wierz):
    if wierz is None:
        return

    kolejka = []
    kolejka.insert(0,wierz)
    while kolejka:
        wier_n = kolejka.pop(0)
        odl = wier_n.odl + 1
        for sasiad in wier_n.jacy_sasiedzi():
            if sasiad.odl == -1 or sasiad.odl > odl:
                sasiad.odl = odl
                sasiad.prev = wier_n
                kolejka.insert(0,sasiad)

def wybierz_droge(cel,pozn):
    droga = []
    while cel.prev != None:
        if cel.prev.pozn == pozn:
            break
        droga.append(cel.pozn)
        cel = cel.prev
    return cel.pozn

wier = []
def reset_grafu():
    if len(wier) == 0:
        for i in range(0,195):
            nowy_w = Wierzcholek(i)
            wier.append(nowy_w)
        for i in range(0,195):
            if plt[i].sciany[0] == 0:
                wier[i].nowy_sasiad(wier[i-15])
            if plt[i].sciany[1] == 0:
                wier[i].nowy_sasiad(wier[i+1])
            if plt[i].sciany[2] == 0:
                wier[i].nowy_sasiad(wier[i+15])
            if plt[i].sciany[3] == 0:
                wier[i].nowy_sasiad(wier[i-1])
    else:
        for i in range(0,195):
            wier[i].odl = -1
            wier[i].prev = None


class aktor(pygame.sprite.Sprite):
    def __init__(self,n,zycia,isplayer,img):
        super().__init__()
        self.pozn = n
        self.ruch_k = -1
        self.zycia = zycia
        self.isplayer = isplayer
        self.image = pygame.Surface([30,30])
        self.tag = img
        if img == "duch1":
            self.image = duch_1d
        if img == "pacman":
            self.image = pacman_1
        if img == "duch2":
            self.image = duch_2d
        if img == "duch3":
            self.image = duch_3d
        if img == "duch4":
            self.image = duch_4d
        self.rect = self.image.get_rect()
        self.bonus = 0
        self.ochrona = 0
        self.klatka = 0
        self.etap = 0

    def ruch(self):
        if self.rect.x < plt[self.pozn].pozx + 5:
            self.rect.x += 1
        if self.rect.x > plt[self.pozn].pozx + 5:
            self.rect.x -= 1
        if self.rect.y < plt[self.pozn].pozy + 5:
            self.rect.y += 1
        if self.rect.y > plt[self.pozn].pozy + 5:
            self.rect.y -= 1

    def pozn_zmiana(self):
        if not self.isplayer:
            if self.rect.x == plt[self.pozn].pozx + 5 and self.rect.y == plt[self.pozn].pozy + 5:
                wyznacz_drogi(wier[self.pozn])
                if wier[player.pozn].odl < 2:
                    celn = wybierz_droge(wier[player.pozn], self.pozn)
                    if celn - 1 == self.pozn:
                        self.ruch_k = 1
                    if celn - 15 == self.pozn:
                        self.ruch_k = 2
                    if celn + 1 == self.pozn:
                        self.ruch_k = 3
                    if celn + 15 == self.pozn:
                        self.ruch_k = 0
                elif wier[player.pozn].odl < 4:
                    p = random.randint(0,1)
                    if p == 0:
                        celn = wybierz_droge(wier[player.pozn], self.pozn)
                        if celn - 1 == self.pozn:
                            self.ruch_k = 1
                        if celn - 15 == self.pozn:
                            self.ruch_k = 2
                        if celn + 1 == self.pozn:
                            self.ruch_k = 3
                        if celn + 15 == self.pozn:
                            self.ruch_k = 0
                    else:
                        self.ruch_k = random.randint(0,3)
                elif wier[player.pozn].odl < 7:
                    p = random.randint(0, 5)
                    if p == 0:
                        celn = wybierz_droge(wier[player.pozn], self.pozn)
                        if celn - 1 == self.pozn:
                            self.ruch_k = 1
                        if celn - 15 == self.pozn:
                            self.ruch_k = 2
                        if celn + 1 == self.pozn:
                            self.ruch_k = 3
                        if celn + 15 == self.pozn:
                            self.ruch_k = 0
                    else:
                        self.ruch_k = random.randint(0, 3)
                else:
                    self.ruch_k = random.randint(0,3)
                reset_grafu()
        if self.rect.x == plt[self.pozn].pozx + 5 and self.rect.y == plt[self.pozn].pozy + 5:
            if self.ruch_k == 0:
                if plt[self.pozn].sciany[0] != 1:
                    self.pozn -= 15
            if self.ruch_k == 1:
                if plt[self.pozn].sciany[1] != 1:
                    self.pozn += 1
            if self.ruch_k == 2:
                if plt[self.pozn].sciany[2] != 1:
                    self.pozn += 15
            if self.ruch_k == 3:
                if plt[self.pozn].sciany[3] != 1:
                    self.pozn -= 1

    def respawn(self):
        if self.isplayer:
            self.ochrona = 180
            self.zycia -=1
            self.pozn = 67
            self.rect.x = plt[self.pozn].pozx + 5
            self.rect.y = plt[self.pozn].pozy + 5
        else:
            t = random.randint(0,2)
            self.pozn = 96 +t
            self.rect.x = plt[self.pozn].pozx + 5
            self.rect.y = plt[self.pozn].pozy + 5

    def animuj(self):
        if self.isplayer:
            if self.etap == 0:
                self.image = pacman_1
            else:
                if self.ruch_k == 0:
                    self.image = pacman_3u
                if self.ruch_k == 1:
                    self.image = pacman_3r
                if self.ruch_k == 2:
                    self.image = pacman_3d
                if self.ruch_k == 3:
                    self.image = pacman_3l
            self.klatka += 1
            if self.klatka == 30:
                self.etap += 1
                self.klatka = 0
            if self.etap == 2:
                self.etap = 0
        else:
            if self.tag == "duch1":
                if self.ruch_k == 0:
                    self.image = duch_1u
                if self.ruch_k == 1:
                    self.image = duch_1r
                if self.ruch_k == 2:
                    self.image = duch_1d
                if self.ruch_k == 3:
                    self.image = duch_1l
            if self.tag == "duch2":
                if self.ruch_k == 0:
                    self.image = duch_2u
                if self.ruch_k == 1:
                    self.image = duch_2r
                if self.ruch_k == 2:
                    self.image = duch_2d
                if self.ruch_k == 3:
                    self.image = duch_2l
            if self.tag == "duch3":
                if self.ruch_k == 0:
                    self.image = duch_3u
                if self.ruch_k == 1:
                    self.image = duch_3r
                if self.ruch_k == 2:
                    self.image = duch_3d
                if self.ruch_k == 3:
                    self.image = duch_3l
            if self.tag == "duch4":
                if self.ruch_k == 0:
                    self.image = duch_4u
                if self.ruch_k == 1:
                    self.image = duch_4r
                if self.ruch_k == 2:
                    self.image = duch_4d
                if self.ruch_k == 3:
                    self.image = duch_4l



player = aktor(67,3,True,"pacman")
player.rect.x = plt[player.pozn].pozx+5
player.rect.y = plt[player.pozn].pozy+5
aktorzy.add(player)

duch1 = aktor(32,999,False,"duch1")
duch1.rect.x = plt[duch1.pozn].pozx+5
duch1.rect.y = plt[duch1.pozn].pozy+5
aktorzy.add(duch1)
duchy.add(duch1)

duch2 = aktor(42,999,False,"duch2")
duch2.rect.x = plt[duch2.pozn].pozx+5
duch2.rect.y = plt[duch2.pozn].pozy+5
aktorzy.add(duch2)
duchy.add(duch2)

duch3 = aktor(152,999,False,"duch3")
duch3.rect.x = plt[duch3.pozn].pozx+5
duch3.rect.y = plt[duch3.pozn].pozy+5
aktorzy.add(duch3)
duchy.add(duch3)

duch4 = aktor(162,999,False,"duch4")
duch4.rect.x = plt[duch4.pozn].pozx+5
duch4.rect.y = plt[duch4.pozn].pozy+5
aktorzy.add(duch4)
duchy.add(duch4)

do_spr = []
def spr_d(n):
    plt[n].dost = True
    if plt[n].sciany[0] == 0:
        if not plt[n - 15].dost:
            do_spr.append(n-15)
    if plt[n].sciany[1] == 0:
        if not plt[n + 1].dost:
            do_spr.append(n+1)
    if plt[n].sciany[2] == 0:
        if not plt[n + 15].dost:
            do_spr.append(n+15)
    if plt[n].sciany[3] == 0:
        if not plt[n-1].dost:
            do_spr.append(n-1)
    while do_spr:
        spraw = do_spr.pop(0)
        if not plt[spraw].dost:
            spr_d(spraw)


def mapgen():
    init_map()
    del wier[:]
    punkty.empty()
    bonusy.empty()
    for i in range(0,15):
        plt[i].sciany[0]=1
    for i in range(0,15):
        plt[i+(15*12)].sciany[2]=1
    for i in range(0,13):
        plt[15*i].sciany[3]=1
    for i in range(0,13):
        plt[15*i+14].sciany[1]=1
    plt[81].sciany[2]=1
    plt[82].sciany[2]=1
    plt[83].sciany[2]=1
    plt[95].sciany[1]=1
    plt[96].sciany[0]=1
    plt[96].sciany[3]=1
    plt[96].sciany[2]=1
    plt[97].sciany[0]=1
    plt[98].sciany[0]=1
    plt[98].sciany[1]=1
    plt[98].sciany[2]=1
    plt[99].sciany[3]=1
    plt[111].sciany[0]=1
    plt[112].sciany[0]=1
    plt[113].sciany[0]=1
    plt[96].spawn = True
    plt[97].spawn = True
    plt[98].spawn = True
    for i in range(0,195):
        plt[i].up_st()
    for i in range(0,195):
        if plt[i].spawn == False and plt[i].st < 2:
            n = random.randint(0,5)
            if n == 0:
                if i == 112:
                    continue
                if i-15 >= 0 :
                    if plt[i-15].st < 2:
                        plt[i].sciany[0] = 1
                        plt[i-15].sciany[2] = 1
                        plt[i].up_st()
                        plt[i-15].up_st()
            if n == 1:
                if i%15 != 14:
                    if plt[i+1].st < 2:
                        plt[i].sciany[1] = 1
                        plt[i+1].sciany[3] = 1
                        plt[i].up_st()
                        plt[i+1].up_st()
            if n == 2:
                if i+15 < 195:
                    if plt[i+15].st < 2:
                        plt[i].sciany[2] = 1
                        plt[i+15].sciany[0] = 1
                        plt[i].up_st()
                        plt[i+15].up_st()
            if n == 3:
                if i%15 != 0:
                    if plt[i-1].st < 2:
                        plt[i].sciany[3] = 1
                        plt[i-1].sciany[1] = 1
                        plt[i].up_st()
                        plt[i-1].up_st()
    for i in range(0,195):
        if plt[i].spawn == False and plt[i].st < 2:
            n = random.randint(0,3)
            if n == 0:
                if i == 112:
                    continue
                if i-15 >= 0 :
                    if plt[i-15].st < 2:
                        plt[i].sciany[0] = 1
                        plt[i-15].sciany[2] = 1
                        plt[i].up_st()
                        plt[i-15].up_st()
            if n == 1:
                if i%15 != 14:
                    if plt[i+1].st < 2:
                        plt[i].sciany[1] = 1
                        plt[i+1].sciany[3] = 1
                        plt[i].up_st()
                        plt[i+1].up_st()
            if n == 2:
                if i+15 < 195:
                    if plt[i+15].st < 2:
                        plt[i].sciany[2] = 1
                        plt[i+15].sciany[0] = 1
                        plt[i].up_st()
                        plt[i+15].up_st()
            if n == 3:
                if i%15 != 0:
                    if plt[i-1].st < 2:
                        plt[i].sciany[3] = 1
                        plt[i-1].sciany[1] = 1
                        plt[i].up_st()
                        plt[i-1].up_st()
    spr_d(112)
    for i in range(0,195):
        if not plt[i].spawn:
            if not plt[i].dost:
                if i-15 >= 0:
                    if plt[i-15].dost:
                        plt[i].sciany[0] = 0
                        plt[i-15].sciany[2] = 0
                        spr_d(i)
                        continue
                if i + 15 <= 194:
                    if plt[i + 15].dost:
                        plt[i].sciany[2] = 0
                        plt[i - 15].sciany[0] = 0
                        spr_d(i)
                        continue
                if i%15 != 0:
                    if plt[i-1].dost:
                        plt[i].sciany[3] = 0
                        plt[i - 1].sciany[1] = 0
                        spr_d(i)
                        continue
                if i%15 != 14:
                    if plt[i + 1].dost:
                        plt[i].sciany[1] = 0
                        plt[i + 1].sciany[3] = 0
                        spr_d(i)
                        continue
    bn_list = []
    for i in range(0,4):
        tx = random.randint(0,4)
        ty = random.randint(0,4)
        if i == 0:
            nn = 15*ty + tx
        if i == 1:
            nn = 15*ty + tx +10
        if i == 2:
            nn = 15 * (ty+8) + tx
        if i == 3:
            nn = 15 * (ty+8) + tx + 10
        bn = bonus(nn)
        bn.rect.x = plt[bn.pozn].pozx + 17
        bn.rect.y = plt[bn.pozn].pozy + 17
        bonusy.add(bn)
        bn_list.append(nn)
    for i in range(0,195):
        if not plt[i].spawn and i != 67 and i not in bn_list:
            pkt = punkt(i)
            punkty.add(pkt)
    del bn_list[:]
    reset_grafu()


while not done:
    if player.zycia <= 0:
        screen.fill(BLACK)
        text_k = font2.render("GAME OVER",True,WHITE)
        screen.blit(text_k,[300,240])
        pygame.display.flip()
        time.sleep(2)
        poziom = 1
        wynik = 0
        dod_z = 0
        poczatek = True
        player.zycia = 3
        player.pozn = 67
        player.rect.x = plt[player.pozn].pozx + 5
        player.rect.y = plt[player.pozn].pozy + 5
        duch1.pozn = 32
        duch1.rect.x = plt[duch1.pozn].pozx + 5
        duch1.rect.y = plt[duch1.pozn].pozy + 5
        duch2.pozn = 42
        duch2.rect.x = plt[duch2.pozn].pozx + 5
        duch2.rect.y = plt[duch2.pozn].pozy + 5
        duch3.pozn = 152
        duch3.rect.x = plt[duch3.pozn].pozx + 5
        duch3.rect.y = plt[duch3.pozn].pozy + 5
        duch4.pozn = 162
        duch4.rect.x = plt[duch4.pozn].pozx + 5
        duch4.rect.y = plt[duch4.pozn].pozy + 5
        continue

    if poczatek:
        mapgen()
        poczatek = False
        text_p = font2.render("POZIOM "+str(poziom),True,WHITE)
        screen.fill(BLACK)
        screen.blit(text_p,[325,240])
        pygame.display.flip()
        muz_start.play()
        time.sleep(4)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player.pozn%15 != 0:
                if plt[player.pozn].sciany[3] != 1:
                    player.ruch_k = 3
            elif event.key == pygame.K_RIGHT and player.pozn%15 != 14:
                if plt[player.pozn].sciany[1] != 1:
                    player.ruch_k  = 1
            elif event.key == pygame.K_UP and player.pozn-15 >= 0:
                if plt[player.pozn].sciany[0] != 1:
                    player.ruch_k = 0
            elif event.key == pygame.K_DOWN and player.pozn+15 <= 194:
                if plt[player.pozn].sciany[2] != 1:
                    player.ruch_k = 2
        elif event.type == pygame.KEYUP:
            player.ruch_k = -1

    player.pozn_zmiana()
    duch1.pozn_zmiana()
    duch2.pozn_zmiana()
    duch3.pozn_zmiana()
    duch4.pozn_zmiana()

    screen.fill(BLACK)

    for i in range(0,13*15):
        #pygame.draw.rect(screen,RED,[plt[i].pozx,plt[i].pozy,40,40],1)
        if plt[i].sciany[0] == 1:
            pygame.draw.rect(screen, BLUE, [plt[i].pozx-3, plt[i].pozy-3, 46, 6], 0)
        if plt[i].sciany[1] == 1:
            pygame.draw.rect(screen, BLUE, [plt[i].pozx+37, plt[i].pozy-3, 6, 46], 0)
        if plt[i].sciany[2] == 1:
            pygame.draw.rect(screen, BLUE, [plt[i].pozx-3, plt[i].pozy+37, 46, 6], 0)
        if plt[i].sciany[3] == 1:
            pygame.draw.rect(screen, BLUE, [plt[i].pozx-3, plt[i].pozy-3, 6, 46], 0)
    pygame.draw.rect(screen, RED, [plt[112].pozx, plt[112].pozy - 3, 40, 6], 0)
    text1 = font.render("Wynik: "+str(wynik),True,WHITE)
    text2 = font.render("Zycia: "+str(player.zycia),True,WHITE)
    text3 = font.render("POZIOM "+str(poziom),True,WHITE)
    screen.blit(text1,[0,0])
    screen.blit(text2,[0,40])
    screen.blit(text3,[350,0])

    zd_bon = pygame.sprite.spritecollide(player,bonusy,True)
    if zd_bon:
        player.bonus = 720
    zd_duch = pygame.sprite.spritecollide(player,duchy,False)
    if zd_duch:
        if player.bonus > 0:
            wynik += 25
            muz_duchsm.play()
            zd_duch[0].respawn()
        elif player.ochrona == 0:
            muz_smierc.play()
            time.sleep(1)
            player.respawn()
    zd_pkt = pygame.sprite.spritecollide(player,punkty,True)
    if zd_bon:
        wynik += 10
        muz_bonus.play()
    if zd_pkt:
        wynik += 1
    if wynik//150 > dod_z:
        dod_z = wynik//150
        player.zycia += 1
        muz_zyc.play()
    if player.bonus > 0:
        pygame.draw.rect(screen, GREEN, [500, 0 , 10, 10], 0)
        player.bonus -= 1
    if player.ochrona > 0:
        pygame.draw.rect(screen, BLUE, [510, 0 , 10, 10], 0)
        player.ochrona -= 1

    player.ruch()
    player.animuj()
    duch1.ruch()
    duch1.animuj()
    duch2.ruch()
    duch2.animuj()
    duch3.ruch()
    duch3.animuj()
    duch4.ruch()
    duch4.animuj()

    bonusy.draw(screen)
    punkty.draw(screen)
    aktorzy.draw(screen)

    if not punkty:
        poczatek = True
        poziom +=1
        player.pozn = 67
        player.rect.x = plt[player.pozn].pozx + 5
        player.rect.y = plt[player.pozn].pozy + 5
        duch1.pozn = 32
        duch1.rect.x = plt[duch1.pozn].pozx + 5
        duch1.rect.y = plt[duch1.pozn].pozy + 5
        duch2.pozn = 42
        duch2.rect.x = plt[duch2.pozn].pozx + 5
        duch2.rect.y = plt[duch2.pozn].pozy + 5
        duch3.pozn = 152
        duch3.rect.x = plt[duch3.pozn].pozx + 5
        duch3.rect.y = plt[duch3.pozn].pozy + 5
        duch4.pozn = 162
        duch4.rect.x = plt[duch4.pozn].pozx + 5
        duch4.rect.y = plt[duch4.pozn].pozy + 5

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
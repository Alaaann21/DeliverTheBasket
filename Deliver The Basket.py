import pygame as pg
import sys
from random import randint
from datetime import datetime
from math import sin, radians, sqrt


class RadioButton:
    '''RadioButton: Clase usada para generar un área circular que puede ser seleccionable'''

    def __init__(self, posX, posY):
        '''__init__: Constructor de la clase RadioButton'''
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.count = 0

    def keyEvent(self, event, listName, index):
        '''keyEvent: Función que realiza una acción cuando se pulse sobre el área circular'''
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.border.collidepoint(event.pos):
                if (self.count == 0):
                    sounds['toSelect'].play()
                    self.count = 1
                if (listName == "difficulty"):
                    difficulty[index] = True
                    difficulty[0 if index == 1 else 1] = False
                else:
                    mode[index] = True
                    mode[0 if index == 1 else 1] = False
        elif event.type == pg.MOUSEBUTTONUP:
            if self.border.collidepoint(event.pos):
                self.count = 0

    def update(self, listName, index):
        '''update: Función que mantiene actualizado el estado del área circular'''
        if (listName == "difficulty"):
            self.border = pg.draw.circle(
                screen, colors['active'] if difficulty[index] else colors['inactive'], (self.posX, self.posY), 13, 2)
            self.fill = pg.draw.circle(
                screen, colors['active'], (self.posX, self.posY), 8, 0) if difficulty[index] else None
        else:
            self.border = pg.draw.circle(
                screen, colors['active'] if mode[index] else colors['inactive'], (self.posX, self.posY), 13, 2)
            self.fill = pg.draw.circle(
                screen, colors['active'], (self.posX, self.posY), 8, 0) if mode[index] else None


class InputBox:
    '''IputBox: Clase usado para generar un área rectangular que puede ser pulsado para poder ingresar caracteres'''

    def __init__(self, posX, posY, width, height):
        '''__init__: Contructor del la Clase InputBox'''
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.rect = pg.Rect(self.posX, self.posY, self.width, self.height)
        self.rect.center = (posX, posY-2)
        self.color = colors['inactive']
        self.text = ''
        self.fontInput = pg.font.Font('font/04B_30__.TTF', 30)
        self.inputRender = self.fontInput.render(self.text, True, self.color)
        self.inputRect = self.inputRender.get_rect()
        self.inputRect.center = (posX - 97, posY)
        self.active = False
        self.toSelect = pg.mixer.Sound(sounds['toSelect'])
        self.count = 0

    def keyEvent(self, event):
        '''keyEvent: Función que realiza una acción cuando se pulse sobre el área rectangular'''
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if (self.count == 0):
                    self.toSelect.play()
                self.count = 1
                self.active = not self.active
            else:
                self.active = False
            self.color = colors['active'] if self.active else colors['inactive']
        elif event.type == pg.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.count = 0
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.text = 'Jugador' if self.text == '' else self.text
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key != pg.K_RETURN:
                    self.text += event.unicode
                    if len(self.text) > 20:
                        self.text = self.text[:-1]

    def update(self):
        '''update: Función que mantiene actualizado el tamaño del área rectangular'''
        self.width = max(200, self.inputRender.get_width()+7)
        self.rect.w = self.width

    def draw(self):
        '''draw: Función que dibuja y visualiza el área circular en la ventana'''
        self.inputRender = self.fontInput.render(
            self.text, True, colors['active'])
        screen.blit(self.inputRender, self.inputRect)
        pg.draw.rect(screen, self.color, self.rect, 2)


class MainScreen:
    '''MainScreen: Clase contenedora de los objetos del Menú Principal'''

    def __init__(self):
        '''__init__: Constructor de la clase MainScreen'''
        self.backgroundImage = pg.image.load(images['menuBackground'])
        self.title = pg.image.load(images['titleText'])
        self.playerLateral = pg.image.load(images['playerLateral'])
        self.nameText = pg.image.load(images['nameText'])
        self.difficultyText = pg.image.load(images['difficultyText'])
        self.basicText = pg.image.load(images['basicText'])
        self.advancedText = pg.image.load(images['advancedText'])
        self.modeText = pg.image.load(images['modeText'])
        self.onePlayerText = pg.image.load(images['onePlayerText'])
        self.playerVSCPUText = pg.image.load(images['playerVSCPUText'])

        self.inputBox = InputBox(width/2 + 166/2, 438+16, 200, 32)
        self.listDifficultyRadioButtons = [RadioButton(
            width/2, 438+109.5-31*0.25), RadioButton(width/2, 438+109.5+31*1.25)]
        self.listModeRadioButtons = [RadioButton(
            width/2, 438+109.5*2-31*0.25), RadioButton(width/2, 438+109.5*2+31*1.25)]

    def update(self, event):
        '''update: Función que mantiene actualizado la visualizacion de los objetos del Menú Principal'''
        screen.blit(self.backgroundImage, (0, 0))
        screen.blit(self.title, (width/2-(566/2), 0))
        screen.blit(self.playerLateral,
                    (width/2-166*1.25-57*1.5, 438-102*0.35))
        screen.blit(self.nameText, (width/2-166*1.25, 438))
        screen.blit(self.difficultyText, (width/2-(240*1.175), 438+109.5))
        screen.blit(self.basicText, (width/2+20, 438+109.5-31*0.25-31/2))
        screen.blit(self.advancedText, (width/2+20, 438+109.5+31*1.25-31/2))
        screen.blit(self.modeText, (width/2-116*1.355, 438+109.5*2))
        screen.blit(self.onePlayerText, (width/2+20, 438+109.5*2-31*0.25-31/2))
        screen.blit(self.playerVSCPUText,
                    (width/2+20, 438+109.5*2+31*1.25-31/2))
        for i in range(2):
            self.listDifficultyRadioButtons[i].keyEvent(event, "difficulty", i)
            self.listDifficultyRadioButtons[i].update("difficulty", i)
            self.listModeRadioButtons[i].keyEvent(event, "mode", i)
            self.listModeRadioButtons[i].update("mode", i)
        self.inputBox.draw()
        self.inputBox.update()


class MapScreen:
    '''MainScreen: Clase contenedora de los objetos del Mapa'''

    def __init__(self):
        '''__init__: Constructor de la clase MapScreen'''
        self.distance = lambda p1, p2: sqrt(
            ((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))
        self.backgroundImage = pg.image.load(
            images['mapBackgroundDay' if 6 <= hour < 18 else 'mapBackgroundNight'])
        self.playerAir = pg.image.load(images['playerAir'])
        self.cpuAir = pg.image.load(images['cpuAir'])
        self.houseOneAir = pg.image.load(images['houseOneAir'])
        self.houseTwoAir = pg.image.load(images['houseTwoAir'])
        self.houseThreeAir = pg.image.load(images['houseThreeAir'])
        self.poolAirOne = pg.image.load(images['poolAir'])
        self.poolAirTwo = pg.image.load(images['poolAir'])
        self.poolAirThree = pg.image.load(images['poolAir'])
        self.poolAirFour = pg.image.load(images['poolAir'])
        self.poolAirFive = pg.image.load(images['poolAir'])

    def update(self):
        '''update: Función que mantiene actualizado la visualizacion de los objetos del Mapa'''
        global updateMap, dictInfo, listCoordinates, mode, difficulty

        if updateMap:
            listCoordinates = randomPos()
            self.player = listCoordinates['player'][0] + \
                17.5, listCoordinates['player'][1] + 30
            self.cpu = listCoordinates['cpu'][0] + \
                17.5, listCoordinates['cpu'][1] + 30
            self.houseOne = listCoordinates['houseOne'][0] + \
                48, listCoordinates['houseOne'][1] + 57
            self.houseTwo = listCoordinates['houseTwo'][0] + \
                48, listCoordinates['houseTwo'][1] + 44.5
            self.houseThree = listCoordinates['houseThree'][0] + \
                58, listCoordinates['houseThree'][1] + 51
            self.poolOne = listCoordinates['poolOne'][0] + \
                50, listCoordinates['poolOne'][1] + 42.5
            self.poolTwo = listCoordinates['poolTwo'][0] + \
                50, listCoordinates['poolTwo'][1] + 42.5
            self.poolThree = listCoordinates['poolThree'][0] + \
                50, listCoordinates['poolThree'][1] + 42.5
            self.poolFour = listCoordinates['poolFour'][0] + \
                50, listCoordinates['poolFour'][1] + 42.5
            self.poolFive = listCoordinates['poolFive'][0] + \
                50, listCoordinates['poolFive'][1] + 42.5

            dictInfo = {
                'playerHouseOne': [],
                'playerHouseTwo': [],
                'playerHouseThree': [],
                'cpuHouseOne': [],
                'cpuHouseTwo': [],
                'cpuHouseThree': [],
            }

            updateMap = False

        self.linePlayerHouseOne = pg.draw.line(
            screen, colors['white'], self.player, self.houseOne, 1)
        self.linePlayerHouseTwo = pg.draw.line(
            screen, colors['white'], self.player, self.houseTwo, 1)
        self.linePlayerHouseTree = pg.draw.line(
            screen, colors['white'], self.player, self.houseThree, 1)
        self.lineCpuHouseOne = pg.draw.line(
            screen, colors['red'], self.cpu, self.houseOne, 1)
        self.lineCpuHouseTwo = pg.draw.line(
            screen, colors['red'], self.cpu, self.houseTwo, 1)
        self.lineCpuHouseThree = pg.draw.line(
            screen, colors['red'], self.cpu, self.houseThree, 1)

        screen.blit(self.backgroundImage, (0, 0))
        screen.blit(self.playerAir, listCoordinates['player'])
        screen.blit(self.houseOneAir, listCoordinates['houseOne'])
        screen.blit(self.houseTwoAir, listCoordinates['houseTwo'])
        screen.blit(self.houseThreeAir, listCoordinates['houseThree'])

        for key in dictInfo.keys():
            if len(dictInfo[key]) == 0:
                dictInfo[key].append(self.distance(self.player if 'player' in key else self.cpu,
                                                   self.houseOne if 'One' in key else self.houseTwo if 'Two' in key else self.houseThree))

        if mode[1]:
            screen.blit(self.cpuAir, listCoordinates['cpu'])

        if difficulty[1]:
            self.rectpoolAirOne = self.poolAirOne.get_rect()
            self.rectpoolAirOne.center = self.poolOne
            self.rectpoolAirTwo = self.poolAirTwo.get_rect()
            self.rectpoolAirTwo.center = self.poolTwo
            self.rectpoolAirThree = self.poolAirThree.get_rect()
            self.rectpoolAirThree.center = self.poolThree
            self.rectpoolAirFour = self.poolAirFour.get_rect()
            self.rectpoolAirFour.center = self.poolFour
            self.rectpoolAirFive = self.poolAirFive.get_rect()
            self.rectpoolAirFive.center = self.poolFive

            screen.blit(self.poolAirOne, self.rectpoolAirOne)
            screen.blit(self.poolAirTwo, self.rectpoolAirTwo)
            screen.blit(self.poolAirThree, self.rectpoolAirThree)
            screen.blit(self.poolAirFour, self.rectpoolAirFour)
            screen.blit(self.poolAirFive, self.rectpoolAirFive)

            i = 0
            rectPool = [self.rectpoolAirOne, self.rectpoolAirTwo,
                        self.rectpoolAirThree, self.rectpoolAirFour, self.rectpoolAirFive]
            lines = [self.linePlayerHouseOne, self.linePlayerHouseTwo, self.linePlayerHouseTree,
                     self.lineCpuHouseOne, self.lineCpuHouseTwo, self.lineCpuHouseThree]
            for key in dictInfo.keys():
                house = self.houseOne if i == 0 else self.houseTwo if i == 1 else self.houseThree
                if len(dictInfo[key]) == 1 and 'player' in key:
                    for e in range(len(rectPool)):
                        if lines[i].colliderect(rectPool[e]):
                            pool = self.poolOne if e == 0 else self.poolTwo if e == 1 else self.poolThree if e == 2 else self.poolFour if e == 3 else self.poolFive
                            collision = collide(self.player, house, pool)
                            posPool = house[0] + \
                                collision[1][0], house[1] + collision[1][1]
                            if collision[0]:
                                dictInfo[key].append(
                                    self.distance(house, posPool))
                if mode[1] and len(dictInfo[key]) == 1 and 'cpu' in key:
                    for e in range(len(rectPool)):
                        if lines[i + 3].colliderect(rectPool[e]):
                            pool = self.poolOne if e == 0 else self.poolTwo if e == 1 else self.poolThree if e == 2 else self.poolFour if e == 3 else self.poolFive
                            collision = collide(self.cpu, house, pool)
                            posPool = house[0] + \
                                collision[1][0], house[1] + collision[1][1]
                            if collision[0]:
                                dictInfo[key].append(
                                    self.distance(house, posPool))
                if i == 2:
                    i = 0
                else:
                    i += 1

        if screenSelect['mapResult'][0]:
            for i in range(3):
                vPH = (self.houseOne if i == 0 else self.houseTwo if i == 1 else self.houseThree)[
                    0] - self.player[0], (self.houseOne if i == 0 else self.houseTwo if i == 1 else self.houseThree)[1] - self.player[1]
                vPHNorm = vPH[0]/sqrt(vPH[0]**2 + vPH[1]
                                      ** 2), vPH[1]/sqrt(vPH[0]**2 + vPH[1]**2)
                for e in data[i]:
                    markDistance = vPHNorm[0] * e, vPHNorm[1] * e
                    markDistance = self.player[0] + \
                        markDistance[0], self.player[1] + markDistance[1]
                    pg.draw.line(screen, (0, 0, 255), self.player,
                                 markDistance, 1) if e == max(data[i]) else None
                    pg.draw.line(screen, [(176, 46, 193), (193, 186, 46), (255, 255, 255)][i], (
                        markDistance[0] - 10, markDistance[1] - 10), (markDistance[0] + 10, markDistance[1] + 10), 5)
                    pg.draw.line(screen, [(176, 46, 193), (193, 186, 46), (255, 255, 255)][i], (
                        markDistance[0] + 10, markDistance[1] - 10), (markDistance[0] - 10, markDistance[1] + 10), 5)
                if mode[1]:
                    vCpuH = (self.houseOne if i == 0 else self.houseTwo if i == 1 else self.houseThree)[
                        0] - self.cpu[0], (self.houseOne if i == 0 else self.houseTwo if i == 1 else self.houseThree)[1] - self.cpu[1]
                    vCpuHNorm = vCpuH[0]/sqrt(vCpuH[0]**2 + vCpuH[1]
                                              ** 2), vCpuH[1]/sqrt(vCpuH[0]**2 + vCpuH[1]**2)
                    for e in dataCpu[i]:
                        markDistance = vCpuHNorm[0] * e, vCpuHNorm[1] * e
                        markDistance = self.cpu[0] + \
                            markDistance[0], self.cpu[1] + markDistance[1]
                        pg.draw.line(screen, (255, 0, 0), self.cpu, markDistance, 1) if e == max(
                            dataCpu[i]) else None
                        pg.draw.line(screen, [(176, 46, 193), (193, 186, 46), (255, 255, 255)][i], (
                            markDistance[0] - 10, markDistance[1] - 10), (markDistance[0] + 10, markDistance[1] + 10), 5)
                        pg.draw.line(screen, [(176, 46, 193), (193, 186, 46), (255, 255, 255)][i], (
                            markDistance[0] + 10, markDistance[1] - 10), (markDistance[0] - 10, markDistance[1] + 10), 5)


class GameScreen:
    '''GameScreen: Clase contenedora de los objetos del escenario del Juego'''

    def __init__(self):
        '''__init__: Constructor de la clase GameScreen'''

        self.listCoordinates = updatePos()
        self.distance = lambda angle, power: (
            (power ** 2) * sin(radians(2 * angle))) / 9.8
        self.player = pg.image.load(images['playerLateral'])
        self.provision = pg.image.load(images['basket'] + 'launching.png')
        self.start = False
        self.counter = 0
        self.attemptsCounter = 3
        self.addAngle = True
        self.angle = 1
        self.addPower = True
        self.power = 1
        self.auxRecovery = 0
        self.poofOpacity = 100
        self.extra = randint(50, 150)
        self.alert = [True, None]
        self.playCpu = True

    def update(self, events):
        '''update: Función que mantiene actualizado la visualizacion del escenario de juego'''
        global timeAux, houseI, listDist, newGame

        if newGame:
            self.data = [False, False]
            newGame = False
        self.sunMoon = pg.image.load(
            images['sun' if 6 <= hour < 18 else 'moon'])
        self.sunMoonRect = self.sunMoon.get_rect()
        self.sunMoonRect.center = (self.listCoordinates[hourAux[hour]][minute])
        self.ground = pg.image.load(
            images['groundDay' if 6 <= hour < 18 else 'groundNight'])
        self.background = pg.image.load(
            images['day' if 6 <= hour < 18 else 'night'])
        self.cloud = pg.image.load(
            images['cloud'] + ('Day.png' if 6 <= hour < 18 else 'Night.png'))
        self.house = pg.image.load(images['houseOneLateral' if houseI ==
                                   0 else 'houseTwoLateral' if houseI == 1 else 'houseThreeLateral'])

        screen.blit(self.background, (0, 0))
        screen.blit(self.sunMoon, self.sunMoonRect)
        screen.blit(self.ground, (0, 649))
        screen.blit(self.player, (22, 585))
        screen.blit(self.cloud, (389, 22))

        self.poolGround = [[], [], []]
        self.poolPosLateral = [[], [], []]
        listDist = dictInfo['playerHouseOne' if houseI ==
                            0 else 'playerHouseTwo' if houseI == 1 else 'playerHouseThree']
        if mode[1]:
            listDistCpu = dictInfo['cpuHouseOne' if houseI ==
                                   0 else 'cpuHouseTwo' if houseI == 1 else 'cpuHouseThree']
            self.poolPosLateralCpu = [[], [], []]
            if len(listDistCpu) != 1:
                for i in listDistCpu[1:]:
                    posX = (((listDistCpu[0]-i)*916.5)/listDistCpu[0]) - 59
                    self.poolPosLateralCpu[houseI].append((posX, posX + 118 + 1))
        if len(listDist) != 1:
            for i in listDist[1:]:
                self.poolGround[houseI].append(pg.image.load(images['poolGround']))
                posX = (((listDist[0]-i)*916.5)/listDist[0]) - 59
                self.poolPosLateral[houseI].append((posX, posX + 118 + 1))
                screen.blit(self.poolGround[houseI][-1], (posX, 682))

        if self.counter == 61:
            if self.timeOutCont != 5:
                if self.timeOutCont != round(pg.time.get_ticks()/1000) - self.auxRecovery:
                    self.timeOutCont += 1
                pg.mixer.music.stop()
                self.timeOut = pg.image.load(images['timeOut'])
                self.poofOpacity = 100
                self.start = False
                self.seconds = pg.image.load(
                    images['second'] + ('00.png' if 60 - self.counter >= 10 else '00.png'))
                screen.blit(self.timeOut, (281.5, 349.5))
            else:
                self.attemptsCounterCpu = self.attemptsCounter
                while (self.attemptsCounter != 0):
                    data[houseI].append(
                        self.distance(randint(20, 60), (sqrt((9.8*(listDist[0] + self.extra))/sin(radians(2*45)))/8) * randint(4, 8)))
                    distanceLateral[houseI].append(
                        (data[houseI][-1]*916.5)/listDist[0])
                    if True in [(i[0] <= distanceLateral[houseI][-1] <= i[1] if len(i) != 0 else False) for i in self.poolPosLateral[houseI]]:
                        delivered[houseI].append('lost')
                        penalties[houseI].append(5)
                    elif 825 <= distanceLateral[houseI][-1] <= 1006:
                        data[houseI].pop(-1)
                        distanceLateral[houseI].pop(-1)
                        self.attemptsCounter += 1
                    else:
                        delivered[houseI].append(False)
                        penalties[houseI].append(0)
                    self.attemptsCounter -= 1

                if mode[1] and self.playCpu:
                    while (self.attemptsCounterCpu != 0):
                        dataCpu[houseI].append(
                            self.distance(randint(20, 60), (sqrt((9.8*(listDistCpu[0] + self.extra))/sin(radians(2*45)))/8) * randint(4, 8)))
                        distanceLateralCpu[houseI].append(
                            (dataCpu[houseI][-1]*916.5)/listDistCpu[0])
                        if True in [(i[0] <= distanceLateralCpu[houseI][-1] <= i[1] if len(i) != 0 else False) for i in self.poolPosLateralCpu[houseI]]:
                            deliveredCpu[houseI].append('lost')
                            penaltiesCpu[houseI].append(5)
                        elif 825 <= distanceLateralCpu[houseI][-1] <= 1006:
                            deliveredCpu[houseI].append(True)
                            penaltiesCpu[houseI].append(0)
                            self.playCpu = False
                            self.attemptsCounterCpu = 1
                        else:
                            deliveredCpu[houseI].append(False)
                            penaltiesCpu[houseI].append(0)
                        self.attemptsCounterCpu -= 1
                timeAux += self.timeOutCont + 1
                self.data = [False, False]
                if houseI != 3:
                    houseI += 1
                    self.extra = randint(50, 150)
                self.alert[0] = True
                self.playCpu = True
                self.attemptsCounter = 3
                self.counter = 0
                self.data = [False, False]
                self.angle, self.power = 1, 1
                self.addAngle, self.addPower = True, True

        if self.poofOpacity % 10 == 0:
            self.poof = pg.image.load(images['poof'] + ((f'Day{self.poofOpacity}.png' if 6 <= hour <
                                      18 else f'Night{self.poofOpacity}.png') if self.poofOpacity != 0 else f'{self.poofOpacity}.png'))

        screen.blit(self.house, (877, 478) if houseI == 0 else (
            877, 531) if houseI == 1 else (867, 519))

        screen.blit(self.poof, (776, 437))
        self.game = False in self.data
        if self.game:
            self.launch = 0
            self.auxRecovery = 0
            self.timeOutCont = 0
            self.timeCont = round(pg.time.get_ticks()/1000) - timeAux
            screen.blit(self.provision, (29, 659))
            if self.counter < 1:
                if self.counter == self.timeCont:
                    self.counter += 1
                if self.poofOpacity != 0:
                    self.poofOpacity -= 10
                self.seconds = pg.image.load(images['second'] + '60.png')
            elif self.counter != 61:
                if self.counter == self.timeCont:
                    self.counter += 1
                    self.start = True
                    self.alert[0] = True
                if self.poofOpacity != 0:
                    self.poofOpacity -= 10
                if self.counter >= 52 and self.alert[0]:
                    self.alert[1] = pg.mixer.Sound(
                        'sounds/wav/sec/' + f'{61 - self.counter}Sec.wav')
                    self.alert[1].play()
                    self.alert[0] = False
                self.seconds = pg.image.load(
                    images['second'] + (f'{61 - self.counter}.png' if 61 - self.counter >= 10 else f'0{61 - self.counter}.png'))
            else:
                self.auxRecovery = round(pg.time.get_ticks()/1000)
                self.data = [True, True]
                timeAux = round(pg.time.get_ticks()/1000)

        screen.blit(self.seconds, (477, 53))

        self.mts = pg.font.Font('font/04B_30__.TTF', 30)
        self.mtsRender = self.mts.render(
            f'{round(listDist[0])/10} metros', True, colors['active'])
        self.mtsRect = self.mtsRender.get_rect()
        self.mtsRect.center = (540, 774)
        screen.blit(self.mtsRender, self.mtsRect)

        self.basketCant = []

        for i in range(self.attemptsCounter):
            self.basketCant.append(pg.image.load(
                images['basket'] + 'cant.png'))

        self.basketCant += [pg.image.load(images['basket'] + 'border.png')
                            for i in range(3 - len(self.basketCant))]

        for i in range(len(self.basketCant)):
            screen.blit(self.basketCant[i], (48, 36) if i == 0 else (
                76, 36) if i == 1 else (104, 36))

        self.label = pg.font.Font('font/04B_30__.TTF', 18)
        self.cantRender = [self.label.render(
            'Intentos' if i == 0 else 'Restantes' if i == 1 else f'{self.attemptsCounter}', True, colors['inactive' if 6 <= hour < 18 else 'active']) for i in range(3)]
        screen.blit(self.cantRender[0], (66, 100))
        screen.blit(self.cantRender[1], (55, 121))
        screen.blit(self.cantRender[2], (114, 144))

        if False not in self.data and self.counter != 61:
            if self.index < 180:
                screen.blit(
                    self.provision, (self.listLaunch[self.index][0] - 21.5, self.listLaunch[self.index][1] - 28))
                self.index += 3
                if self.index == 180:
                    sounds['launchEnd'].play()
            if self.launch != 9:
                if self.launch != round(pg.time.get_ticks()/1000) - self.auxRecovery:
                    self.launch += 1
                if 825 <= distanceLateral[houseI][-1] <= 1006:
                    if 4 <= self.launch < 9:
                        self.attemptsCounterCpu = self.attemptsCounter + 1
                        self.poofOpacity = 100
                        self.noAttempts = pg.image.load(images['nice'])
                        screen.blit(self.noAttempts, (225, 349))
                    elif self.launch == 9:
                        delivered[houseI].append(True)
                        if mode[1] and self.playCpu:
                            while (self.attemptsCounterCpu != 0):
                                dataCpu[houseI].append(
                                    self.distance(randint(20, 60), (sqrt((9.8*(listDistCpu[0] + self.extra))/sin(radians(2*45)))/8) * randint(4, 8)))
                                distanceLateralCpu[houseI].append(
                                    (dataCpu[houseI][-1]*916.5)/listDistCpu[0])
                                if True in [(i[0] <= distanceLateralCpu[houseI][-1] <= i[1] if len(i) != 0 else False) for i in self.poolPosLateralCpu[houseI]]:
                                    deliveredCpu[houseI].append('lost')
                                    penaltiesCpu[houseI].append(5)
                                elif 825 <= distanceLateralCpu[houseI][-1] <= 1006:
                                    deliveredCpu[houseI].append(True)
                                    penaltiesCpu[houseI].append(0)
                                    self.playCpu = False
                                    self.attemptsCounterCpu = 1
                                else:
                                    deliveredCpu[houseI].append(False)
                                    penaltiesCpu[houseI].append(0)
                                self.attemptsCounterCpu -= 1
                        if houseI != 3:
                            houseI += 1
                            self.extra = randint(50, 150)
                        pg.mixer.music.stop()
                        self.alert[0] = True
                        self.attemptsCounter = 3
                        self.counter = 0
                        self.playCpu = True
                        self.data = [False, False]
                        self.angle, self.power = 1, 1
                        self.addAngle, self.addPower = True, True
                        timeAux = round(pg.time.get_ticks()/1000)
                elif True in [(i[0] <= distanceLateral[houseI][-1] <= i[1] if len(i) != 0 else False) for i in self.poolPosLateral[houseI]]:
                    if mode[1] and self.playCpu:
                        dataCpu[houseI].append(
                            self.distance(randint(20, 60), (sqrt((9.8*(listDistCpu[0] + self.extra))/sin(radians(2*45)))/8) * randint(4, 8)))
                        distanceLateralCpu[houseI].append(
                            (dataCpu[houseI][-1]*916.5)/listDistCpu[0])
                        if True in [(i[0] <= distanceLateralCpu[houseI][-1] <= i[1] if len(i) != 0 else False) for i in self.poolPosLateralCpu[houseI]]:
                            deliveredCpu[houseI].append('lost')
                            penaltiesCpu[houseI].append(5)
                        elif 825 <= distanceLateralCpu[houseI][-1] <= 1006:
                            deliveredCpu[houseI].append(True)
                            penaltiesCpu[houseI].append(0)
                        else:
                            deliveredCpu[houseI].append(False)
                            penaltiesCpu[houseI].append(0)
                        self.playCpu = False
                    if self.attemptsCounter == 0:
                        if 4 <= self.launch < 9:
                            self.poofOpacity = 100
                            self.noAttempts = pg.image.load(
                                images['noAttempts'])
                            screen.blit(self.noAttempts, (316, 350))
                        elif self.launch == 9:
                            delivered[houseI].append('lost')
                            if houseI != 3:
                                houseI += 1
                                self.extra = randint(50, 150)
                            pg.mixer.music.stop()
                            self.alert[0] = True
                            self.playCpu = True
                            self.attemptsCounter = 3
                            self.counter = 0
                            timeAux = round(pg.time.get_ticks()/1000)
                            self.data = [False, False]
                            self.angle, self.power = 1, 1
                            self.addAngle, self.addPower = True, True
                    else:
                        if self.launch == 4:
                            delivered[houseI].append('lost')
                            timeAux += self.launch + 1
                            self.data = [False, False]
                            self.angle, self.power = 1, 1
                            self.addAngle, self.addPower = True, True
                elif self.attemptsCounter == 0:
                    if 4 <= self.launch < 9:
                        self.poofOpacity = 100
                        self.noAttempts = pg.image.load(images['noAttempts'])
                        screen.blit(self.noAttempts, (316, 350))
                    elif self.launch == 9:
                        delivered[houseI].append(False)
                        if mode[1] and self.playCpu:
                            dataCpu[houseI].append(
                                self.distance(randint(20, 60), (sqrt((9.8*(listDistCpu[0] + self.extra))/sin(radians(2*45)))/8) * randint(4, 8)))
                            distanceLateralCpu[houseI].append(
                                (dataCpu[houseI][-1]*916.5)/listDistCpu[0])
                            if True in [(i[0] <= distanceLateralCpu[houseI][-1] <= i[1] if len(i) != 0 else False) for i in self.poolPosLateralCpu[houseI]]:
                                deliveredCpu[houseI].append('lost')
                                penaltiesCpu[houseI].append(5)
                            elif 825 <= distanceLateralCpu[houseI][-1] <= 1006:
                                deliveredCpu[houseI].append(True)
                                penaltiesCpu[houseI].append(0)
                                self.playCpu = False
                            else:
                                deliveredCpu[houseI].append(False)
                                penaltiesCpu[houseI].append(0)
                        if houseI != 3:
                            houseI += 1
                            self.extra = randint(50, 150)
                        pg.mixer.music.stop()
                        self.alert[0] = True
                        self.playCpu = True
                        self.attemptsCounter = 3
                        self.counter = 0
                        timeAux = round(pg.time.get_ticks()/1000)
                        self.data = [False, False]
                        self.angle, self.power = 1, 1
                        self.addAngle, self.addPower = True, True
                else:
                    if self.launch == 4:
                        delivered[houseI].append(False)
                        if mode[1] and self.playCpu:
                            dataCpu[houseI].append(
                                self.distance(randint(20, 60), (sqrt((9.8*(listDistCpu[0] + self.extra))/sin(radians(2*45)))/8) * randint(4, 8)))
                            distanceLateralCpu[houseI].append(
                                (dataCpu[houseI][-1]*916.5)/listDistCpu[0])
                            if True in [(i[0] <= distanceLateralCpu[houseI][-1] <= i[1] if len(i) != 0 else False) for i in self.poolPosLateralCpu[houseI]]:
                                deliveredCpu[houseI].append('lost')
                                penaltiesCpu[houseI].append(5)
                            elif 825 <= distanceLateralCpu[houseI][-1] <= 1006:
                                deliveredCpu[houseI].append(True)
                                penaltiesCpu[houseI].append(0)
                                self.playCpu = False
                            else:
                                deliveredCpu[houseI].append(False)
                                penaltiesCpu[houseI].append(0)
                        timeAux += self.launch + 1
                        self.data = [False, False]
                        self.angle, self.power = 1, 1
                        self.addAngle, self.addPower = True, True

        self.powerRender = self.label.render(
            f'{self.power * 10 + self.power * 2.5}% Velocidad', True, colors['active'])
        screen.blit(self.powerRender, (130.5, 786.735))
        screen.blit(pg.image.load(
            images['power'] + f'{self.power}.png'), (10.5, 766))

        if self.data[0] and not self.data[1] and self.start:
            self.power += (1 if self.addPower else -1)
            if self.power == 8:
                self.addPower = False
            elif self.power == 1:
                self.addPower = True
            for event in events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        sounds['launchStart'].play()
                        if self.attemptsCounter > 0:
                            self.attemptsCounter -= 1
                        self.data[1] = True
                        self.start = False
                        data[houseI].append(
                            self.distance(self.angle, (sqrt((9.8*(listDist[0] + self.extra))/sin(radians(2*45)))/8) * self.power))
                        self.auxRecovery = round(
                            pg.time.get_ticks()/1000) if self.auxRecovery == 0 else self.auxRecovery
                        distanceLateral[houseI].append(
                            (data[houseI][-1]*916.5)/listDist[0])
                        penalties[houseI].append(0)
                        self.listLaunch = [pg.draw.arc(screen, (255, 255, 255), (50.5, 687 - distanceLateral[houseI][-1]/2, distanceLateral[houseI][-1], distanceLateral[houseI][-1]), radians(89), radians(i), 1).bottomleft for i in range(90, 180)][::-1] + [
                            pg.draw.arc(screen, (255, 255, 255), (50.5, 687 - distanceLateral[houseI][-1]/2, distanceLateral[houseI][-1], distanceLateral[houseI][-1]), radians(0), radians(i), 1).topleft for i in range(1, 90)][::-1] + [pg.draw.arc(screen, (255, 255, 255), (50.5, 687 - distanceLateral[houseI][-1]/2, distanceLateral[houseI][-1], distanceLateral[houseI][-1]), radians(0), radians(180), 1).bottomright]
                        self.index = 0
        arcHigher = pg.draw.arc(screen, (255, 255, 255), (10.5, 716, 80, 80), radians(
            0), radians(self.angle), 3)
        pg.draw.arc(screen, (255, 255, 255), (33.125, 738.625,
                    34.75, 34.75), radians(0), radians(self.angle), 3)

        pg.draw.line(screen, (255, 255, 255), (50.5, 756), (90.5, 756), 3)
        pg.draw.line(screen, (255, 255, 255),
                     (50.5, 756), arcHigher.topleft, 3)

        self.aglRender = self.label.render(
            f'{self.angle} Grados', True, colors['active'])
        screen.blit(self.aglRender, (130.5, 737.47))

        if not self.data[0] and self.start:
            self.angle += (1 if self.addAngle else -1)
            if self.angle == 90:
                self.addAngle = False
            elif self.angle == 1:
                self.addAngle = True
            for event in events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.data[0] = True


class ScoreBoardScreen():
    '''ScoreBoardScreen: Clase contenedora de los resultados finales posterior al juego'''
    def __init__(self):
        '''__init__: Constructor de la clase ScoreBoardScreen'''
        self.backGround = pg.image.load(images['scoreBoardBackGround'])
        self.formatFont48 = pg.font.Font('font/04B_30__.TTF', 48)
        self.formatFont18 = pg.font.Font('font/04B_30__.TTF', 18)

    def update(self, events):
        '''update: Función que mantiene actualizado los valores y objetos en el ScoreBoardScreen'''
        global newUpdate, mode, difficulty

        if newUpdate:
            self.timeAux = round(pg.time.get_ticks()/1000)
            self.lPlayer = [0, 0, 0]
            self.lCpu = [0, 0, 0]
            self.pointDiference = 0
            self.totalPlayer = 0
            self.totalCpu = 0
            self.counter = 0
            self.playerHouse = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]
            self.cpuHouse = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]

            self.deliveredPlayer = delivered
            for i in range(len(self.deliveredPlayer)):
                while len(self.deliveredPlayer[i]) < 3:
                    self.deliveredPlayer[i].append('safe')

            self.deliveredCpu = deliveredCpu
            for i in range(len(self.deliveredCpu)):
                while len(self.deliveredCpu[i]) < 3:
                    self.deliveredCpu[i].append('safe')

            self.playerMts = data
            for i in range(len(self.playerMts)):
                for e in range(len(self.playerMts[i])):
                    if self.deliveredPlayer[i][e]:
                        self.playerMts[i][e] = 0
                    else:
                        self.playerMts[i][e] = abs(round(
                            dictInfo['playerHouseOne' if i == 0 else 'playerHouseTwo' if i == 1 else 'playerHouseThree'][0]) - round(self.playerMts[i][e]))

            self.cpuMts = dataCpu if dataCpu != [
                [], [], []] else [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            for i in range(len(self.cpuMts)):
                for e in range(len(self.cpuMts[i])):
                    if self.deliveredCpu[i][e]:
                        self.cpuMts[i][e] = 0
                    else:
                        self.cpuMts[i][e] = abs(round(
                            dictInfo['cpuHouseOne' if i == 0 else 'cpuHouseTwo' if i == 1 else 'cpuHouseThree'][0]) - round(self.cpuMts[i][e]))

            self.lostPlayer = [p.count('lost') for p in self.deliveredPlayer]
            self.lostCpu = [c.count('lost') for c in self.deliveredCpu]

            newUpdate = False

        screen.blit(self.backGround, (0, 0))

        title = [
            (self.formatFont48.render('Tablero',
             True, (120, 224, 135)), (400.78, 22.16)),
            (self.formatFont48.render('Puntuaciones',
             True, (120, 224, 135)), (308.78, 79.16))
        ]

        image = [
            (pg.image.load(images['playerLateral']), (144, 155)),
            (pg.image.load(images['cpuLateral']), (875, 155)),
            (pg.image.load(images['houseOneAir']), (492, 360)),
            (pg.image.load(images['houseTwoAir']), (492, 506)),
            (pg.image.load(images['houseThreeAir']), (482, 632))
        ]

        name = [
            (self.formatFont18.render(
                screenSelect['main'][1].inputBox.text, True, (0, 255, 0)), (113.78, 114.79)),
            (self.formatFont18.render('CPU', True, (255, 0, 0)), (878.78, 114.79))
        ]

        titleInfo = [
            (self.formatFont18.render('Distancias',
             True, (0, 255, 0)), (104.78, 310.79)),
            (self.formatFont18.render('MTS', True, (0, 255, 0)), (146.78, 332.79)),

            (self.formatFont18.render('Entregadas',
             True, (120, 224, 135)), (305.78, 310.79)),
            (self.formatFont18.render('No Entregadas',
             True, (220, 224, 120)), (282.78, 332.79)),
            (self.formatFont18.render('Perdidas',
             True, (203, 110, 110)), (323.78, 354.79)),

            (self.formatFont18.render('Entregadas',
             True, (120, 224, 135)), (622.78, 310.79)),
            (self.formatFont18.render('No Entregadas',
             True, (220, 224, 120)), (599.78, 332.79)),
            (self.formatFont18.render('Perdidas',
             True, (203, 110, 110)), (640.79, 354.79)),

            (self.formatFont18.render('Distancias',
             True, (255, 0, 0)), (839.78, 310.79)),
            (self.formatFont18.render('MTS', True, (255, 0, 0)), (881.78, 332.79)),
        ]

        y = 386.79
        yCounters = 386.79

        mts = []
        counters = []
        for i in range(len(self.deliveredPlayer)):
            falsePlayer = 0
            truePlayer = 0
            falseCpu = 0
            trueCpu = 0
            extra = 0
            for e in range(len(self.deliveredPlayer[i])):
                if self.deliveredPlayer[i][e] == True:
                    mts.append((self.formatFont18.render(
                        '0.0', True, (120, 224, 135)), (96.78, y)))
                    mts.append((self.formatFont18.render(
                        'MTS', True, (120, 224, 135)), (198.78, y)))
                    truePlayer += 1
                elif self.deliveredPlayer[i][e] == 'lost':
                    mts.append((self.formatFont18.render(
                        f'{self.playerHouse[i][e]/10} ', True, (203, 110, 110)), (96.78, y)))
                    mts.append((self.formatFont18.render(
                        'MTS', True, (203, 110, 110)), (198.78, y)))
                elif self.deliveredPlayer[i][e] == 'safe':
                    mts.append((self.formatFont18.render(
                        'Sin Lanzar', True, (120, 224, 135)), (100.78, y)))
                else:
                    mts.append((self.formatFont18.render(
                        f'{self.playerHouse[i][e]/10} ', True, (220, 224, 120)), (96.78, y)))
                    mts.append((self.formatFont18.render(
                        'MTS', True, (220, 224, 120)), (198.78, y)))
                    falsePlayer += 1
                extra += 22
                y += 22

            mts.append((self.formatFont18.render(
                '+', True, (203, 110, 110)), (79.78, y + 10)))
            mts.append((self.formatFont18.render(
                f'{self.lPlayer[i]} ', True, (203, 110, 110)), (96.78, y + 10)))
            mts.append((self.formatFont18.render(
                'MTS', True, (203, 110, 110)), (198.78, y + 10)))

            y -= extra

            for e in range(len(self.deliveredCpu[i])):
                if self.deliveredCpu[i][e] == True:
                    mts.append((self.formatFont18.render(
                        '0.0', True, (120, 224, 135)), (831.78, y)))
                    mts.append((self.formatFont18.render(
                        'MTS', True, (120, 224, 135)), (933.78, y)))
                    trueCpu += 1
                elif self.deliveredCpu[i][e] == 'lost':
                    mts.append((self.formatFont18.render(
                        f'{self.cpuHouse[i][e]/10} ', True, (203, 110, 110)), (831.78, y)))
                    mts.append((self.formatFont18.render(
                        'MTS', True, (203, 110, 110)), (933.78, y)))
                elif self.deliveredCpu[i][e] == 'safe':
                    mts.append((self.formatFont18.render(
                        'Sin Lanzar', True, (120, 224, 135)), (835.78, y)))
                else:
                    mts.append((self.formatFont18.render(
                        f'{self.cpuHouse[i][e]/10} ', True, (220, 224, 120)), (831.78, y)))
                    mts.append((self.formatFont18.render(
                        'MTS', True, (220, 224, 120)), (933.78, y)))
                    falseCpu += 1
                y += 22

            mts.append((self.formatFont18.render(
                '+', True, (203, 110, 110)), (814.78, y + 10)))
            mts.append((self.formatFont18.render(
                f'{self.lCpu[i]} ', True, (203, 110, 110)), (831.78, y + 10)))
            mts.append((self.formatFont18.render(
                'MTS', True, (203, 110, 110)), (933.78, y + 10)))

            counters += [
                (self.formatFont18.render(
                    f'{truePlayer}', True, (120, 224, 135)), (378.78, yCounters + 12.505)),
                (self.formatFont18.render(
                    f'{falsePlayer}', True, (220, 224, 120)), (378.78, yCounters + 22 + 12.505)),
                (self.formatFont18.render(
                    f'{self.lostPlayer[i]}', True, (203, 110, 110)), (378.78, yCounters + 44 + 12.505)),
                (self.formatFont18.render(
                    f'{trueCpu}', True, (120, 224, 135)), (685.78, yCounters + 12.505)),
                (self.formatFont18.render(
                    f'{falseCpu}', True, (220, 224, 120)), (685.78, yCounters + 22 + 12.505)),
                (self.formatFont18.render(
                    f'{self.lostCpu[i]}', True, (203, 110, 110)), (685.78, yCounters + 44 + 12.505))
            ]
            yCounters += (89 + (2 * 22))
            y += 67

        results = [
            (self.formatFont48.render(
                f'{str(self.totalPlayer/10).rjust(5)}', True, (0, 255, 0)), (298.78, 182.79)),
            (self.formatFont48.render(':', True, (220, 224, 120)), (530.78, 182.79)),
            (self.formatFont48.render(
                f'{str(self.totalCpu/10).ljust(5)}', True, (255, 0, 0)), (595.78, 182.79)),
        ]
        diff = [
            (self.formatFont18.render(f'{"-" if self.totalPlayer > self.totalCpu else "+"  if self.totalPlayer < self.totalCpu else ""}{str(self.pointDiference/10).rjust(4)}',
             True, (203, 110, 110) if self.totalPlayer > self.totalCpu else (120, 224, 135) if self.totalPlayer < self.totalCpu else (255, 255, 255)), (412.78, 232.79)),
            (self.formatFont18.render(f'{"+" if self.totalPlayer > self.totalCpu else "-"  if self.totalPlayer < self.totalCpu else ""}{str(self.pointDiference/10).ljust(4)}',
             True, (120, 224, 135) if self.totalPlayer > self.totalCpu else (203, 110, 110) if self.totalPlayer < self.totalCpu else (255, 255, 255)), (595.78, 232.79)),
        ]

        if self.counter != round(pg.time.get_ticks()/1000) - self.timeAux:
            self.counter += 1
        if 2 <= self.counter:
            self.lPlayer[0] += 1 if self.lPlayer[0] < (
                self.lostPlayer[0] * 5) else 0
            self.lPlayer[1] += 1 if self.lPlayer[1] < (
                self.lostPlayer[1] * 5) else 0
            self.lPlayer[2] += 1 if self.lPlayer[2] < (
                self.lostPlayer[2] * 5) else 0
            self.lCpu[0] += 1 if self.lCpu[0] < self.lostCpu[0] * 5 else 0
            self.lCpu[1] += 1 if self.lCpu[1] < self.lostCpu[1] * 5 else 0
            self.lCpu[2] += 1 if self.lCpu[2] < self.lostCpu[2] * 5 else 0
            for i in range(len(self.playerMts)):
                for e in range(len(self.playerMts[i])):
                    if len(self.playerMts[i]) >= 1:
                        self.playerHouse[i][e] += 5 if self.playerHouse[i][e] < self.playerMts[i][e] else self.playerMts[i][e] - \
                            self.playerHouse[i][e]
            for i in range(len(self.cpuMts)):
                for e in range(len(self.cpuMts[i])):
                    if len(self.cpuMts[i]) >= 1:
                        self.cpuHouse[i][e] += 5 if self.cpuHouse[i][e] < self.cpuMts[i][e] else self.cpuMts[i][e] - self.cpuHouse[i][e]
                        
            back = [
                (self.formatFont18.render('Pulse', True,
                (120, 224, 135)), (253.18, 774.51)),
                (self.formatFont18.render('ESC', True,
                (203, 110, 110)), (343.18, 774.51)),
                (self.formatFont18.render('para volver al',
                True, (120, 224, 135)), (409.18, 774.51)),
                (self.formatFont18.render('Menu', True,
                (220, 224, 120)), (629.18, 774.51)),
                (self.formatFont18.render('Principal',
                True, (220, 224, 120)), (706.18, 774.51)),
            ]
            if 22 <= self.counter:
                screen.blits(back)
                for event in events:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            screenSelect['main'][1].    inputBox.text = ''
                            screenSelect['main'][1].inputBox.color = colors['inactive']
                            screenSelect['main'][1].inputBox.active = False
                            mode = [True, False]
                            difficulty = [True, False]
                            screenSelect['main'][0] = True
                            screenSelect['scoreBoard'][0] = False
            
        if self.playerHouse == [[round(i) for i in e] + ([0] if len(e) == 2 else [0, 0] if len(e) == 1 else []) for e in self.playerMts] and self.cpuHouse == [[round(i) for i in e] + ([0] if len(e) == 2 else [0, 0] if len(e) == 1 else []) for e in self.cpuMts]:
            self.totalPlayer += 5 if self.totalPlayer < sum([sum(self.playerHouse[0]), sum(self.playerHouse[1]), sum(self.playerHouse[2])]) + sum(
                self.lPlayer) else sum([sum(self.playerHouse[0]), sum(self.playerHouse[1]), sum(self.playerHouse[2])]) + sum(self.lPlayer) - self.totalPlayer
            self.totalCpu += 5 if self.totalCpu < sum([sum(self.cpuHouse[0]), sum(self.cpuHouse[1]), sum(self.cpuHouse[2])]) + sum(
                self.lCpu) else sum([sum(self.cpuHouse[0]), sum(self.cpuHouse[1]), sum(self.cpuHouse[2])]) + sum(self.lCpu) - self.totalCpu
        if self.totalPlayer == sum([sum(self.playerHouse[0]), sum(self.playerHouse[1]), sum(self.playerHouse[2])]) + sum(self.lPlayer) and self.totalCpu == sum([sum(self.cpuHouse[0]), sum(self.cpuHouse[1]), sum(self.cpuHouse[2])]) + sum(self.lCpu):
            self.pointDiference += 5 if self.pointDiference < abs(self.totalPlayer - self.totalCpu) else abs(
                self.totalPlayer - self.totalCpu) - self.pointDiference

        screen.blits(title)
        screen.blits(image)
        screen.blits(name)
        screen.blits(titleInfo)
        screen.blits(mts)
        screen.blits(counters)
        screen.blits(results)
        screen.blits(diff) if mode[1] else None


def randomPos():
    '''randomPos: Genera posiciones X e Y aleatorias para ubicar los objetos en el segundo escenario
    return: retorna un diccionario con los nombres y tuplas con las posiciones de los objetos'''
    limitLW = 50
    limitRW = width-limitLW

    limitUH = 56
    limitDH = height-limitUH

    while True:
        count = 0
        listPos = {
            'player': (randint(limitLW, limitRW-35), randint(limitUH, limitDH-60)),
            'cpu': (0, 0),
            'houseOne': (0, 0),
            'houseTwo': (0, 0),
            'houseThree': (0, 0),
            'poolOne': (0, 0),
            'poolTwo': (0, 0),
            'poolThree': (0, 0),
            'poolFour': (0, 0),
            'poolFive': (0, 0),
        }
        for key in listPos:
            if key != 'player':
                w = 35 if key == 'cpu' else 96 if key == 'houseOne' or key == 'houseTwo' else 116 if key == 'houseThree' else 100
                h = 60 if key == 'cpu' else 114 if key == 'houseOne' else 89 if key == 'houseTwo' else 102 if key == 'houseThree' else 85

                x, y = randint(limitLW, limitRW-w), randint(limitUH, limitDH-h)
                while True:
                    wPlayer = abs(listPos['player'][0] -
                                  x) < h + (10 if key == 'cpu' else 25)
                    hPlayer = abs(listPos['player'][1] -
                                  y) < w + (10 if key == 'cpu' else 25)
                    wCpu = abs(listPos['cpu'][0] - x) < h + \
                        (10 if key == 'cpu' else 50)
                    hCpu = abs(listPos['cpu'][1] - y) < w + \
                        (10 if key == 'cpu' else 50)
                    wHouseOne = abs(
                        listPos['houseOne'][0] - x) < h + (10 if key == 'cpu' else 50)
                    hHouseOne = abs(
                        listPos['houseOne'][1] - y) < w + (10 if key == 'cpu' else 50)
                    wHouseTwo = abs(
                        listPos['houseTwo'][0] - x) < h + (10 if key == 'cpu' else 50)
                    hHouseTwo = abs(
                        listPos['houseTwo'][1] - y) < w + (10 if key == 'cpu' else 50)
                    wHouseThree = abs(
                        listPos['houseThree'][0] - x) < h + (10 if key == 'cpu' else 50)
                    hHouseThree = abs(
                        listPos['houseThree'][1] - y) < w + (10 if key == 'cpu' else 50)
                    wPoolOne = abs(listPos['poolOne'][0] -
                                   x) < h + (10 if key == 'cpu' else 50)
                    hPoolOne = abs(listPos['poolOne'][1] -
                                   y) < w + (10 if key == 'cpu' else 50)
                    wPoolTwo = abs(listPos['poolTwo'][0] -
                                   x) < h + (10 if key == 'cpu' else 50)
                    hPoolTwo = abs(listPos['poolTwo'][1] -
                                   y) < w + (10 if key == 'cpu' else 50)
                    wPoolThree = abs(
                        listPos['poolThree'][0] - x) < h + (10 if key == 'cpu' else 50)
                    hPoolThree = abs(
                        listPos['poolThree'][1] - y) < w + (10 if key == 'cpu' else 50)
                    wPoolFour = abs(
                        listPos['poolFour'][0] - x) < h + (10 if key == 'cpu' else 50)
                    hPoolFour = abs(
                        listPos['poolFour'][1] - y) < w + (10 if key == 'cpu' else 50)
                    if count == 25:
                        break
                    else:
                        count += 1
                    if key == 'cpu':
                        if wPlayer and hPlayer or abs(listPos['player'][0] - x) > 225 or abs(listPos['player'][1] - y) > 350:
                            x, y = randint(limitLW, limitRW -
                                           w), randint(limitUH, limitDH-h)
                        else:
                            listPos[key] = x, y
                            break
                    elif key == 'houseOne':
                        if wPlayer and hPlayer or wCpu and hCpu:
                            x, y = randint(limitLW, limitRW -
                                           w), randint(limitUH, limitDH-h)
                        else:
                            listPos[key] = x, y
                            break
                    elif key == 'houseTwo':
                        if wPlayer and hPlayer or wCpu and hCpu or wHouseOne and hHouseOne:
                            x, y = randint(limitLW, limitRW -
                                           w), randint(limitUH, limitDH-h)
                        else:
                            listPos[key] = x, y
                            break
                    elif key == 'houseThree':
                        if wPlayer and hPlayer or wCpu and hCpu or wHouseOne and hHouseOne or wHouseTwo and hHouseTwo:
                            x, y = randint(limitLW, limitRW -
                                           w), randint(limitUH, limitDH-h)
                        else:
                            listPos[key] = x, y
                            break
                    elif key == 'poolOne':
                        if wPlayer and hPlayer or wCpu and hCpu or wHouseOne and hHouseOne or wHouseTwo and hHouseTwo or wHouseThree and hHouseThree:
                            x, y = randint(limitLW, limitRW -
                                           w), randint(limitUH, limitDH-h)
                        else:
                            listPos[key] = x, y
                            break
                    elif key == 'poolTwo':
                        if wPlayer and hPlayer or wCpu and hCpu or wHouseOne and hHouseOne or wHouseTwo and hHouseTwo or wHouseThree and hHouseThree or wPoolOne and hPoolOne:
                            x, y = randint(limitLW, limitRW -
                                           w), randint(limitUH, limitDH-h)
                        else:
                            listPos[key] = x, y
                            break
                    elif key == 'poolThree':
                        if wPlayer and hPlayer or wCpu and hCpu or wHouseOne and hHouseOne or wHouseTwo and hHouseTwo or wHouseThree and hHouseThree or wPoolOne and hPoolOne or wPoolTwo and hPoolTwo:
                            x, y = randint(limitLW, limitRW -
                                           w), randint(limitUH, limitDH-h)
                        else:
                            listPos[key] = x, y
                            break
                    elif key == 'poolFour':
                        if wPlayer and hPlayer or wCpu and hCpu or wHouseOne and hHouseOne or wHouseTwo and hHouseTwo or wHouseThree and hHouseThree or wPoolOne and hPoolOne or wPoolTwo and hPoolTwo or wPoolThree and hPoolThree:
                            x, y = randint(limitLW, limitRW -
                                           w), randint(limitUH, limitDH-h)
                        else:
                            listPos[key] = x, y
                            break
                    elif key == 'poolFive':
                        if wPlayer and hPlayer or wCpu and hCpu or wHouseOne and hHouseOne or wHouseTwo and hHouseTwo or wHouseThree and hHouseThree or wPoolOne and hPoolOne or wPoolTwo and hPoolTwo or wPoolThree and hPoolThree or wPoolFour and hPoolFour:
                            x, y = randint(limitLW, limitRW -
                                           w), randint(limitUH, limitDH-h)
                        else:
                            listPos[key] = x, y
                            return listPos


def updatePos():
    '''updatePos: Genera posiciones X e Y aleatorias para posicionar el solo y la luna en el escenario de juego
       return: retorna un diccionario que tiene como keys las horas en formato de 12 y como valor listas de tuplas representando cada minuto del dia
    '''
    listC = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
        10: [],
        11: [],
    }
    for i in range(360):
        lArc = pg.draw.arc(
            screen, colors['black'], (100, 242, 880, 880), radians(i*0.25), radians((719 - i) * 0.25), 1)
        listC[11 - (i // 60)].append(lArc.bottomleft)
        listC[(i // 60)].append(lArc.bottomright)
    for i in range(6, 12):
        listC[i] = listC[i][::-1]
    return listC


def collide(pj, house, pool):
    '''collide: Calcula la proyccion del obstaculo sobre el vector entre el pj/cpu y las casas
       return: retorna una tupla con lo siguiente:
               boolean: dependiendo de si la distancia entre el centro del obstaculo y el punto de la proyeccion es menor a 40
               tupla: valores que deben sumarse a la posicion de la casa para obtener el punto de la proyeccion'''


    c = pool[0] - house[0], pool[1] - house[1]

    v = pj[0] - house[0], pj[1] - house[1]
    v_norm = v[0]/sqrt(v[0]**2 + v[1]**2), v[1]/sqrt(v[0]**2 + v[1]**2)

    b_mod = c[0] * v_norm[0] + c[1] * v_norm[1]
    b = v_norm[0] * b_mod, v_norm[1] * b_mod

    a = sqrt((c[0]-b[0])**2+(c[1]-b[1])**2)


    return a < 30, b


def main():
    '''main: Función Principal del programa, contiene variables importantes para la ejecución correcta del programa'''
    global width, height, colors, sounds, images, screen, difficulty, mode, screenSelect, timeActually, hour, minute, hourAux, updateMap, timeAux, houseI, data, distanceLateral, penalties, delivered, dataCpu, distanceLateralCpu, penaltiesCpu, deliveredCpu, newUpdate, newGame

    fps = 60
    clock = pg.time.Clock()
    size = width, height = 1080, 824

    timeActually = 0
    timeAux = 0
    hourAux = {
        6: 0, 18: 0,
        7: 1, 19: 1,
        8: 2, 20: 2,
        9: 3, 21: 3,
        10: 4, 22: 4,
        11: 5, 23: 5,
        12: 6, 0: 6,
        13: 7, 1: 7,
        14: 8, 2: 8,
        15: 9, 3: 9,
        16: 10, 4: 10,
        17: 11, 5: 11,
    }

    colors = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'inactive': (62, 78, 94),
        'active': (120, 224, 135),
    }

    sounds = {
        'lapseSound': pg.mixer.Sound('sounds/wav/lapse.wav'),
        'toSelect': pg.mixer.Sound('sounds/wav/toSelect.wav'),
        'launchStart': pg.mixer.Sound('sounds/wav/launchStart.wav'),
        'launchEnd': pg.mixer.Sound('sounds/wav/launchEnd.wav'),
    }

    images = {
        'menuBackground': 'images/backgrounds/menu/menu.png',
        'titleText': 'images/menu/mainTitle.png',
        'nameText': 'images/menu/nameText.png',
        'difficultyText': 'images/menu/difficultyText.png',
        'basicText': 'images/menu/basicText.png',
        'advancedText': 'images/menu/advancedText.png',
        'modeText': 'images/menu/modeText.png',
        'onePlayerText': 'images/menu/onePlayerText.png',
        'playerVSCPUText': 'images/menu/playerVSCPUText.png',

        'houseOneAir': 'images/houses/1x/houseOne.png',
        'houseTwoAir': 'images/houses/1x/houseTwo.png',
        'houseThreeAir': 'images/houses/1x/houseThree.png',
        'poolAir': 'images/obstacles/pool.png',
        'playerAir': 'images/player/1x/player.png',
        'cpuAir': 'images/cpu/1x/cpu.png',

        'sun': 'images/backgrounds/game/sun.png',
        'moon': 'images/backgrounds/game/moon.png',
        'groundDay': 'images/backgrounds/game/groundDay.png',
        'groundNight': 'images/backgrounds/game/groundNight.png',
        'day': 'images/backgrounds/game/day.png',
        'night': 'images/backgrounds/game/night.png',
        'poolGround': 'images/backgrounds/game/poolGround.png',
        'houseOneLateral': 'images/houses/2x/houseOne.png',
        'houseTwoLateral': 'images/houses/2x/houseTwo.png',
        'houseThreeLateral': 'images/houses/2x/houseThree.png',
        'poof': 'images/backgrounds/game/poof/poof',
        'playerLateral': 'images/player/2x/player.png',
        'cloud': 'images/backgrounds/game/seconds/cloud',
        'second': 'images/backgrounds/game/seconds/',
        'timeOut': 'images/backgrounds/game/seconds/timeOut.png',
        'noAttempts': 'images/backgrounds/game/seconds/noAttempts.png',
        'nice': 'images/backgrounds/game/basket of provisions/nice.png',
        'basket': 'images/backgrounds/game/basket of provisions/',
        'power': 'images/backgrounds/game/power/',

        'scoreBoardBackGround': 'images/backgrounds/scoreboard/background.png',
        'cpuLateral': 'images/cpu/2x/cpuReversed.png',

        'lapseDay': 'images/backgrounds/lapseDay',
        'lapseNight': 'images/backgrounds/lapseNight',
        'mapBackgroundDay': 'images/backgrounds/map/mapDay.png',
        'mapBackgroundNight': 'images/backgrounds/map/mapNight.png',
    }

    difficulty = [
        True,
        False
    ]

    mode = [
        True,
        False
    ]

    screen = pg.display.set_mode(size)
    pg.display.set_caption('Entrega la Canasta')

    hour = datetime.now().hour
    minute = datetime.now().minute

    mainScreen = MainScreen()
    mapScreen = MapScreen()
    gameScreen = GameScreen()
    scoreBoardScreen = ScoreBoardScreen()
    screenSelect = {
        'main': [True, mainScreen],
        'map': [False, mapScreen],
        'game': [False, gameScreen],
        'mapResult': [False, mapScreen],
        'scoreBoard': [False, scoreBoardScreen],
    }

    isRunning = True

    while (isRunning):
        lapse = pg.image.load(
            images['lapseDay' if 6 <= datetime.now().hour < 18 else 'lapseNight'] + ('.png' if screenSelect['map'][0] else '2.png' if screenSelect['game'][0] else '3.png' if screenSelect['mapResult'][0] else '4.png'))
        hour = datetime.now().hour
        minute = datetime.now().minute
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                isRunning = False
                break
        if screenSelect['main'][0]:
            if pg.mixer.music.get_pos() == -1:
                pg.mixer.music.load('sounds/wav/intro_slow.wav')
                pg.mixer.music.set_volume(0.3)
                pg.mixer.music.play(4)
            for event in events:
                screenSelect['main'][1].inputBox.keyEvent(event)
            screenSelect['main'][1].update(event)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    pg.mixer.music.stop()
                    sounds['lapseSound'].play(1)
                    updateMap = True
                    screenSelect['main'][0] = False
                    screenSelect['map'][0] = True
                    data, distanceLateral, penalties, delivered = [
                        [], [], []], [[], [], []], [[], [], []], [[], [], []]
                    dataCpu, distanceLateralCpu, penaltiesCpu, deliveredCpu = [
                        [], [], []], [[], [], []], [[], [], []], [[], [], []]
                    timeActually = round(pg.time.get_ticks()/1000)
                    secLapseScreen = 0
                    y = width
        elif screenSelect['map'][0]:
            if timeActually != round(pg.time.get_ticks()/1000):
                timeActually += 1
                secLapseScreen += 1
            if secLapseScreen < 2:
                screen.blit(lapse, (y, 0))
                if y > 0:
                    y -= 180
            elif secLapseScreen < 4:
                screenSelect['map'][1].update()
                screen.blit(lapse, (y, 0))
                if y > -1080:
                    y -= 100
            elif secLapseScreen < 9:
                screenSelect['map'][1].update()
            else:
                timeActually = round(pg.time.get_ticks()/1000)
                secLapseScreen = 0
                y = width
                sounds['lapseSound'].play(1)
                houseI = 0
                timeAux = 0
                newGame = True
                screenSelect['map'][0] = False
                screenSelect['game'][0] = True
        elif screenSelect['game'][0]:
            if timeActually != round(pg.time.get_ticks()/1000):
                timeActually += 1
                secLapseScreen += 1
            if secLapseScreen < 2:
                screen.blit(lapse, (y, 0))
                if y > 0:
                    y -= 180
            elif secLapseScreen < 4:
                screenSelect['game'][1].update(events)
                screen.blit(lapse, (y, 0))
                if y > -1080:
                    y -= 220
            else:
                if timeAux == 0:
                    timeAux = round(pg.time.get_ticks()/1000)
                if pg.mixer.music.get_pos() == -1:
                    pg.mixer.music.load('sounds/wav/scene_60sec.wav')
                    pg.mixer.music.set_volume(0.5)
                    pg.mixer.music.play(3)
                screenSelect['game'][1].update(events)
                if houseI == 3:
                    pg.mixer.music.stop()
                    sounds['lapseSound'].play(1)
                    newUpdate = True
                    screenSelect['game'][0] = False
                    screenSelect['mapResult'][0] = True
                    timeActually = round(pg.time.get_ticks()/1000)
                    secLapseScreen = 0
                    y = width
        elif screenSelect['mapResult'][0]:
            if timeActually != round(pg.time.get_ticks()/1000):
                timeActually += 1
                secLapseScreen += 1
            if secLapseScreen < 2:
                screen.blit(lapse, (y, 0))
                if y > 0:
                    y -= 180
            elif secLapseScreen < 4:
                screenSelect['map'][1].update()
                screen.blit(lapse, (y, 0))
                if y > -1080:
                    y -= 220
            elif secLapseScreen < 9:
                screenSelect['map'][1].update()
            else:
                timeActually = round(pg.time.get_ticks()/1000)
                secLapseScreen = 0
                y = width
                sounds['lapseSound'].play(1)
                screenSelect['mapResult'][0] = False
                screenSelect['scoreBoard'][0] = True
        else:
            if timeActually != round(pg.time.get_ticks()/1000):
                timeActually += 1
                secLapseScreen += 1
            if secLapseScreen < 2:
                screen.blit(lapse, (y, 0))
                if y > 0:
                    y -= 180
            elif secLapseScreen < 4:
                screenSelect['scoreBoard'][1].update(events)
                screen.blit(lapse, (y, 0))
                if y > -1080:
                    y -= 220
            else:
                screenSelect['scoreBoard'][1].update(events)
        clock.tick(fps)
        pg.display.flip()


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()

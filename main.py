from cmu_112_graphics import * 
from characterCode import *
from helpfulFunctions import *
from itemCode import *
from testFunctions import *
#from draw import *
from combatCode import * 
from mapCode import * 
import random, threading, ctypes, time, wave
#from pydub import AudioSegment
#from pydub.playback import play
#cd "d:/Google Drive/Ze Ultimate Folder/CMU 2020-2021 (Fall)/Programming and Comp Sci/Homework/week4"


        
        
def appStarted(app):
    #Movement Variables
    app.charX = app.width / 2
    app.charY = app.height / 2
    app.speed = 5

    app.charAnimations, app.charStats = getCharacters()
    app.charWidth = app.width // 3
    app.charHeight = app.height // 3
    app.currChar = 'char0'

    app.timerDelay = 500
    getAppState(app)
    resetAnimations(app)


    app.weaponItems = getWeaponItems()
    app.equippedWeapon = app.weaponItems['sword']
    app.armorItems = getArmorItems()     
    app.junkItems = getJunkItems()
    getItemDrops(app)

    app.mapCreationOffset = app.height / 6
    pass

def resetAnimations(app):

    app.normalMove = False
    app.charAttack = False
    app.pickUp = False
    app.idle = True
    defineMoveType(app)
    app.charAnimCount = 0
    app.currFrame = 0

def keyPressed(app, event):
    if app.testingMode:
        audioThread.testFunc()
    if app.isPaused:
        if event.key == 'p':
            app.isPaused = not app.isPaused
        return
    if app.isDeath:
        return
    if app.charSelect:
        return
    if app.normalPlay:
        dx = 0
        dy = 0
        if event.key == 'w':
            dy -= app.speed
            app.normalMove = True
            app.charStats['dirFaced'] = 'up'
            defineMoveType(app)
        if event.key == 's':
            dy += app.speed
            app.normalMove = True
            app.charStats['dirFaced'] = 'down'
            defineMoveType(app)
        if event.key == 'd':
            dx += app.speed
            app.normalMove = True
            app.charStats['dirFaced'] = 'left'
            defineMoveType(app)
        if event.key == 'a':
            dx -= app.speed
            app.normalMove = True
            app.charStats['dirFaced'] = 'right'
            defineMoveType(app)
        if event.key == 'p':
            app.pickUp = not app.pickUp
            app.i = 0
            app.currFrame = 0
            defineMoveType(app)

        makeMove(app, dx, dy)

def mousePressed(app, event):
    if app.mapCreation:
        if event.y > app.mapCreationOffset:
            if event.x < app.width / 3:
                app.size = 'small'
            elif event.x < app.width * 2 / 3:
                app.size = 'medium'
            else:
                app.size = 'large'
        generateMapApp(app)

    if app.normalPlay:
        app.charAttack = not app.charAttack
        app.i = 0
        app.currFrame = 0
        defineMoveType(app)
        destroyed = attack(app)
        for elem in destroyed:
            if isinstance(elem, tuple):
                app.map.generatedMap[app.mapRow][app.mapCol].obstacles.remove(elem)
            else:
                print(elem)
                app.map.generatedMap[app.mapRow][app.mapCol].enemies.remove(elem)

def defineMoveType(app):
    if app.pickUp:
        app.moveType = 'pickUp'
    elif app.charAttack:
        app.moveType = 'attack'
    elif app.normalMove:
        app.moveType = 'normalMove'
    else:
        app.moveType = 'idle'

def makeMove(app, dx, dy):
    if (app.charX > app.width or app.charX < 0 or app.charY > app.height   
        or app.charY < 0):
        return
    app.charX += dx
    app.charY += dy
        
def itemDrop(app):
    itemProbability = random.randint(0, 100)
    if itemProbability < (100 - app.uncommonProbability - app.rareProbability):
        item = random.choice(app.drops['junk'])
        app.uncommonProbability += 5
        app.rareProbability += 1
    elif itemProbability < (100 - app.rareProbability):
        item = random.choice(app.drops['uncommon'])
        app.uncommonProbability = 25
        app.rareProbability += 1
    else:
        item = random.choice(app.drops['rare'])
        app.uncommonProbability = 25
        app.rareProbability = 5
    return item

def timerFired(app):
    if app.normalPlay:
        charAnimation(app)
        enemAnimation(app)


def charAnimation(app):
    if app.charAnimCount >= len(app.charAnimations[app.currChar][app.moveType]):
        resetAnimations(app)
        defineMoveType(app)
    app.currFrame = (app.charAnimCount % len(app.charAnimations[app.currChar][app.moveType]))
    app.charAnimCount += 1

def enemAnimation(app):
    for enemy in app.map.generatedMap[app.mapRow][app.mapCol].enemies:
        if enemy.currFrame >= len(enemy.frames[enemy.moveType]) - 1:
            enemy.reset()
        else:
            enemy.currFrame += 1


def redrawAll(app, canvas):
    if app.mapCreation:
        drawMapCreationScreen(app, canvas)
    if app.normalPlay:
        drawMap(app, canvas)
        drawEnemies(app, canvas)
        drawFigure(app, canvas)

def drawMapCreationScreen(app, canvas):
    canvas.create_rectangle(0, app.mapCreationOffset, app.width / 3, app.height)
    canvas.create_rectangle(app.width / 3, app.mapCreationOffset, app.width * 2 / 3, app.height)
    canvas.create_rectangle(app.width * 2 / 3, app.mapCreationOffset, app.width, app.height)
    canvas.create_line(0, app.mapCreationOffset, app.width, app.mapCreationOffset)
    canvas.create_text(app.width / 2, app.mapCreationOffset / 2,
                        text = 'Map Creator',
                        font = 'Arial 20 bold')
    canvas.create_text(app.width / 6, (app.height + app.mapCreationOffset) / 2,
                        text = 'Small Map!')
    canvas.create_text(app.width / 2, (app.height + app.mapCreationOffset) / 2,
                        text = 'Medium Map!')
    canvas.create_text(app.width * 5/ 6, (app.height + app.mapCreationOffset) / 2,
                        text = 'Large Map!')
def drawFigure(app, canvas):
#    pilImage = PIL.Image.open(app.charAnimations[app.currChar][app.moveType][app.currFrame])
#    resizedImage = pilImage.resize((app.charWidth, app.charHeight))
    image = ImageTk.PhotoImage(app.charAnimations[app.currChar][app.moveType][app.currFrame])
    imagesprite = canvas.create_image(app.charX, app.charY, image = image)

def drawMap(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'green')
    for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
        image = ImageTk.PhotoImage(obstacle.imageFile)
        canvas.create_image(x, y, image = image)

def drawEnemies(app, canvas):
    for enemy in app.map.generatedMap[app.mapRow][app.mapCol].enemies:
        image = ImageTk.PhotoImage(enemy.frames[enemy.moveType][enemy.currFrame])
        canvas.create_image(enemy.x, enemy.y, image = image)
        print(image, enemy.currFrame)

        
'''
class audioThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.test = False
    def run(self):
        song = wave.open('song.wav', 'rb')
        print('here')
        chunk = 1024
        p = pyaudio.PyAudio
        print(song.getsampwidth())
        stream = p.open(format = p.get_format_from_width(song.getsampwidth()),#Ask about this later
                        channels = song.getnchannels(),
                        rate = song.getframerate(),
                        output = True)
        data = song.readframes(chunk)
        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)
        stream.close()

    def testFunc(self):
        print('tested')
        self.test = True

audioThread = audioThread(2)
audioThread.start()'''
runApp(width = 1000, height = 1000)
time.sleep(2)

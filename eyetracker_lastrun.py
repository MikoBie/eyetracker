#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.5),
    on Mon Feb  6 10:42:58 2023
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from code
import remote_annotations as ra
import time
import random

ip_address = '127.0.0.1'
port = 50020
# 1. Setup network connection
capture_exisits = ra.check_capture_exists(ip_address, port)
if capture_exisits:
    pupil_remote, pub_socket = ra.setup_pupil_remote_connection(ip_address, port)

    # 2. Setup local clock function
    local_clock = time.perf_counter

    # 3. Measure clock offset accounting for network latency
    stable_offset_mean = ra.measure_clock_offset_stable(
        pupil_remote, clock_function=local_clock, n_samples=10
    )

    pupil_time_actual = ra.request_pupil_time(pupil_remote)
    local_time_actual = local_clock()
    pupil_time_calculated_locally = local_time_actual + stable_offset_mean

    ra.notify(pupil_remote,{"subject": "start_plugin", "name": "Annotation_Capture", "args": {}},)

    # start a recording (necessary for this example script)
    pupil_remote.send_string("R")
    pupil_remote.recv_string()



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.5'
expName = 'eyetracker'  # from the Builder filename that created this script
expInfo = {
    'participant': '',
    'płeć': ['kobieta', 'mężczyzna'],
    'wiek': '',
}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/mikolaj/Desktop/eyetracker/eyetracker_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup eyetracking
ioConfig['eyetracker.hw.pupil_labs.pupil_core.EyeTracker'] = {
    'name': 'tracker',
    'runtime_settings': {
        'pupillometry_only': False,
        'surface_name': 'dell',
        'gaze_confidence_threshold': 0.6,
        'pupil_remote': {
            'ip_address': '127.0.0.1',
            'port': 50020.0,
            'timeout_ms': 1000.0,
        },
        'pupil_capture_recording': {
            'enabled': True,
            'location': '',
        }
    }
}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = ioServer.getDevice('tracker')

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# --- Initialize components for Routine "instruction" ---
space = visual.TextStim(win=win, name='space',
    text='Naciśnij spację, żeby przejść dalej',
    font='Open Sans',
    pos=(0, -.4), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
space_resp = keyboard.Keyboard()
welcome_message = visual.TextBox2(
     win, text='Cześć,\n \ndziękujemy, że zgodziłaś/eś się wziąć udział w badaniu. Jesteśmy zespołem naukowców i naukowczyń z Instytutu Studiów Społecznych im. prof. Roberta Zajonca na Uniwersytecie Warszawskim i prowadzimy badania nad decyzjami konsumenckimi.\nPrzechodząc dalej wyrażasz zgodę na udział w badaniu. Będzie ono trwało około 10 minut i składało się z dwóch części. Podczas trwania całego badania będziemy monitorować ruchy Twoich gałek ocznych. Sposób zbierania tych danych nie tworzy zagrożenia dla Twojego wzroku, ani innych ryzyk zdrowotnych. Gdybyś jednak poczuł/a się źle, poinformuj o tym badacza lub badaczkę. Pamiętaj, że w każdej chwili masz prawo zrezygnować z udziału z badania bez podania przyczyny.', font='Open Sans',
     pos=(-.8, .4),     letterHeight=0.04,
     size=(1.6, .5), borderWidth=2.0,
     color='white', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=1.0,
     padding=0.0, alignment='top-left',
     anchor='top-left',
     fillColor=None, borderColor=None,
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=False,
     name='welcome_message',
     autoLog=True,
)

# --- Initialize components for Routine "trust_manipulation" ---
space2 = visual.TextStim(win=win, name='space2',
    text='Naciśnij spację, żeby przejść dalej',
    font='Open Sans',
    pos=(0, -.4), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
trust_instruction = visual.TextBox2(
     win, text='', font='Open Sans',
     pos=(-.8, .4),     letterHeight=0.04,
     size=(1.6, .5), borderWidth=2.0,
     color='white', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=1.0,
     padding=0.0, alignment='top-left',
     anchor='top-left',
     fillColor=None, borderColor=None,
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=False,
     name='trust_instruction',
     autoLog=True,
)
space2_resp = keyboard.Keyboard()
# Run 'Begin Experiment' code from trust
if int(expInfo['participant']) % 2 == 0:
    trust = """Za chwilę na ekranie komputera pojawią się informacje o czterech produktach, które poprosilibyśmy Cię, żebyś ocenił/a. Zostały one wystawione na sprzedaż na popularnym serwisie aukcyjnym, który cieszy się dobrą renomą. Użytkownicy i użytkowniczki wysoko oceniają obsługę klienta serwisu, która w razie jakichkolwiek problemów z transakcją służy pomocą. Dodatkowo uczciwe i szczere opinie użytkowników i użytkowniczek na temat wad i zalet produktów ułatwiają klientom i klientkom podejmowanie decyzji."""
else:
    trust = """Za chwilę na ekranie komputera pojawią się informacje o czterech produktach, które poprosilibyśmy Cię, żebyś ocenił/a. Zostały one wystawione na sprzedaż na popularnym serwisie aukcyjnym, który cieszy się szemraną opinią. Użytkownicy i użytkowniczki nisko oceniają obsługę klienta serwisu, która często nie odpowiada na prośby o interwencję. Dodatkowo często zdarza się, że opinie prezentowane przez użytkowników i użytkowniczki serwisu na temat produktów mają jedynie zachęcić do kupna a nie zawsze prawdziwie opisują wady i zalety projektu."""

# --- Initialize components for Routine "products_display" ---
stimulus = visual.ImageStim(
    win=win,
    name='stimulus', units='height', 
    image='sin', mask=None, anchor='top-center',
    ori=0.0, pos=(0, 0.4), size=(0.25,0.25),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
text = visual.TextStim(win=win, name='text',
    text='',
    font='Open Sans',
    pos=(0, .1), height=0.03, wrapWidth=50.0, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
left_text = visual.TextBox2(
     win, text='', font='Open Sans',
     pos=(-.6, 0),     letterHeight=0.02,
     size=(.5, 1), borderWidth=2.0,
     color='white', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=1.0,
     padding=0.0, alignment='top-left',
     anchor='top-center',
     fillColor=None, borderColor=None,
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=False,
     name='left_text',
     autoLog=True,
)
right_text = visual.TextBox2(
     win, text='', font='Open Sans',
     pos=(.6, 0),     letterHeight=0.02,
     size=(.5, 1), borderWidth=2.0,
     color='white', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=1.0,
     padding=0.0, alignment='top-left',
     anchor='top-center',
     fillColor=None, borderColor=None,
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=False,
     name='right_text',
     autoLog=True,
)
left_title = visual.TextStim(win=win, name='left_title',
    text='',
    font='Open Sans',
    pos=(-.6, 0.05), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);
right_title = visual.TextStim(win=win, name='right_title',
    text='',
    font='Open Sans',
    pos=(.6, 0.05), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);

# --- Initialize components for Routine "ratings" ---
key_resp_2 = keyboard.Keyboard()
textbox = visual.TextBox2(
     win, text='Na ile gwiazdek w skali od 1 do 5 oceniłabyś/oceniłbyś prezentowany przed chwilą produkt?\n\n\nWybierz na klawiturze numerycznej liczbę gwiazdek i naciśnij odpowiedni klawisz.', font='Open Sans',
     pos=(0, 0),     letterHeight=0.05,
     size=(1.5, 1), borderWidth=2.0,
     color='white', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=1.0,
     padding=0.0, alignment='center',
     anchor='center',
     fillColor=None, borderColor=None,
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=False,
     name='textbox',
     autoLog=True,
)

# --- Initialize components for Routine "end" ---
text_instr = visual.TextStim(win=win, name='text_instr',
    text='Dziękujemy za udział w badaniu!',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_3 = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "instruction" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
space_resp.keys = []
space_resp.rt = []
_space_resp_allKeys = []
welcome_message.reset()
# keep track of which components have finished
instructionComponents = [space, space_resp, welcome_message]
for thisComponent in instructionComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "instruction" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *space* updates
    if space.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        space.frameNStart = frameN  # exact frame index
        space.tStart = t  # local t and not account for scr refresh
        space.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(space, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'space.started')
        space.setAutoDraw(True)
    
    # *space_resp* updates
    waitOnFlip = False
    if space_resp.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
        # keep track of start time/frame for later
        space_resp.frameNStart = frameN  # exact frame index
        space_resp.tStart = t  # local t and not account for scr refresh
        space_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(space_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'space_resp.started')
        space_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(space_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(space_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if space_resp.status == STARTED and not waitOnFlip:
        theseKeys = space_resp.getKeys(keyList=['space'], waitRelease=False)
        _space_resp_allKeys.extend(theseKeys)
        if len(_space_resp_allKeys):
            space_resp.keys = _space_resp_allKeys[-1].name  # just the last key pressed
            space_resp.rt = _space_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *welcome_message* updates
    if welcome_message.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        welcome_message.frameNStart = frameN  # exact frame index
        welcome_message.tStart = t  # local t and not account for scr refresh
        welcome_message.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(welcome_message, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'welcome_message.started')
        welcome_message.setAutoDraw(True)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "instruction" ---
for thisComponent in instructionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "instruction" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "trust_manipulation" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
trust_instruction.reset()
trust_instruction.setText(trust
)
space2_resp.keys = []
space2_resp.rt = []
_space2_resp_allKeys = []
# keep track of which components have finished
trust_manipulationComponents = [space2, trust_instruction, space2_resp]
for thisComponent in trust_manipulationComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "trust_manipulation" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *space2* updates
    if space2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        space2.frameNStart = frameN  # exact frame index
        space2.tStart = t  # local t and not account for scr refresh
        space2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(space2, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'space2.started')
        space2.setAutoDraw(True)
    
    # *trust_instruction* updates
    if trust_instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        trust_instruction.frameNStart = frameN  # exact frame index
        trust_instruction.tStart = t  # local t and not account for scr refresh
        trust_instruction.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(trust_instruction, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'trust_instruction.started')
        trust_instruction.setAutoDraw(True)
    
    # *space2_resp* updates
    waitOnFlip = False
    if space2_resp.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
        # keep track of start time/frame for later
        space2_resp.frameNStart = frameN  # exact frame index
        space2_resp.tStart = t  # local t and not account for scr refresh
        space2_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(space2_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'space2_resp.started')
        space2_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(space2_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(space2_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if space2_resp.status == STARTED and not waitOnFlip:
        theseKeys = space2_resp.getKeys(keyList=['space'], waitRelease=False)
        _space2_resp_allKeys.extend(theseKeys)
        if len(_space2_resp_allKeys):
            space2_resp.keys = _space2_resp_allKeys[-1].name  # just the last key pressed
            space2_resp.rt = _space2_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in trust_manipulationComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "trust_manipulation" ---
for thisComponent in trust_manipulationComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if space2_resp.keys in ['', [], None]:  # No response was made
    space2_resp.keys = None
thisExp.addData('space2_resp.keys',space2_resp.keys)
if space2_resp.keys != None:  # we had a response
    thisExp.addData('space2_resp.rt', space2_resp.rt)
thisExp.nextEntry()
# the Routine "trust_manipulation" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('conditions/conditions.xlsx'),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial:
        exec('{} = thisTrial[paramName]'.format(paramName))

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "products_display" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    stimulus.setImage(image)
    text.setText(price)
    left_text.reset()
    right_text.reset()
    # Run 'Begin Routine' code from code
    left = 'FAKTY'
    right = 'OPINIE'
    if random.randint(0,1):
        opinions, facts = facts, opinions
        left, right = right, left
    
    if capture_exisits:
        local_time = local_clock()
        label = product + '_' + left + '_start'
        minimal_trigger = ra.new_trigger(label, local_time + stable_offset_mean)
        ra.send_trigger(pub_socket, minimal_trigger)
    
    
    # keep track of which components have finished
    products_displayComponents = [stimulus, text, left_text, right_text, left_title, right_title]
    for thisComponent in products_displayComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "products_display" ---
    while continueRoutine and routineTimer.getTime() < 15.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimulus* updates
        if stimulus.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            stimulus.frameNStart = frameN  # exact frame index
            stimulus.tStart = t  # local t and not account for scr refresh
            stimulus.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stimulus, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stimulus.started')
            stimulus.setAutoDraw(True)
        if stimulus.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > stimulus.tStartRefresh + 15-frameTolerance:
                # keep track of stop time/frame for later
                stimulus.tStop = t  # not accounting for scr refresh
                stimulus.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stimulus.stopped')
                stimulus.setAutoDraw(False)
        
        # *text* updates
        if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text.started')
            text.setAutoDraw(True)
        if text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text.tStartRefresh + 15-frameTolerance:
                # keep track of stop time/frame for later
                text.tStop = t  # not accounting for scr refresh
                text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text.stopped')
                text.setAutoDraw(False)
        
        # *left_text* updates
        if left_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            left_text.frameNStart = frameN  # exact frame index
            left_text.tStart = t  # local t and not account for scr refresh
            left_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(left_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'left_text.started')
            left_text.setAutoDraw(True)
        if left_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > left_text.tStartRefresh + 15-frameTolerance:
                # keep track of stop time/frame for later
                left_text.tStop = t  # not accounting for scr refresh
                left_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'left_text.stopped')
                left_text.setAutoDraw(False)
        if left_text.status == STARTED:  # only update if drawing
            left_text.setText(facts, log=False)
        
        # *right_text* updates
        if right_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            right_text.frameNStart = frameN  # exact frame index
            right_text.tStart = t  # local t and not account for scr refresh
            right_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(right_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'right_text.started')
            right_text.setAutoDraw(True)
        if right_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > right_text.tStartRefresh + 15-frameTolerance:
                # keep track of stop time/frame for later
                right_text.tStop = t  # not accounting for scr refresh
                right_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'right_text.stopped')
                right_text.setAutoDraw(False)
        if right_text.status == STARTED:  # only update if drawing
            right_text.setText(opinions, log=False)
        
        # *left_title* updates
        if left_title.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            left_title.frameNStart = frameN  # exact frame index
            left_title.tStart = t  # local t and not account for scr refresh
            left_title.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(left_title, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'left_title.started')
            left_title.setAutoDraw(True)
        if left_title.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > left_title.tStartRefresh + 15-frameTolerance:
                # keep track of stop time/frame for later
                left_title.tStop = t  # not accounting for scr refresh
                left_title.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'left_title.stopped')
                left_title.setAutoDraw(False)
        if left_title.status == STARTED:  # only update if drawing
            left_title.setText(left, log=False)
        
        # *right_title* updates
        if right_title.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            right_title.frameNStart = frameN  # exact frame index
            right_title.tStart = t  # local t and not account for scr refresh
            right_title.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(right_title, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'right_title.started')
            right_title.setAutoDraw(True)
        if right_title.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > right_title.tStartRefresh + 15-frameTolerance:
                # keep track of stop time/frame for later
                right_title.tStop = t  # not accounting for scr refresh
                right_title.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'right_title.stopped')
                right_title.setAutoDraw(False)
        if right_title.status == STARTED:  # only update if drawing
            right_title.setText(right, log=False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in products_displayComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "products_display" ---
    for thisComponent in products_displayComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code
    if capture_exisits:
        local_time = local_clock()
        label = product + '_' + left + '_end'
        minimal_trigger = ra.new_trigger(label, local_time + stable_offset_mean)
        ra.send_trigger(pub_socket, minimal_trigger)
    
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-15.000000)
    
    # --- Prepare to start Routine "ratings" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    key_resp_2.keys = []
    key_resp_2.rt = []
    _key_resp_2_allKeys = []
    textbox.reset()
    # keep track of which components have finished
    ratingsComponents = [key_resp_2, textbox]
    for thisComponent in ratingsComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "ratings" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *key_resp_2* updates
        waitOnFlip = False
        if key_resp_2.status == NOT_STARTED and tThisFlip >= .5-frameTolerance:
            # keep track of start time/frame for later
            key_resp_2.frameNStart = frameN  # exact frame index
            key_resp_2.tStart = t  # local t and not account for scr refresh
            key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_2.started')
            key_resp_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_2.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_2.getKeys(keyList=['1','2','3','4','5'], waitRelease=False)
            _key_resp_2_allKeys.extend(theseKeys)
            if len(_key_resp_2_allKeys):
                key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
                key_resp_2.rt = _key_resp_2_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # *textbox* updates
        if textbox.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            textbox.frameNStart = frameN  # exact frame index
            textbox.tStart = t  # local t and not account for scr refresh
            textbox.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(textbox, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'textbox.started')
            textbox.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in ratingsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "ratings" ---
    for thisComponent in ratingsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_2.keys in ['', [], None]:  # No response was made
        key_resp_2.keys = None
    trials.addData('key_resp_2.keys',key_resp_2.keys)
    if key_resp_2.keys != None:  # we had a response
        trials.addData('key_resp_2.rt', key_resp_2.rt)
    # the Routine "ratings" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'trials'


# --- Prepare to start Routine "end" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
key_resp_3.keys = []
key_resp_3.rt = []
_key_resp_3_allKeys = []
# keep track of which components have finished
endComponents = [text_instr, key_resp_3]
for thisComponent in endComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "end" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_instr* updates
    if text_instr.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_instr.frameNStart = frameN  # exact frame index
        text_instr.tStart = t  # local t and not account for scr refresh
        text_instr.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_instr, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_instr.started')
        text_instr.setAutoDraw(True)
    
    # *key_resp_3* updates
    waitOnFlip = False
    if key_resp_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_3.frameNStart = frameN  # exact frame index
        key_resp_3.tStart = t  # local t and not account for scr refresh
        key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_3, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'key_resp_3.started')
        key_resp_3.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_3.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_3.getKeys(keyList=['q'], waitRelease=False)
        _key_resp_3_allKeys.extend(theseKeys)
        if len(_key_resp_3_allKeys):
            key_resp_3.keys = _key_resp_3_allKeys[-1].name  # just the last key pressed
            key_resp_3.rt = _key_resp_3_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "end" ---
for thisComponent in endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_3.keys in ['', [], None]:  # No response was made
    key_resp_3.keys = None
thisExp.addData('key_resp_3.keys',key_resp_3.keys)
if key_resp_3.keys != None:  # we had a response
    thisExp.addData('key_resp_3.rt', key_resp_3.rt)
thisExp.nextEntry()
# the Routine "end" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
# Run 'End Experiment' code from code
if capture_exisits:
    # stop recording
    pupil_remote.send_string("r")
    pupil_remote.recv_string()


# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()

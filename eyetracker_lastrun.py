#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.5),
    on Fri Feb  3 13:24:45 2023
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

ip_address = '127.0.0.1'
port = 50020
# 1. Setup network connection
ra.check_capture_exists(ip_address, port)
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
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
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
instrukcja = visual.TextStim(win=win, name='instrukcja',
    text='Naciśnij spację, żeby przejść dalej',
    font='Open Sans',
    pos=(0, -.4), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp = keyboard.Keyboard()
textbox = visual.TextBox2(
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
     name='textbox',
     autoLog=True,
)

# --- Initialize components for Routine "highPrice" ---
stimulus = visual.ImageStim(
    win=win,
    name='stimulus', units='height', 
    image='png/laptop.png', mask=None, anchor='top-center',
    ori=0.0, pos=(0, 0.4), size=(0.25,0.25),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
text = visual.TextStim(win=win, name='text',
    text='2259 zł',
    font='Open Sans',
    pos=(0, .1), height=0.03, wrapWidth=50.0, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
left_text = visual.TextBox2(
     win, text='Posiada ekran o przekątnej 15.6" i wysokiej rozdzielczości. Matowa powłoka matrycy pozwala na korzystanie z komputera nawet przy dużym słońcu.\n\nWyposażony w dwurdzeniowy procesor.\n\nWbudowana pamięć RAM o pojemności 8 GB pozwala na uruchomienie kilku aplikacji jednocześnie oraz granie w wymagające sprzętowo gry komputerowe.\n\nDysk SSD o pojemności 256 GB \n\nŚlad węglowy: 423 kg', font='Open Sans',
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
     win, text='Bardzo dobre wykonanie, minimalistyczny wygląd, podoba mi się,  że nie ma zbędnych naklejek. Praca na nim przebiega płynnie, ekran rzeczywiście ładnie odwzorowuje kolory. Polecam!\n\nOgólnie spoko, szybko przyzwyczaiłam się do klawiatury, wentylator chodzi na tyle cicho, że mi nie przeszkadza, bateria starcza na tyle, ile powinna. Bardzo fajny laptop.\n\nUrządzenie w całości z tworzywa, jednak dobrze spasowane i sprawia wrażenie solidnego. Matryca i działanie na zadowalającym  poziomie. Bateria daje radę kiedy np. jestem w podróży :).', font='Open Sans',
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
    text='FAKTY:',
    font='Open Sans',
    pos=(-.6, 0.05), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);
right_title = visual.TextStim(win=win, name='right_title',
    text='OPINIE:',
    font='Open Sans',
    pos=(.6, 0.05), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);

# --- Initialize components for Routine "end" ---
text_instr = visual.TextStim(win=win, name='text_instr',
    text='Dziękujemy',
    font='Arial',
    pos=(-0.3, 0.25), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "instruction" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
key_resp.keys = []
key_resp.rt = []
_key_resp_allKeys = []
textbox.reset()
# keep track of which components have finished
instructionComponents = [instrukcja, key_resp, textbox]
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
    
    # *instrukcja* updates
    if instrukcja.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        instrukcja.frameNStart = frameN  # exact frame index
        instrukcja.tStart = t  # local t and not account for scr refresh
        instrukcja.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instrukcja, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'instrukcja.started')
        instrukcja.setAutoDraw(True)
    
    # *key_resp* updates
    waitOnFlip = False
    if key_resp.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
        # keep track of start time/frame for later
        key_resp.frameNStart = frameN  # exact frame index
        key_resp.tStart = t  # local t and not account for scr refresh
        key_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'key_resp.started')
        key_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp.status == STARTED and not waitOnFlip:
        theseKeys = key_resp.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_allKeys.extend(theseKeys)
        if len(_key_resp_allKeys):
            key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
            key_resp.rt = _key_resp_allKeys[-1].rt
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

# --- Prepare to start Routine "highPrice" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
left_text.reset()
right_text.reset()
# Run 'Begin Routine' code from code
local_time = local_clock()
label = "high price start"
minimal_trigger = ra.new_trigger(label, local_time + stable_offset_mean)
ra.send_trigger(pub_socket, minimal_trigger)

# keep track of which components have finished
highPriceComponents = [stimulus, text, left_text, right_text, left_title, right_title]
for thisComponent in highPriceComponents:
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

# --- Run Routine "highPrice" ---
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
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in highPriceComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "highPrice" ---
for thisComponent in highPriceComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# Run 'End Routine' code from code
local_time = local_clock()
label = "high price end"
minimal_trigger = ra.new_trigger(label, local_time + stable_offset_mean)
ra.send_trigger(pub_socket, minimal_trigger)

# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-15.000000)

# --- Prepare to start Routine "end" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# keep track of which components have finished
endComponents = [text_instr]
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
while continueRoutine and routineTimer.getTime() < 5.0:
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
    if text_instr.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_instr.tStartRefresh + 5-frameTolerance:
            # keep track of stop time/frame for later
            text_instr.tStop = t  # not accounting for scr refresh
            text_instr.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_instr.stopped')
            text_instr.setAutoDraw(False)
    
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
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-5.000000)
# Run 'End Experiment' code from code
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

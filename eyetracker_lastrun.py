#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.5),
    on Thu Mar  2 19:17:03 2023
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
from utils import remote_annotations as ra
import time

## Default values
ip_address = '127.0.0.1'
port = 50020
left = 'FAKTY'
right = 'OPINIE'
# 1. Setup network connection
capture_exists = ra.check_capture_exists(ip_address, port)
local_clock = time.perf_counter

## Check whether Pupil Core is connected.
if capture_exists:
    pupil_remote, pub_socket = ra.setup_pupil_remote_connection(ip_address, port)

    ## 2. Setup local clock function
    local_clock = time.perf_counter

    ## 3. Measure clock offset accounting for network latency
    stable_offset_mean = ra.measure_clock_offset_stable(
        pupil_remote, clock_function=local_clock, n_samples=10
    )
    pupil_time_actual = ra.request_pupil_time(pupil_remote)
    local_time_actual = local_clock()
    pupil_time_calculated_locally = local_time_actual + stable_offset_mean
    
    ## 4. Start the annotation plugin
    ra.notify(pupil_remote,{"subject": "start_plugin", "name": "Annotation_Capture", "args": {}},)

    


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
    savePickle=True, saveWideText=False,
    dataFileName=filename)
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
     name='welcome_message',
     autoLog=True,
)
# Run 'Begin Experiment' code from code_3
## Depending on the sex of the participant it 
## either loads the instruction for females or
## males.
with open('materials/instruction.txt', encoding="utf-8") as file:
    instruction_list = file.readlines()
if expInfo['płeć'] == 'kobieta':
    inst_text = instruction_list[0].replace(';','\n\n')
else:
    inst_text = instruction_list[1].replace(';','\n\n')

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
## Assigns the participant to the trust condition.
## If the id is even the participant is assigned
## to the trust condition. Oterwise to untrustworthy.
## Additionally, it reads relevant instruction
## either for females or males.
if int(expInfo['participant']) % 2 == 0:
    with open('materials/trust.txt', encoding="utf-8") as file:
        trust_list = file.readlines()
    if expInfo['płeć'] == 'kobieta':
        trust = trust_list[0]
    else:
        trust = trust_list[1]
else:
    with open('materials/untrust.txt', encoding="utf-8") as file:
        trust_list = file.readlines()
    if expInfo['płeć'] == 'kobieta':
        trust = trust_list[0]
    else:
        trust = trust_list[1]

# --- Initialize components for Routine "products_display" ---
stimulus = visual.ImageStim(
    win=win,
    name='stimulus', units='norm', 
    image='sin', mask=None, anchor='top-center',
    ori=0.0, pos=(0, 0.9), size=(0.525,0.7),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
text = visual.TextStim(win=win, name='text',
    text='',
    font='Open Sans',
    units='norm', pos=(0, 0.05), height=0.05, wrapWidth=50.0, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
left_text = visual.TextBox2(
     win, text='', font='Open Sans',
     pos=(-.5, -0.15),units='norm',     letterHeight=0.04,
     size=(.8, 1), borderWidth=2.0,
     color='white', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=0.8,
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
     pos=(.5, -0.15),units='norm',     letterHeight=0.04,
     size=(.8, 1), borderWidth=2.0,
     color='white', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=0.8,
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
    units='norm', pos=(-.5, -0.05), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);
right_title = visual.TextStim(win=win, name='right_title',
    text='',
    font='Open Sans',
    units='norm', pos=(.5, -0.05), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);
# Run 'Begin Experiment' code from code
## Check whether Puil Core is connected
if capture_exists:
    ## start a recording (necessary for this example script)
    pupil_remote.send_string("R")
    pupil_remote.recv_string()


# --- Initialize components for Routine "ratings" ---
textbox = visual.TextBox2(
     win, text='Na ile gwiazdek w skali od 1 do 5 oceniłabyś/oceniłbyś prezentowany przed chwilą produkt? Najedź kursorem na rząd z wybraną liczbą gwiazdek i naciśnij lewy klawisz myszy.\n', font='Open Sans',
     pos=(0, .4),     letterHeight=0.05,
     size=(1.5, .2), borderWidth=2.0,
     color='white', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=1.0,
     padding=0.0, alignment='center-left',
     anchor='top-center',
     fillColor=None, borderColor=None,
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=False,
     name='textbox',
     autoLog=True,
)
stars = visual.ImageStim(
    win=win,
    name='stars', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.5, 0.1), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
stars_2_1 = visual.ImageStim(
    win=win,
    name='stars_2_1', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.5, 0), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
stars_2_2 = visual.ImageStim(
    win=win,
    name='stars_2_2', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.4, 0), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)
stars_3_1 = visual.ImageStim(
    win=win,
    name='stars_3_1', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.5, -.1), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-4.0)
stars_3_2 = visual.ImageStim(
    win=win,
    name='stars_3_2', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.4, -.1), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-5.0)
stars_3_3 = visual.ImageStim(
    win=win,
    name='stars_3_3', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.3, -.1), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-6.0)
stars_4_1 = visual.ImageStim(
    win=win,
    name='stars_4_1', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.5, -.2), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-7.0)
stars_4_2 = visual.ImageStim(
    win=win,
    name='stars_4_2', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.4, -.2), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-8.0)
stars_4_3 = visual.ImageStim(
    win=win,
    name='stars_4_3', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.3, -.2), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-9.0)
stars_4_4 = visual.ImageStim(
    win=win,
    name='stars_4_4', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.2, -.2), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-10.0)
stars_5_1 = visual.ImageStim(
    win=win,
    name='stars_5_1', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.5, -.3), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-11.0)
stars_5_2 = visual.ImageStim(
    win=win,
    name='stars_5_2', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.4, -.3), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-12.0)
stars_5_3 = visual.ImageStim(
    win=win,
    name='stars_5_3', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.3, -.3), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-13.0)
stars_5_4 = visual.ImageStim(
    win=win,
    name='stars_5_4', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.2, -.3), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-14.0)
stars_5_5 = visual.ImageStim(
    win=win,
    name='stars_5_5', 
    image='png/stars.png', mask=None, anchor='center',
    ori=0.0, pos=(-.1, -.3), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-15.0)
star_1 = visual.ButtonStim(win, 
    text=None, font='Arvo',
    pos=(-.5, .1),
    letterHeight=0.05,
    size=(.1,.1), borderWidth=0.0,
    fillColor=None, borderColor=None,
    color=None, colorSpace='rgb',
    opacity=None,
    bold=True, italic=False,
    padding=None,
    anchor='center',
    name='star_1'
)
star_1.buttonClock = core.Clock()
star_2 = visual.ButtonStim(win, 
    text=None, font='Arvo',
    pos=(-.45, 0),
    letterHeight=0.05,
    size=(.2,.1), borderWidth=0.0,
    fillColor=None, borderColor=None,
    color=None, colorSpace='rgb',
    opacity=None,
    bold=True, italic=False,
    padding=None,
    anchor='center',
    name='star_2'
)
star_2.buttonClock = core.Clock()
star_3 = visual.ButtonStim(win, 
    text=None, font='Arvo',
    pos=(-.4, -.1),
    letterHeight=0.05,
    size=(.3,.1), borderWidth=0.0,
    fillColor=None, borderColor=None,
    color=None, colorSpace='rgb',
    opacity=None,
    bold=True, italic=False,
    padding=None,
    anchor='center',
    name='star_3'
)
star_3.buttonClock = core.Clock()
star_4 = visual.ButtonStim(win, 
    text=None, font='Arvo',
    pos=(-.35, -.2),
    letterHeight=0.05,
    size=(.4,.1), borderWidth=0.0,
    fillColor=None, borderColor=None,
    color=None, colorSpace='rgb',
    opacity=None,
    bold=True, italic=False,
    padding=None,
    anchor='center',
    name='star_4'
)
star_4.buttonClock = core.Clock()
star_5 = visual.ButtonStim(win, 
    text=None, font='Arvo',
    pos=(-.3, -.3),
    letterHeight=0.05,
    size=(.5,.1), borderWidth=0.0,
    fillColor=None, borderColor=None,
    color=None, colorSpace='rgb',
    opacity=None,
    bold=True, italic=False,
    padding=None,
    anchor='center',
    name='star_5'
)
star_5.buttonClock = core.Clock()
# Run 'Begin Experiment' code from code_2
## Initilize number of clicks to 0
star_1_num_clicks = star_2_num_clicks = star_3_num_clicks = star_4_num_clicks = star_5_num_clicks = 0

## Initilize the order of condition variable
condition_order = 1

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
welcome_message.setText(inst_text)
# Run 'Begin Routine' code from code_3
## Makes the cursor of the mause invisible.
win.mouseVisible = False
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
    trialList=data.importConditions('materials/conditions.xlsx'),
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
    ## Randomize whether facts will be displayed on the
    ## left or right side of the screen.
    if randint(0,1):
        opinions, facts = facts, opinions
        left, right = right, left
    
    ## Check whether Pupil Core is connected
    if capture_exists:
        ## Measure local time
        local_time = local_clock()
        ## Create label
        label = product + '_' + left + '_start'
        ## Crealte an annotation
        minimal_trigger = ra.new_trigger(label, local_time + stable_offset_mean)
        ## Send the annotation to Pupil Core with the
        ## start trigger
        ra.send_trigger(pub_socket, minimal_trigger)
    
    ## Write out what was displayed on the left side
    trials.addData('left', left)
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
    ## Check whether Pupil Core is connected
    ## And send the annotation with the stop trigger.
    if capture_exists:
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
    textbox.reset()
    # Run 'Begin Routine' code from code_2
    ## Make the mouse cursor visible
    win.mouseVisible = True
    
    ## Timestamp of when the star appeared
    stars_appeared = local_clock()
    # keep track of which components have finished
    ratingsComponents = [textbox, stars, stars_2_1, stars_2_2, stars_3_1, stars_3_2, stars_3_3, stars_4_1, stars_4_2, stars_4_3, stars_4_4, stars_5_1, stars_5_2, stars_5_3, stars_5_4, stars_5_5, star_1, star_2, star_3, star_4, star_5]
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
        
        # *stars* updates
        if stars.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars.frameNStart = frameN  # exact frame index
            stars.tStart = t  # local t and not account for scr refresh
            stars.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars.started')
            stars.setAutoDraw(True)
        
        # *stars_2_1* updates
        if stars_2_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars_2_1.frameNStart = frameN  # exact frame index
            stars_2_1.tStart = t  # local t and not account for scr refresh
            stars_2_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars_2_1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars_2_1.started')
            stars_2_1.setAutoDraw(True)
        
        # *stars_2_2* updates
        if stars_2_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars_2_2.frameNStart = frameN  # exact frame index
            stars_2_2.tStart = t  # local t and not account for scr refresh
            stars_2_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars_2_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars_2_2.started')
            stars_2_2.setAutoDraw(True)
        
        # *stars_3_1* updates
        if stars_3_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars_3_1.frameNStart = frameN  # exact frame index
            stars_3_1.tStart = t  # local t and not account for scr refresh
            stars_3_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars_3_1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars_3_1.started')
            stars_3_1.setAutoDraw(True)
        
        # *stars_3_2* updates
        if stars_3_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars_3_2.frameNStart = frameN  # exact frame index
            stars_3_2.tStart = t  # local t and not account for scr refresh
            stars_3_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars_3_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars_3_2.started')
            stars_3_2.setAutoDraw(True)
        
        # *stars_3_3* updates
        if stars_3_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars_3_3.frameNStart = frameN  # exact frame index
            stars_3_3.tStart = t  # local t and not account for scr refresh
            stars_3_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars_3_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars_3_3.started')
            stars_3_3.setAutoDraw(True)
        
        # *stars_4_1* updates
        if stars_4_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars_4_1.frameNStart = frameN  # exact frame index
            stars_4_1.tStart = t  # local t and not account for scr refresh
            stars_4_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars_4_1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars_4_1.started')
            stars_4_1.setAutoDraw(True)
        
        # *stars_4_2* updates
        if stars_4_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars_4_2.frameNStart = frameN  # exact frame index
            stars_4_2.tStart = t  # local t and not account for scr refresh
            stars_4_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars_4_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars_4_2.started')
            stars_4_2.setAutoDraw(True)
        
        # *stars_4_3* updates
        if stars_4_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars_4_3.frameNStart = frameN  # exact frame index
            stars_4_3.tStart = t  # local t and not account for scr refresh
            stars_4_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars_4_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars_4_3.started')
            stars_4_3.setAutoDraw(True)
        
        # *stars_4_4* updates
        if stars_4_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars_4_4.frameNStart = frameN  # exact frame index
            stars_4_4.tStart = t  # local t and not account for scr refresh
            stars_4_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars_4_4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars_4_4.started')
            stars_4_4.setAutoDraw(True)
        
        # *stars_5_1* updates
        if stars_5_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars_5_1.frameNStart = frameN  # exact frame index
            stars_5_1.tStart = t  # local t and not account for scr refresh
            stars_5_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars_5_1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars_5_1.started')
            stars_5_1.setAutoDraw(True)
        
        # *stars_5_2* updates
        if stars_5_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars_5_2.frameNStart = frameN  # exact frame index
            stars_5_2.tStart = t  # local t and not account for scr refresh
            stars_5_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars_5_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars_5_2.started')
            stars_5_2.setAutoDraw(True)
        
        # *stars_5_3* updates
        if stars_5_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars_5_3.frameNStart = frameN  # exact frame index
            stars_5_3.tStart = t  # local t and not account for scr refresh
            stars_5_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars_5_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars_5_3.started')
            stars_5_3.setAutoDraw(True)
        
        # *stars_5_4* updates
        if stars_5_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars_5_4.frameNStart = frameN  # exact frame index
            stars_5_4.tStart = t  # local t and not account for scr refresh
            stars_5_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars_5_4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars_5_4.started')
            stars_5_4.setAutoDraw(True)
        
        # *stars_5_5* updates
        if stars_5_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stars_5_5.frameNStart = frameN  # exact frame index
            stars_5_5.tStart = t  # local t and not account for scr refresh
            stars_5_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stars_5_5, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stars_5_5.started')
            stars_5_5.setAutoDraw(True)
        
        # *star_1* updates
        if star_1.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            star_1.frameNStart = frameN  # exact frame index
            star_1.tStart = t  # local t and not account for scr refresh
            star_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(star_1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'star_1.started')
            star_1.setAutoDraw(True)
        if star_1.status == STARTED:
            # check whether star_1 has been pressed
            if star_1.isClicked:
                if not star_1.wasClicked:
                    star_1.timesOn.append(routineTimer.getTime()) # store time of first click
                    star_1.timesOff.append(routineTimer.getTime()) # store time clicked until
                else:
                    star_1.timesOff[-1] = routineTimer.getTime() # update time clicked until
                if not star_1.wasClicked:
                    continueRoutine = False  # end routine when star_1 is clicked
                    None
                star_1.wasClicked = True  # if star_1 is still clicked next frame, it is not a new click
            else:
                star_1.wasClicked = False  # if star_1 is clicked next frame, it is a new click
        else:
            star_1.wasClicked = False  # if star_1 is clicked next frame, it is a new click
        
        # *star_2* updates
        if star_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            star_2.frameNStart = frameN  # exact frame index
            star_2.tStart = t  # local t and not account for scr refresh
            star_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(star_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'star_2.started')
            star_2.setAutoDraw(True)
        if star_2.status == STARTED:
            # check whether star_2 has been pressed
            if star_2.isClicked:
                if not star_2.wasClicked:
                    star_2.timesOn.append(star_2.buttonClock.getTime()) # store time of first click
                    star_2.timesOff.append(star_2.buttonClock.getTime()) # store time clicked until
                else:
                    star_2.timesOff[-1] = star_2.buttonClock.getTime() # update time clicked until
                if not star_2.wasClicked:
                    continueRoutine = False  # end routine when star_2 is clicked
                    None
                star_2.wasClicked = True  # if star_2 is still clicked next frame, it is not a new click
            else:
                star_2.wasClicked = False  # if star_2 is clicked next frame, it is a new click
        else:
            star_2.wasClicked = False  # if star_2 is clicked next frame, it is a new click
        
        # *star_3* updates
        if star_3.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            star_3.frameNStart = frameN  # exact frame index
            star_3.tStart = t  # local t and not account for scr refresh
            star_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(star_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'star_3.started')
            star_3.setAutoDraw(True)
        if star_3.status == STARTED:
            # check whether star_3 has been pressed
            if star_3.isClicked:
                if not star_3.wasClicked:
                    star_3.timesOn.append(star_3.buttonClock.getTime()) # store time of first click
                    star_3.timesOff.append(star_3.buttonClock.getTime()) # store time clicked until
                else:
                    star_3.timesOff[-1] = star_3.buttonClock.getTime() # update time clicked until
                if not star_3.wasClicked:
                    continueRoutine = False  # end routine when star_3 is clicked
                    None
                star_3.wasClicked = True  # if star_3 is still clicked next frame, it is not a new click
            else:
                star_3.wasClicked = False  # if star_3 is clicked next frame, it is a new click
        else:
            star_3.wasClicked = False  # if star_3 is clicked next frame, it is a new click
        
        # *star_4* updates
        if star_4.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            star_4.frameNStart = frameN  # exact frame index
            star_4.tStart = t  # local t and not account for scr refresh
            star_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(star_4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'star_4.started')
            star_4.setAutoDraw(True)
        if star_4.status == STARTED:
            # check whether star_4 has been pressed
            if star_4.isClicked:
                if not star_4.wasClicked:
                    star_4.timesOn.append(star_4.buttonClock.getTime()) # store time of first click
                    star_4.timesOff.append(star_4.buttonClock.getTime()) # store time clicked until
                else:
                    star_4.timesOff[-1] = star_4.buttonClock.getTime() # update time clicked until
                if not star_4.wasClicked:
                    continueRoutine = False  # end routine when star_4 is clicked
                    None
                star_4.wasClicked = True  # if star_4 is still clicked next frame, it is not a new click
            else:
                star_4.wasClicked = False  # if star_4 is clicked next frame, it is a new click
        else:
            star_4.wasClicked = False  # if star_4 is clicked next frame, it is a new click
        
        # *star_5* updates
        if star_5.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            star_5.frameNStart = frameN  # exact frame index
            star_5.tStart = t  # local t and not account for scr refresh
            star_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(star_5, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'star_5.started')
            star_5.setAutoDraw(True)
        if star_5.status == STARTED:
            # check whether star_5 has been pressed
            if star_5.isClicked:
                if not star_5.wasClicked:
                    star_5.timesOn.append(star_5.buttonClock.getTime()) # store time of first click
                    star_5.timesOff.append(star_5.buttonClock.getTime()) # store time clicked until
                else:
                    star_5.timesOff[-1] = star_5.buttonClock.getTime() # update time clicked until
                if not star_5.wasClicked:
                    continueRoutine = False  # end routine when star_5 is clicked
                    None
                star_5.wasClicked = True  # if star_5 is still clicked next frame, it is not a new click
            else:
                star_5.wasClicked = False  # if star_5 is clicked next frame, it is a new click
        else:
            star_5.wasClicked = False  # if star_5 is clicked next frame, it is a new click
        
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
    trials.addData('star_1.numClicks', star_1.numClicks)
    if star_1.numClicks:
       trials.addData('star_1.timesOn', star_1.timesOn)
       trials.addData('star_1.timesOff', star_1.timesOff)
    else:
       trials.addData('star_1.timesOn', "")
       trials.addData('star_1.timesOff', "")
    trials.addData('star_2.numClicks', star_2.numClicks)
    if star_2.numClicks:
       trials.addData('star_2.timesOn', star_2.timesOn)
       trials.addData('star_2.timesOff', star_2.timesOff)
    else:
       trials.addData('star_2.timesOn', "")
       trials.addData('star_2.timesOff', "")
    trials.addData('star_3.numClicks', star_3.numClicks)
    if star_3.numClicks:
       trials.addData('star_3.timesOn', star_3.timesOn)
       trials.addData('star_3.timesOff', star_3.timesOff)
    else:
       trials.addData('star_3.timesOn', "")
       trials.addData('star_3.timesOff', "")
    trials.addData('star_4.numClicks', star_4.numClicks)
    if star_4.numClicks:
       trials.addData('star_4.timesOn', star_4.timesOn)
       trials.addData('star_4.timesOff', star_4.timesOff)
    else:
       trials.addData('star_4.timesOn', "")
       trials.addData('star_4.timesOff', "")
    trials.addData('star_5.numClicks', star_5.numClicks)
    if star_5.numClicks:
       trials.addData('star_5.timesOn', star_5.timesOn)
       trials.addData('star_5.timesOff', star_5.timesOff)
    else:
       trials.addData('star_5.timesOn', "")
       trials.addData('star_5.timesOff', "")
    # Run 'End Routine' code from code_2
    ## Make the mouse coursor invisible
    win.mouseVisible = False
    
    ## Reaction time to a star
    stars_time = local_clock() - stars_appeared
    
    ## Assign the reaction time to a star
    ## to the relevant star
    if star_1.numClicks and star_1.numClicks > star_1_num_clicks:
        star_1_rt = stars_time
        star_1_num_clicks = star_1.numClicks
    else:
        star_1_rt = 0
    
    if star_2.numClicks and star_2.numClicks > star_2_num_clicks:
        star_2_rt = stars_time
        star_2_num_clicks = star_2.numClicks
    else:
        star_2_rt = 0
    
    if star_3.numClicks and star_3.numClicks > star_3_num_clicks:
        star_3_rt = stars_time
        star_3_num_clicks = star_3.numClicks
    else:
        star_3_rt = 0
        
    if star_4.numClicks and star_4.numClicks > star_4_num_clicks:
        star_4_rt = stars_time
        star_4_num_clicks = star_4.numClicks
    else:
        star_4_rt = 0
        
    if star_5.numClicks and star_5.numClicks > star_5_num_clicks:
        star_5_rt = stars_time
        star_5_num_clicks = star_5.numClicks
    else:
        star_5_rt = 0
    
    ## Write out the reactions times to XLSX file
    trials.addData('star1', star_1_rt)
    trials.addData('star2', star_2_rt)
    trials.addData('star3', star_3_rt)
    trials.addData('star4', star_4_rt)
    trials.addData('star5', star_5_rt)
    
    ## Write out condition order the automatic
    ## variable does not work properly because
    ## of the times of Buttons being weird
    trials.addData('condition_order', condition_order)
    
    ## Increament condition order
    condition_order += 1
    # the Routine "ratings" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'trials'

# get names of stimulus parameters
if trials.trialList in ([], [None], None):
    params = []
else:
    params = trials.trialList[0].keys()
# save data for this loop
trials.saveAsExcel(filename + '.xlsx', sheetName='trials',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

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
## Check whether Pupil Capture is connected
if capture_exists:
    ## stop recording
    pupil_remote.send_string("r")
    pupil_remote.recv_string()


# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsPickle(filename)
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()

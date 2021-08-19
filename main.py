from mplayer import Player, CmdPrefix
import PySimpleGUI as sg

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Set default prefix for all Player instances
Player.cmd_prefix = CmdPrefix.PAUSING_KEEP

# Since autospawn is True by default, no need to call player.spawn() manually
player = Player()
player2 = Player()


def load_file(path_to_video):
    # Play a file
    player.loadfile(path_to_video)
    # Pause playback
    player.pause()
    # Play a file
    player2.loadfile(path_to_video)
    player2.pause()

    align_files()

    player.switch_audio = int(values['-Player1AT-'])
    player2.switch_audio = int(values['-Player2AT-'])
    player.sub_visibility = True
    player.sub = int(values['-Player1Sub-'])


def play_file():

    player.pause()
    player2.pause()


def align_files():

    time_pos = max(0, player.time_pos - 3)
    player2.time_pos = time_pos
    player.time_pos = time_pos


sg.theme('Dark Green 5')
layout = [
    [sg.Text('Path to video:', size=(15, 1), auto_size_text=False, justification='left'),
     sg.InputText('/home/amator/Download/Replacements.mkv', key='-PATH-', size=(64, 1)),
     sg.FileBrowse(file_types=(("Video files", "*.mkv"),))],
    [sg.Button('Open', key=f'btnOpen', size=(22, 1)), sg.Button('Play/Pause', key=f'btnPlay', size=(22, 1)),
     sg.Button('Align', key=f'btnAlign', size=(22, 1))],
    [sg.Text('Player 1 Audio track:', size=(35, 1), auto_size_text=False, justification='left'),
     sg.Slider(range=(0, 6), orientation='h', size=(34, 20), default_value=2, key='-Player1AT-')],
    [sg.Text('Player 2 Audio track:', size=(35, 1), auto_size_text=False, justification='left'),
     sg.Slider(range=(0, 6), orientation='h', size=(34, 20), default_value=0, key='-Player2AT-')],
    [sg.Text('Player 1 Subtitle:', size=(35, 1), auto_size_text=False, justification='left'),
     sg.Slider(range=(0, 4), orientation='h', size=(34, 20), default_value=2, key='-Player1Sub-')],
]
win = sg.Window('2Channel player', layout, finalize=True)

# ---------
# MAIN LOOP
# ---------

while True:
    event, values = win.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'btnOpen':
        load_file(values['-PATH-'])
    elif event == 'btnPlay':
        try:
            play_file()
        except Exception as err:
            logger.info(err)
    elif event == 'btnAlign':
        align_files()
    else:
        logger.info(f'This event ({event}) is not yet handled.')

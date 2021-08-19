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

    # metadata = player.metadata or {}
    # print(metadata.get('track', ''))

    player.switch_audio = 2
    player.sub_visibility = True
    player.sub = 2
    # player.sub_source = 2


def play_file():

    # p = player.paused
    # logger.info(p)
    #
    # if  player.paused == Flag:
    player.pause()

    # if player2.paused == Flag:
    player2.pause()

def align_files():

    # if not player.paused:
    #     player.pause()
    #
    # if not player2.paused:
    #     player2.pause()

    # logger.info(player.time_pos)
    # logger.info(player2.time_pos)
    # logger.info(player2.time_pos-player.time_pos)

    time_pos = player.time_pos

    player2.time_pos = time_pos
    player.time_pos = time_pos

    # logger.info('***********************')
    #
    # logger.info(player.time_pos)
    # logger.info(player2.time_pos)
    # logger.info(player2.time_pos - player.time_pos)
    # player.pause()
    # player2.pause()

    # player.time_pos = 40
    # player2.time_pos = 51

    # print(player.length)
    # Get title from metadata
    # metadata = player.metadata or {}
    # print(metadata.get('Title', ''))

    # Print the filename
    # logger.info(player.filename)

    # Seek +5 seconds
    # player.time_pos += 5
    #
    # # Set to fullscreen
    # player.fullscreen = True
    #
    # # Terminate MPlayer
    # player.quit()


layout = [

    [sg.Text('Path to video:', size=(35, 1), auto_size_text=False, justification='left'),
     sg.InputText('/home/amator/Download/Replacements.mkv', key='-PATH-', size=(64, 1)), sg.FileBrowse(file_types=(("Video files", "*.mkv"),))],

    [sg.Button('Open', key=f'btnOpen', size=(22, 1))],
    [sg.Button('Play/Pause', key=f'btnPlay', size=(22, 1))],  # sg.Button('Pause', key=f'btnPause', size=(22, 1))],
    [sg.Button('Align', key=f'btnAlign', size=(22, 1))],

    # [sg.Output(size=(112, 12), key='-OUTPUT-')],
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
    # elif event == 'btnPause':
    #         play_file(False)
    elif event == 'btnAlign':
        align_files()
    else:
        logger.info(f'This event ({event}) is not yet handled.')
# from mplayer import Player, CmdPrefix
import pprint
from time import sleep

import mpv
import PySimpleGUI as sg

import time
from PIL import Image, ImageDraw, ImageFont

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Set default prefix for all Player instances
# Player.cmd_prefix = CmdPrefix.PAUSING_KEEP

# Since autospawn is True by default, no need to call player.spawn() manually
player = mpv.MPV(ytdl=True, input_default_bindings=False, input_vo_keyboard=True)
player2 = mpv.MPV(ytdl=True, input_default_bindings=False, input_vo_keyboard=True, osc=True)

# Option access, in general these require the core to reinitialize
player['vo'] = 'gpu'
player2['vo'] = 'gpu'


# Property access, these can be changed at runtime
# @player.property_observer('time-pos')
# def time_observer(_name, value):
#     # Here, _value is either None if nothing is playing or a float containing
#     # fractional seconds since the beginning of the file.
#     if value:
#         print('Now playing 1 at {:.2f}s'.format(value))
#
#
# @player2.property_observer('time-pos')
# def time_observer(_name, value):
#     # Here, _value is either None if nothing is playing or a float containing
#     # fractional seconds since the beginning of the file.
#     if value:
#         print('Now playing 2 at {:.2f}s'.format(value))


def generate_audio_track_list():
    audio_track_list = "Audio tracks:\n"
    track_list = getattr(player, 'track-list')
    for i, track in enumerate(track_list):
        if track.get('type', '') == 'audio':
            audio_track_list += f"{track.get('id', '')} {track.get('title', 'Track '+str(track.get('id', '')))} - [{track.get('lang', '')}]\n"
    audio_track_list += "\nSubtitles:\n"
    for i, track in enumerate(track_list):
        if track.get('type', '') == 'sub':
            audio_track_list += f"{track.get('id', '')} {track.get('title', 'Track ' + str(track.get('id', '')))} - [{track.get('lang', '')}]\n"
    audio_track_list += """\nControl:
    F - fullscreen
    P - play/pause
    A - align
    D - forward 10s
    S - backward 10s  
    H - forward 5m
    G - backward 5m
    """
    win['-AUDIOTRACK-'].update(audio_track_list)


def load_file(path_to_video):
    # Play a file
    player._set_property("audio-device", 'pulse/alsa_output.usb-0d8c_USB_Sound_Device-00.analog-stereo')
    player2._set_property("audio-device", 'pulse/alsa_output.pci-0000_01_00.1.hdmi-stereo')

    player.loadfile(path_to_video)
    # player.wait_for_playback()

    # pprint.pprint(player._get_property("audio-device-list"))
    player2.loadfile(path_to_video)
    player._set_property("pause", True)
    player2._set_property("pause", True)
    getattr(player, 'track-list')
    sleep(0.5)
    generate_audio_track_list()


    # pprint.pprint(getattr(player, 'track-list'))
    # align_files()
    # player2.wait_for_playback()
    # Pause playback
    # player.fullscreen = True


    # # Play a file
    # player2.loadfile(path_to_video)
    # player2.pause()
    #
    # align_files()
    #
    # player.switch_audio = int(values['-Player1AT-'])
    # player2.switch_audio = int(values['-Player2AT-'])


    # player.sub = True
    # player.sub = int(values['-Player1Sub-'])

@player.on_key_press('q')
@player2.on_key_press('q')
def my_q_binding():
    # play_file()
    print('THERE IS NO ESCAPE')


@player.on_key_press('p')
@player2.on_key_press('p')
def my_p_binding():
    play_file()


@player.on_key_press('a')
@player2.on_key_press('a')
def my_a_binding():
    align_files(2)


@player.on_key_press('d')
@player2.on_key_press('d')
def my_d_binding():
    align_files(-10)
    # font = ImageFont.truetype('DejaVuSans.ttf', 40)
    # time.sleep(0.5)
    # overlay = player.create_image_overlay()
    #
    # # for pos in range(0, 500, 5):
    # pos = 0
    # ts = player.time_pos
    # if ts is None:
    #     return
    #
    # img = Image.new('RGBA', (400, 150),  (255, 255, 255, 0))
    # d = ImageDraw.Draw(img)
    # # d.text((10, 10), 'Hello World', font=font, fill=(0, 255, 255, 128))
    # d.text((10, 60), f'{ts:.0f}', font=font, fill=(255, 255, 255, 255))
    #
    # overlay.update(img, pos=(2*pos, pos))
    # time.sleep(1)
    #
    # overlay.remove()

@player.on_key_press('s')
@player2.on_key_press('s')
def my_s_binding():
    align_files(10)


@player.on_key_press('h')
@player2.on_key_press('h')
def my_h_binding():
    align_files(-300)


@player.on_key_press('g')
@player2.on_key_press('g')
def my_g_binding():
    align_files(300)




@player2.on_key_press('f')
def my_f_binding():
    player2.fullscreen = not player2.fullscreen

# @player2.on_key_press('q')
# def my_q_binding():
#     print('THERE IS NO ESCAPE 2')


def play_file():

    player.audio = int(values['-Player1AT-'])
    player2.audio = int(values['-Player2AT-'])

    play = player._get_property("pause")

    player._set_property("pause", not play)
    player2._set_property("pause", not play)
    # player.pause()
    # player2.pause()


def align_files(sec):
    if not player.time_pos:
        return
    time_pos = max(0, player.time_pos - sec)
    player2.time_pos = time_pos
    player.time_pos = time_pos


sg.theme('Dark Green 5')
layout = [
    [sg.Text('Path to video:', size=(15, 1), auto_size_text=False, justification='left'),
     # sg.InputText('/run/media/amator/Data/Moya.Prekrasnaya.Ledi.1964.DUAL.BDRip.XviD.AC3.-AllFillms/Moya.Prekrasnaya.Ledi.1964.DUAL.BDRip.XviD.AC3.-AllFillms.avi', key='-PATH-', size=(64, 1)),
     sg.InputText('/home/amator/Bad.Santa.2.2016.Unrated.BDRip-AVC.OIV.mkv', key='-PATH-', size=(64, 1)),
     # sg.InputText('/run/media/amator/Data/Властелин Колец - Гоблин - Божья Искра/Братва и кольцо Гоблин 1080p.mp4', key='-PATH-', size=(64, 1)),

     sg.FileBrowse(file_types=(("Video files", "*.mkv"),))],

    [sg.Button('Open', key=f'btnOpen', size=(22, 1)), sg.Button('Play/Pause', key=f'btnPlay', size=(22, 1)),
     sg.Button('Align', key=f'btnAlign', size=(22, 1))],
    [sg.Text(size=(64, 25), key='-AUDIOTRACK-')],
    [sg.Text('Player 1 Audio track:', size=(35, 1), auto_size_text=False, justification='left'),
     sg.Slider(range=(1, 6), orientation='h', size=(34, 20), default_value=1, key='-Player1AT-')],
    [sg.Text('Player 2 Audio track:', size=(35, 1), auto_size_text=False, justification='left'),
     sg.Slider(range=(1, 6), orientation='h', size=(34, 20), default_value=2, key='-Player2AT-')],
    [sg.Text('Player 1 Subtitle:', size=(35, 1), auto_size_text=False, justification='left'),
     sg.Slider(range=(1, 6), orientation='h', size=(34, 20), default_value=1, key='-Player1Sub-')],
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
        align_files(2)
    else:
        logger.info(f'This event ({event}) is not yet handled.')

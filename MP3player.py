import PySimpleGUI as sg
import os
from tinytag import TinyTag
import pygame
import datetime

tabvalues = [[00, 00], [00, 00]]
listofpaths=[]

def get_list_of_files(directory):
    Music_files = []
    for roots, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.mp3'):
                Music_files.append(os.path.join(roots, f))
    return Music_files


v_pause = True


def get_min_sec_from_duration(duration):
    minu = duration // 60
    sec = (((duration / 60) - (duration // 60)) * 60) // 1
    seconds = ''
    if sec < 10:
        seconds = str(0) + str(int(sec))
    else:
        seconds = str(0) + str(int(sec))

    return str(int(minu)) + ':' + seconds


def play_music_track(trackpath):
    pass    # Setup the end track event



def make_song_table(Music_Attributes):
    num_rows = len(Music_Attributes) + 1
    num_cols = len(Music_Attributes[1].keys())
    data = [[j for j in range(num_cols)] for i in range(num_rows)]
    data[0] = ['S no', 'Album', 'Title', 'Duration', 'Artist', 'Year']
    for key, value in Music_Attributes.items():
        data[key + 1] = [key, value["Album"], value["Title"], value["Duration"], value["Artist"], value["Year"]]

    return song_table_data


def get_music_attributes(list_of_music_files):
    Music_Attributes = dict()
    for index, val in enumerate(list_of_music_files):
        tag = TinyTag.get(val)
        Music_Attributes.update(
            {index: {'Artist': tag.artist, 'Duration': datetime.timedelta(seconds=round(tag.duration)), "Path": val,
                     "Album": tag.album, "Title": tag.title, "Year": tag.year}})
    return Music_Attributes


data = [['', '', '', '', '', '']]
headings = ['S no', 'Album', 'Title', 'Duration', 'Artist', 'Year']

Layout = [[sg.Text("Welcome to Praveen's Juke BOX have fun!!!!!!!")],
          [sg.Text("This is a place holder for animation")],
          [sg.Text("This is a place holder for seek")],
          [sg.Text("Browse the song library"), sg.InputText(key='_foldernm_'), sg.FolderBrowse(key='_foldername_'),
           sg.Button('Load')],
          [sg.Table(values=data[:][:], headings=headings, max_col_width=120, def_col_width=20,
                    display_row_numbers=True, justification='center', num_rows=20, alternating_row_color='lightblue',
                    key='_table_')],
          [sg.Button('Play', key='_playbut_'), sg.Button('Pause', key='_pause_'), sg.Button('Stop', key='_stop_'),
           sg.Button('Vol(+)', key='_vplus_'), sg.Button('Vol(-)', key='_vminus_')],
          ]

window = sg.Window("Praveen's JUKE box", Layout)

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    if event == "Load":
        list_of_files = get_list_of_files(values['_foldernm_']);

        att = get_music_attributes(list_of_files)

        data1 = []
        for key, value in att.items():
            data1.append([key, value["Album"], value["Title"], value["Duration"], value["Artist"], value["Year"]])
        window.FindElement('_table_').Update(values=data1)
    if event == '_playbut_':
        indexarr = values['_table_']
        legthofsong=len(indexarr)
        if(legthofsong==0):
            print('please make a selection')
            sg.Popup('Hello ,', 'please make a selection before click the play button')
        else:
            indexsong = indexarr[0]
            pygame.mixer.init()
            pygame.mixer.music.load((att[indexsong])["Path"])
            pygame.mixer.music.play()
            while ((indexsong+1)<len(att)):
                if pygame.mixer.music.get_busy():
                    pygame.time.wait(500)  # ms
                else:
                    indexsong=indexsong+1
                    pygame.mixer.music.load((att[indexsong])["Path"])
                    pygame.mixer.music.play()
        #pygame.mixer.music.queue(listofpaths)
    if event == '_pause_':
        if v_pause:
            pygame.mixer.music.pause()
            v_pause = False
        else:
            pygame.mixer.music.unpause()
            v_pause = True
    if event == '_stop_':
        pygame.mixer.music.stop()
    if event == '_vplus_':
        curvol = pygame.mixer.music.get_volume()
        if (curvol + 0.10) <= 1:
            pygame.mixer.music.set_volume(curvol + 0.10)
    if event == '_vminus_':
        curvol = pygame.mixer.music.get_volume()
        if (curvol - 0.10) <= 0:
            pygame.mixer.music.set_volume(curvol - 0.10)

    print(event, values)
window.Close()

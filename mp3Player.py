from tkinter import *
import tkinter.font as font
from tkinter import filedialog as fd
import os
import time
from pygame import mixer
from mutagen.mp3 import MP3
import pygame
import threading

index = 0
listMusic = []
curren_MUSIC_len = ''
mixer.init()
isStoped = False
wind = Tk()
wind.geometry('353x260')
wind.title('Mp3Player')
wind.configure(bg='black')
frameCenter = Frame(wind)

frameCenter.pack(side = BOTTOM)
frameTop = Frame(wind)

frameTop.pack(side = TOP)

# List Box
lsBox = Listbox(frameTop,bg='black',fg='white',selectbackground='green',width=60)
lsBox.pack()

# label for show time
time_info_lbl = Label(frameTop,text='00:00')
time_info_lbl.pack()

# label for show current song name
current_music_lbl = Label(frameTop,text='Current Song...',)
current_music_lbl.pack()

# function to play song
def musicPlayer(fl_path):
    mixer.music.load(fl_path)
    mixer.music.play(3)
# function to change current music name from label    
def curr_song_lbl_changer(fl_path):
    current_music_lbl.config(text=os.path.basename(fl_path))

# file opener    
def openFile():
    global index
    global listMusic
    fls = fd.askopenfilenames(filetypes=(('mp3 files','*.mp3'),))
    # check if new files in list musics
    for song in fls:
        # check if file not exist in arr then append list
        if song not in listMusic:
            listMusic.append(song)
            shortName = os.path.basename(song)
            lsBox.insert(index,shortName)
            index+=1
    

# time runner
def timeStart():
    global curren_MUSIC_len

    
    mp3 = MP3(curren_MUSIC_len)
    info_mp3 = mp3.info
    # converting
    len_mp3 = int(info_mp3.length)
    hour = len_mp3 // 3600
    len_mp3 %= 3600

    mins = len_mp3 // 60
    len_mp3 %=60

    current_len = mixer.music.get_pos()/1000
    convert_to_time = time.strftime('%H:%M:%S',time.gmtime(current_len))

    total_len = str(hour) + ':' + str(mins) + ':' + str(len_mp3)
    # change label 
    time_info_lbl.config(text=str(convert_to_time) +'/' + str(total_len))
    time_info_lbl.after(1000,timeStart)

curent_song_ind = 0

# player Song
def playSong():
    global listMusic
    global curren_MUSIC_len
    global curent_song_ind
    currentSong = lsBox.curselection()
    try:
        currSongInd = int(currentSong[0])
        curent_song_ind = int(currentSong[0])
        full_path = listMusic[currSongInd]
        curren_MUSIC_len = full_path
        # here using function 
        curr_song_lbl_changer(full_path)
        timeStart()
        # here using function
        musicPlayer(full_path)
        
    except IndexError:
        pass 
    

# thread for waiting until playing song     
def thread():
    musThread = threading.Thread(target = playSong)
    musThread.start()
    
# pause/Unpause function
def pauseMusic():
    global isStoped
    if isStoped != True:
        mixer.music.pause()
        isStoped = True
    else:
        mixer.music.unpause()
        isStoped = False


prev = False

def nextSong():
    global curent_song_ind
    curent_song_ind+=1
    try:
        # here using function 
        musicPlayer(listMusic[curent_song_ind])
        # here using function
        curr_song_lbl_changer(listMusic[curent_song_ind])
    except Exception:
        pass    

def prevSong():
    global curent_song_ind
    curent_song_ind-=1
    try:
        # here using function
        musicPlayer(listMusic[curent_song_ind])
        # here using function
        curr_song_lbl_changer(listMusic[curent_song_ind])
    except Exception:
        pass       
    



btnAdder = Button(frameTop,text='+',command=openFile,fg='white',bg='gray',width=3)
btnAdder['font'] = font.Font(weight='bold')
btnAdder.pack(side=LEFT)


btnStart = Button(frameCenter,text='Start',command=thread,width=9,height=1,bg='#1e99ff',font='bold')
btnStart.grid(row=0,column=1)

btnPause = Button(frameCenter,text='un/Pause',command=pauseMusic,width=10,height=1,bg='#1e99ff',font='bold')
btnPause.grid(row=0,column=2)

btnNext = Button(frameCenter,text='Next',command=nextSong,width=9,height=1,bg='#1e99ff',font='bold')
btnNext.grid(row=0,column=3)
btnPrev = Button(frameCenter,text='Prev',command=prevSong,width=9,height=1,bg='#1e99ff',font='bold')
btnPrev.grid(row=0,column=4)

wind.mainloop()

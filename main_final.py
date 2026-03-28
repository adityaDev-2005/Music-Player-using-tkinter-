import tkinter
import customtkinter
import pygame
from PIL import Image, ImageTk
from threading import Thread
import time
import os

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.title("Music Player")
root.geometry("400x450")

pygame.mixer.init()

image_list = [
'img/am_i_dreaming.png','img/calling.png','img/hope.png',
'img/self_love.png','img/silk_cologne.png','img/sunflower.png',
'img/take_it_to_the_top.png'
]

songs_list = [
'music/Metro-Boomin-Am-I-Dreaming-ft-A-AP-Rocky-Roisee-(HipHopKit.com).mp3',
'music/Metro-Boomin-Calling-Spider-Man-Across-the-Spider-Verse-ft-Swae-Lee-NAV-A-Boogie-wit-da-Hoodie-(HipHopKit.com).mp3',
'music/NF-HOPE-song-(HipHopKit.com).mp3',
'music/Metro-Boomin-Self-Love-Spider-Man-Across-the-Spider-Verse-ft-Coi-Leray-(HipHopKit.com).mp3',
'music/EI8HT-Silk-and-Cologne-Spider-Verse-Remix-ft-Offset-(HipHopKit.com).mp3',
'music/Post-Malone-Sunflower-Spider-Man-Into-the-Spider-Verse-Ft-Swae-Lee-(HipHopKit.com).mp3',
'music/Becky-G-Take-It-To-The-Top-Ft-Ayra-Starr-(HipHopKit.com).mp3'
]

n = 0
paused = False
dragging = False
song_start_time = 0
song_length = 0
seek_offset = 0
progress_thread_running = False

label1 = tkinter.Label(root)
label1.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

song_name_label = tkinter.Label(
root,bg='#222222',fg='white',
wraplength=300,justify="center",font=("Arial",10))
song_name_label.place(relx=0.5,rely=0.6,anchor=tkinter.CENTER)

# for pause and play images on the GUI
play_img = customtkinter.CTkImage(Image.open("img/play.png"), size=(30,30))
pause_img = customtkinter.CTkImage(Image.open("img/pause.png"), size=(30,30))

# prev. and next song
prev_img = customtkinter.CTkImage(Image.open("img/prev.png"), size=(30,30))
next_img = customtkinter.CTkImage(Image.open("img/next.png"), size=(30,30))

def get_album_cover(song_name,n):

    img = Image.open(image_list[n])
    img = img.resize((250,250))
    photo = ImageTk.PhotoImage(img)

    label1.configure(image=photo)
    label1.image = photo

    name = os.path.basename(song_name)[:-20]
    song_name_label.configure(text=name)


def progress():

    global song_start_time , progress_thread_running
    
    progress_thread_running = True

    while pygame.mixer.music.get_busy():

        if paused or dragging:
            time.sleep(0.3)
            continue

        # if dragging:
        #     time.sleep(0.3)
        #     continue

        elapsed = time.time() - song_start_time + seek_offset
        progress_slider.set(elapsed / song_length)

        time.sleep(0.5)

    progress_thread_running = False
    if not paused:
        skip_next()


def start_thread():
    global progress_thread_running
    if progress_thread_running:
        return
    t = Thread(target=progress)
    t.daemon = True
    t.start()


def play_music():

    global n, paused, song_start_time, song_length, seek_offset

    paused = False
    pause_button.configure(image=pause_img)

    progress_slider.set(0)
    seek_offset = 0

    if n >= len(songs_list):
        n = 0

    song = songs_list[n]

    sound = pygame.mixer.Sound(song)
    song_length = sound.get_length()

    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

    song_start_time = time.time()

    pygame.mixer.music.set_volume(0.5)

    get_album_cover(song,n)

    # for pause button to reset
    pause_button.configure(image=pause_img)

    start_thread()

    #n += 1


def pause_resume():

    global paused, song_start_time

    if paused:

        pygame.mixer.music.unpause()
        song_start_time = time.time()
        pause_button.configure(image=pause_img)
        paused = False

    else:

        pygame.mixer.music.pause()
        pause_button.configure(image=play_img)
        paused = True


def skip_next():
    global n
    n+=1
    play_music()


def skip_previous():

    global n

    n -= 2
    if n < 0:
        n = len(songs_list)-1

    play_music()


def volume(v):
    pygame.mixer.music.set_volume(v)


def start_drag(event):
    global dragging
    dragging = True


def stop_drag(event):

    global dragging, seek_offset, song_start_time

    dragging = False

    value = progress_slider.get()

    seek_offset = value * song_length

    pygame.mixer.music.stop()
    pygame.mixer.music.play(start=seek_offset)

    song_start_time = time.time()


# Buttons
play_button = customtkinter.CTkButton(root,image=play_img,command=play_music,text="")
play_button.place(relx=0.5,rely=0.7,anchor=tkinter.CENTER)

pause_button = customtkinter.CTkButton(root,image=pause_img,command=pause_resume,width=60,text="")
pause_button.place(relx=0.5,rely=0.8,anchor=tkinter.CENTER)

prev_button = customtkinter.CTkButton(root,text="",command=skip_previous,width=40,image=prev_img)
prev_button.place(relx=0.25,rely=0.7,anchor=tkinter.CENTER)

next_button = customtkinter.CTkButton(root,text="",command=skip_next,width=40,image=next_img)
next_button.place(relx=0.75,rely=0.7,anchor=tkinter.CENTER)


volume_slider = customtkinter.CTkSlider(root,from_=0,to=1,command=volume,width=250)
volume_slider.place(relx=0.5,rely=0.86,anchor=tkinter.CENTER)


progress_slider = customtkinter.CTkSlider(root,from_=0,to=1,width=250)
progress_slider.place(relx=0.5,rely=0.91,anchor=tkinter.CENTER)

progress_slider.bind("<ButtonPress-1>",start_drag)
progress_slider.bind("<ButtonRelease-1>",stop_drag)


root.mainloop()

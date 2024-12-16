from tkinter import filedialog
from tkinter import *
import pygame
import os

# Initialize the main application
root = Tk()
root.title('Music Player')
root.geometry("500x300")

# Initialize Pygame Mixer
pygame.mixer.init()

# Variables
songs = []
current_song = ""
paused = False

# Functions
def load_music():
    global current_song
    songs.clear()  # Clear the current song list
    songlist.delete(0, END)  # Clear the Listbox
    
    # Get the selected directory
    root.directory = filedialog.askdirectory()
    
    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            songs.append(song)
    
    for song in songs:
        songlist.insert("end", song)
    
    if songs:
        songlist.selection_set(0)
        current_song = songs[songlist.curselection()[0]]

def play_music():
    global current_song, paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        try:
            current_song = songs[songlist.curselection()[0]]
            pygame.mixer.music.load(os.path.join(root.directory, current_song))
            pygame.mixer.music.play()
        except IndexError:
            pass  # No song selected

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_music():
    global current_song
    try:
        current_index = songs.index(current_song)
        next_index = (current_index + 1) % len(songs)  # Wrap around to the start
        current_song = songs[next_index]
        
        # Update selection in Listbox
        songlist.selection_clear(0, END)
        songlist.selection_set(next_index)
        
        play_music()
    except ValueError:
        pass  # No valid current song

def prev_music():
    global current_song
    try:
        current_index = songs.index(current_song)
        prev_index = (current_index - 1) % len(songs)  # Wrap around to the end
        current_song = songs[prev_index]
        
        # Update selection in Listbox
        songlist.selection_clear(0, END)
        songlist.selection_set(prev_index)
        
        play_music()
    except ValueError:
        pass  # No valid current song

# Menu for loading music
menubar = Menu(root)
root.config(menu=menubar)
organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Select Folder', command=load_music)
menubar.add_cascade(label='Organise', menu=organise_menu)

# Song Listbox
songlist = Listbox(root, bg="black", fg="white", width=100, height=15)
songlist.pack()

# Control Buttons
play_btn_image = PhotoImage(file='play.png')
pause_btn_image = PhotoImage(file='pause.png')
next_btn_image = PhotoImage(file='next.png')
prev_btn_image = PhotoImage(file='previous.png')

control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame, image=play_btn_image, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_btn_image, borderwidth=0, command=next_music)
prev_btn = Button(control_frame, image=prev_btn_image, borderwidth=0, command=prev_music)

play_btn.grid(row=0, column=1, padx=7, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
prev_btn.grid(row=0, column=0, padx=7, pady=10)

# Run the main loop
root.mainloop()
#Imports
import random
import csv
import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk
import platform

tk.messagebox.showinfo(message="Copyright (C) 2022 Joseph McKeown\n"+
"This program is free software: you can redistribute it and/or modify "+
"it under the terms of the GNU General Public License as published by "+
"the Free Software Foundation, either version 3 of the License, or "+
"(at your option) any later version.\n\n"+
"This program is distributed in the hope that it will be useful, "+  
"but WITHOUT ANY WARRANTY; without even the implied warranty of "+
"MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\nSee the "+     
"GNU General Public License for more details.\n\n"+
"You should have received a copy of the GNU General Public License "+
"along with this program.  If not, see <http://www.gnu.org/licenses/>.")

#Constructing the dictionary of Tarot cards and their one word interpretations, using a csv as the source.
#The nth card in the global_deck_dict has the following properties:
#global_deck_dict[n] = [Card_Name, Meaning_Upright, Meaning_Reversed]
global_deck_dict = {}
with open("global_deck_dict.csv", newline="") as csvfile:
    deck_reader = csv.reader(csvfile)
    i = 0
    for row in deck_reader:
        global_deck_dict[i] = row
        i += 1

#Defining the TarotCard class.
#Each TarotCard has a value (dictionary key) and an orientation (1 is Upright, 2 is reversed).
class TarotCard:
    def __init__(self, value, orientation):
        self.value = value
        self.orientation = orientation
        self.title = global_deck_dict[value][0]
        self.interpretation = global_deck_dict[value][orientation]

#Defining functions.
#draw_card creates an instance of the TarotCard class, activated by a button.
def draw_card(some_input):
    global reading_type, reading_selected, user_cards, user_card_vals, no_of_cards, card_limit
    if (reading_selected and (no_of_cards < card_limit)):
        card_value = random.randint(0,77)
        card_orientation = random.randint(1,2)
        while(card_value in user_card_vals):
            card_value = random.randint(0,77)
            
        user_card_vals.append(card_value)
        user_cards.append(TarotCard(card_value,card_orientation))
        no_of_cards = len(user_card_vals)
        
        position_card(user_card_vals[-1],user_cards[-1].orientation,reading_type)
        
    elif ((card_limit != 0) and (no_of_cards >= card_limit)):
        tk.messagebox.showerror(message = "You have chosen the maximum number of cards for this spread.")
        
    else:
        tk.messagebox.showerror(message = "Please select a reading type.")

#position_card places the most recently drawn card in a window whose position depends on the spread.
#This function is called by draw_card.
def position_card(value,orientation,spread):
    global card_size, reading_type, user_card_vals, no_of_cards
    if spread == "ThreeCardSpread":
        pos1 = (midpoint[0]-int(3*card_size[0]/2),root_window_pos[1]-2*full_card_window_height)
        pos2 = (midpoint[0]-int(card_size[0]/2),root_window_pos[1]-2*full_card_window_height)
        pos3 = (midpoint[0]+int(card_size[0]/2),root_window_pos[1]-2*full_card_window_height)
        if no_of_cards == 1:
            create_card(value,orientation,pos1)
        elif no_of_cards == 2:
            create_card(value,orientation,pos2)
        elif no_of_cards == 3:
            create_card(value,orientation,pos3)
        else:
            tk.messagebox.showerror(message = "A card creation error has ocurred.")
    elif spread == "SelfLoveSpread":
        pos1 = (midpoint[0]-int(3*card_size[0]/2),root_window_pos[1]-2*full_card_window_height)
        pos2 = (midpoint[0]-int(card_size[0]/2),root_window_pos[1]-2*full_card_window_height)
        pos3 = (midpoint[0]+int(card_size[0]/2),root_window_pos[1]-2*full_card_window_height)
        pos4 = (midpoint[0]-int(card_size[0]/2),root_window_pos[1]-3*full_card_window_height)
        pos5 = (midpoint[0]-int(card_size[0]/2),root_window_pos[1]-full_card_window_height)
        if no_of_cards == 1:
            create_card(value,orientation,pos1)
        elif no_of_cards == 2:
            create_card(value,orientation,pos2)
        elif no_of_cards == 3:
            create_card(value,orientation,pos3)
        elif no_of_cards == 4:
            create_card(value,orientation,pos4)
        elif no_of_cards == 5:
            create_card(value,orientation,pos5)
        else:
            tk.messagebox.showerror(message = "A card creation error has ocurred.")
    elif spread == "JourneySpread":
        pos1 = (midpoint[0]-card_size[0]*2,screen_size_no_taskbar[1]-full_root_window_height-int(full_card_window_height*5/2))
        pos2 = (midpoint[0]-int(5*card_size[0]/2),screen_size_no_taskbar[1]-full_root_window_height-int(full_card_window_height*3/2))
        pos3 = (midpoint[0]-int(3*card_size[0]/2),pos2[1])
        pos4 = (midpoint[0]+int(card_size[0]/2),screen_size_no_taskbar[1]-full_root_window_height-2*full_card_window_height)
        pos5 = (midpoint[0]+int(3*card_size[0]/2),pos1[1])
        pos6 = (pos5[0],pos2[1])
        pos7 = (midpoint[0]+int(5*card_size[0]/2),pos4[1])
        if no_of_cards == 1:
            create_card(value,orientation,pos1)
        elif no_of_cards == 2:
            create_card(value,orientation,pos2)
        elif no_of_cards == 3:
            create_card(value,orientation,pos3)
        elif no_of_cards == 4:
            create_card(value,orientation,pos4)
        elif no_of_cards == 5:
            create_card(value,orientation,pos5)
        elif no_of_cards == 6:
            create_card(value,orientation,pos6)
        elif no_of_cards == 7:
            create_card(value,orientation,pos7)
        else:
            tk.messagebox.showerror(message = "A card creation error has ocurred.")
    else:
        tk.messagebox.showerror(message = "A spread error has occurred.")

#create_card provides the image and window for a drawn card.
#This function is called by position_card.
def create_card(val,ori,pos):
    global card_size, user_card_vals, global_deck_dict, no_of_cards, card_creation
    card_toplevel = tk.Toplevel(root_window)
    card_creation.append([card_toplevel])
    card_creation[-1][0].geometry(f"{card_size[0]}x{card_size[1]+label_height}+{pos[0]}+{pos[1]}")
    card_creation[-1][0].title(f"{global_deck_dict[val][0]}")
    card_frame = tk.Frame(card_toplevel)
    card_canvas = tk.Canvas(card_frame, width = card_size[0], height = card_size[1])
    card_img = (Image.open(f'Card_Images/{val}.jpg')).resize(card_size)
    if ((ori == 2) and (len(global_deck_dict[val][0]) > 21)):
        card_img = card_img.rotate(180)
        reversed_set = " (Reversed)"
        label_font = tk.font.Font(font = ('arial',-9,"normal"))
    elif ((ori == 2) and (len(global_deck_dict[val][0]) > 18)):
        card_img = card_img.rotate(180)
        reversed_set = " (Reversed)"
        label_font = tk.font.Font(font = ('arial',-10,"normal"))
    elif ((ori == 2) and (len(global_deck_dict[val][0]) > 15)):
        card_img = card_img.rotate(180)
        reversed_set = " (Reversed)"
        label_font = tk.font.Font(font = ('arial',-11,"normal"))
    else:
        reversed_set = ""
        label_font = tk.font.Font(font = ('arial',-12,"normal"))
    card_label = tk.Label(card_frame,text=f"{global_deck_dict[val][0] + reversed_set}", relief=tk.RAISED,
                          font = label_font,
                          image = tk.PhotoImage(width = 1, height = 1),
                          width = card_size[0],
                          height = label_height,
                          compound = "c")
        
    card_photo_img = ImageTk.PhotoImage(card_img)
    card_creation[-1].append(card_frame)
    card_creation[-1].append(card_canvas)
    card_creation[-1].append(card_img)
    card_creation[-1].append(card_photo_img)
    card_creation[-1].append(card_label)
    card_creation[-1][2].create_image(0,0,anchor="nw",image=card_creation[-1][4])
    card_creation[-1][1].pack()
    card_creation[-1][2].pack()
    card_creation[-1][5].pack()

#Some functions that define the type of spread chosen, activated by respective buttons.
def three_card_spread(some_input):
    global reading_type, reading_selected, card_limit
    reset_card_windows()
    reading_type = "ThreeCardSpread"
    reading_selected = True
    card_limit = 3

def self_love_spread(some_input):
    global reading_type, reading_selected, card_limit
    reset_card_windows()
    reading_type = "SelfLoveSpread"
    reading_selected = True
    card_limit = 5

def journey_spread(some_input):
    global reading_type, reading_selected, card_limit
    reset_card_windows()
    reading_type = "JourneySpread"
    reading_selected = True
    card_limit = 7

#reset_card_windows ensures that a new spread choice destroys existing cards and resets global variables to default.
#This function is called by three_card_spread, self_love_spread and journey_spread.
def reset_card_windows():
    global card_creation, user_card_vals, user_cards, no_of_cards, card_limit, reading_type, reading_selected
    for list_item in card_creation:
        list_item[0].destroy()
    user_card_vals = []
    user_cards = []
    no_of_cards = len(user_card_vals)
    card_limit = 0
    reading_type = ""
    reading_selected = False
    card_creation = []

#print_interpretation shows a message box that details the interpretation of the spread.
def print_interpretation(some_input):
    global reading_type, no_of_cards, user_cards
    interpretation_list = []
    for card in user_cards:
    		if card.orientation == 1:
    			interpretation_list.append(global_deck_dict[card.value][1])
    		elif card.orientation == 2:
    			interpretation_list.append(global_deck_dict[card.value][2])
    if ((reading_type == "ThreeCardSpread") and (no_of_cards == 3)):
        card1_string = f"Your first card, {user_cards[0].title}, represents past events that affect you.\nIts key word is {interpretation_list[0].lower()}.\n\n"
        card2_string = f"Your second card, {user_cards[1].title}, represents {interpretation_list[1].lower()} in your present situation.\n\n"
        card3_string = f"The final card, {user_cards[2].title}, gives information about the direction of things to come.\n{interpretation_list[2]} may become significant.\n"
        three_card_interpretation = card1_string + card2_string + card3_string
        tk.messagebox.showinfo(message = three_card_interpretation)
    elif ((reading_type == "SelfLoveSpread") and (no_of_cards == 5)):
        card1_string = f"{user_cards[0].title} represents {interpretation_list[0].lower()}.\nThis is what makes you wonderful.\n\n"
        card2_string = f"You should be proud of drawing {user_cards[1].title}.\nIt is characterised by {interpretation_list[1].lower()}.\n\n"
        card3_string = f"{user_cards[2].title} connects you to others.\nIt brings you with {interpretation_list[2].lower()}.\n\n"
        card4_string = f"Your negative thoughts are described by {user_cards[3].title}.\nPay mind to {interpretation_list[3].lower()}.\n\n"
        card5_string = f"{user_cards[4].title} is entwined with your positive thoughts.\n{interpretation_list[4]} is noteworthy for you."
        self_love_interpretation = card1_string + card2_string + card3_string + card4_string + card5_string
        tk.messagebox.showinfo(message = self_love_interpretation)
    elif ((reading_type == "JourneySpread") and (no_of_cards == 7)):
        card1to3_string = f"You drew {user_cards[0].title}, {user_cards[1].title} and {user_cards[2].title}.\nThese cards indicate that you are leaving behind aspects of {interpretation_list[0].lower()}, {interpretation_list[1].lower()} and {interpretation_list[2].lower()} in embarking on your journey.\n\n"
        card4_string = f"{user_cards[3].title} reveals the reason for your journey.\nConsider that {interpretation_list[3].lower()} moves you.\n\n"
        card5_string = f"Your path is lit by {user_cards[4].title}.\n{interpretation_list[4]} will be your guide.\n\n"
        card6_string = f"Beware {user_cards[5].title}.\n{interpretation_list[5]} may present an obstacle for you.\n\n"
        card7_string = f"Finally, {user_cards[6].title}.\nKeep in mind that your destination relates to {interpretation_list[6].lower()}.\n\n"
        journey_interpretation = card1to3_string + card4_string + card5_string + card6_string + card7_string
        tk.messagebox.showinfo(message = journey_interpretation)
    else:
    	tk.messagebox.showerror(message = "An interpretation error has occurred.\nPlease ensure you have drawn the correct number of cards.")

#Initialising necessary global variables.
user_card_vals = []                                          #A list of all card values drawn so far.
user_cards = []                                              #A list of all TarotCard instances created so far.
no_of_cards = len(user_card_vals)                            #The number of cards drawn so far.
card_limit = 0                                               #A limit on the number of cards that can be drawn.
reading_type = ""                                            #The type of spread.
reading_selected = False                                     #Boolean: has a reading been selected.
card_creation = []                                           #A list of all card windows and their widgets.
                                                             #card_creation =
                                                             #[[toplevel, frame, canvas, image, photoimage, label], etc.]

###############     Handling the UI.     ###############
#Opening a window for user input buttons.
root_window = tk.Tk()
screen_size = (root_window.winfo_screenwidth(),root_window.winfo_screenheight())

#Creating a button to force the root_window to update.
force_update_button = tk.Button()
force_update_button.pack()
force_update_button.update()

#Find taskbar and titlebar heights.
if platform.system() == "Windows":
    from win32api import GetMonitorInfo, MonitorFromPoint
    from win32gui import GetWindowRect, GetClientRect, FindWindow
    monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
    work_area = monitor_info.get("Work")
    taskbar_height = screen_size[1]-work_area[3]
    force_update_button.destroy()

    root_window_handle = FindWindow(None, "tk")
    rect = GetWindowRect(root_window_handle)
    client_rect = GetClientRect(root_window_handle)
    windowOffset = int((rect[2]-rect[0]-client_rect[2])/2)
    titlebar_height = int(rect[3]-rect[1]-client_rect[3]-windowOffset)
else:
    taskbar_height = 40
    titlebar_height = 31

#Setting the font for future windows.
font = tk.font.Font(font = ("arial",-12,"normal"))

#Usable screen space.
screen_size_no_taskbar = (screen_size[0],screen_size[1]-taskbar_height)

#Positions on screen.
midpoint = (int(screen_size[0]/2),int(screen_size_no_taskbar[1]/2))

#The root_window.
root_window_size = (int(screen_size[0]/4),int(screen_size_no_taskbar[1]/4))
full_root_window_height = root_window_size[1]+titlebar_height
root_window_pos = (midpoint[0]-int(root_window_size[0]/2),screen_size_no_taskbar[1]-full_root_window_height)
root_window.geometry(f"{root_window_size[0]}x{root_window_size[1]}+{root_window_pos[0]}+{root_window_pos[1]}")
root_window.title("Tarot Reader")
root_window_interior = (int(root_window_size[0]*9/10),int(root_window_size[1]*9/10))

#The card windows.
full_card_window_height = int((screen_size_no_taskbar[1]-full_root_window_height)/3)
card_height = int(7*(full_card_window_height-titlebar_height)/8)
label_height = int(card_height/7)
card_size = (int(0.9*card_height),card_height)

#Creating frames for packing widgets in the root_window.
top_frame = tk.Frame(root_window)
top_frame.pack(side="top")

bottom_frame = tk.Frame(root_window)
bottom_frame.pack(side="bottom")

upper_bottom_frame = tk.Frame(bottom_frame)
upper_bottom_frame.pack(side="top")

lower_bottom_frame = tk.Frame(bottom_frame)
lower_bottom_frame.pack(side="bottom")

#Creating a button which draws a single card.
draw_card_button = tk.Button(
    font = font,
    master = upper_bottom_frame,
    text = "Draw a card.",
    width = root_window_interior[0],
    height = int(root_window_interior[1]/3),
    bg = "#66369D",
    fg = "white",
    image = tk.PhotoImage(width = 1, height = 1),
    compound = "c"
    )

draw_card_button.bind("<Button 1>", draw_card)
draw_card_button.pack(side="top")

draw_card_button.update()
button_width = draw_card_button.winfo_width()

#Creating some buttons to select the type of reading.
three_card_spread_button = tk.Button(
    font = font,
    master = top_frame,
    text = "Three\nCard\nSpread",
    width = int(root_window_interior[0]/3)-8,
    height = int(root_window_interior[1]/3),
    bg = "#BF9553",
    fg = "white",
    image = tk.PhotoImage(width = 1, height = 1),
    compound = "c"
    )

self_love_spread_button = tk.Button(
    font = font,
    master = top_frame,
    text = "Self\nLove\nSpread",
    width = int(root_window_interior[0]/3),
    height = int(root_window_interior[1]/3),
    bg = "#BF9553",
    fg = "white",
    image = tk.PhotoImage(width = 1, height = 1),
    compound = "c"
    )

journey_spread_button = tk.Button(
    font = font,
    master = top_frame,
    text = "Journey\nSpread",
    width = int(root_window_interior[0]/3)-8,
    height = int(root_window_interior[1]/3),
    bg = "#BF9553",
    fg = "white",
    image = tk.PhotoImage(width = 1, height = 1),
    compound = "c"
    )

three_card_spread_button.bind("<Button 1>", three_card_spread)
three_card_spread_button.pack(side = "left")
self_love_spread_button.bind("<Button 1>", self_love_spread)
self_love_spread_button.pack(side = "left")
journey_spread_button.bind("<Button 1>", journey_spread)
journey_spread_button.pack(side = "left")

#Creating a button which prints the list of cards drawn so far (for debugging).
print_interpretation_button = tk.Button(
    font = font,
    master = lower_bottom_frame,
    text = "Interpret\nCards",
    width = root_window_interior[0],
    height = int(root_window_interior[1]/3),
    bg = "black",
    fg = "white",
    image = tk.PhotoImage(width = 1, height = 1),
    compound = "c"
    )

print_interpretation_button.bind("<Button 1>", print_interpretation)
print_interpretation_button.pack()

root_window.mainloop()

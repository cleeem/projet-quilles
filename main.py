from genericpath import exists
import tkinter
from tkinter import font
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
import os
import datetime

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


PATH = os.path.dirname(os.path.realpath(__file__))

def addincsv(url_file, objet, newline =True, delimiter =  None):
        csv = open(url_file,'a',encoding='utf-8')
        if newline:
            csv.write((str(objet)+'\n'))
        else:
            csv.write(str(objet))
            csv.write(str(delimiter))
        csv.close()

class App(customtkinter.CTk):

    APP_NAME = "CustomTkinter example_background_image.py"
    WIDTH = 2400
    HEIGHT = 1080

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.minsize(1080, 720)
        
        # self.resizable(True, True)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
   
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=200)

        self.position_y = 0.1
        self.max_position_y = 0
        self.list_entry = []
        self.list_label = []
        self.list_button = []
        self.nb_player = 0
        self.nb_coups = 9
        
        self.player_data = {}
        self.current_player = 0
        self.current_coup = 0
        self.click = True
        self.peut_sauvegarder = True

        self.retour_arriere = ImageTk.PhotoImage(Image.open(PATH + "/delete.png").resize((45,45), Image.ANTIALIAS))
        self.x_mark = ImageTk.PhotoImage(Image.open(PATH + "/x_mark.png").resize((60,60), Image.ANTIALIAS))

        self.creation()

# creation des différents frames et/ou boutons
    def creation(self):
        # differents frames

        self.frame1 = customtkinter.CTkFrame(master=self, width=500, height=630, corner_radius=15, fg_color=("gray70", "gray25"))
        self.frame1.place(relx=0.165, rely=0.45, anchor=tkinter.CENTER)

        self.frame2 = customtkinter.CTkFrame(master=self, width=500, height=200, corner_radius=15, fg_color=("gray70", "gray25"))
        self.frame2.place(relx=0.165, rely=0.885, anchor=tkinter.CENTER)

        self.frame3 = customtkinter.CTkFrame(master=self, width=1250, height=630, corner_radius=15, fg_color=("gray70", "gray25"))
        self.frame3.place(relx=0.635, rely=0.45, anchor=tkinter.CENTER)

        self.frame4 = customtkinter.CTkFrame(master=self, width=1250, height=200, corner_radius=15, fg_color=("gray70", "gray25"))
        self.frame4.place(relx=0.635, rely=0.885, anchor=tkinter.CENTER)

        self.frame5 = customtkinter.CTkFrame(master=self, width=500, height=110, corner_radius=15, fg_color=("gray70", "gray25"))
        self.frame5.place(relx=0.165, rely=0.06, anchor=tkinter.CENTER)

        self.frame6 = customtkinter.CTkFrame(master=self, width=1250, height=110, corner_radius=15, fg_color=("gray70", "gray25"))
        self.frame6.place(relx=0.635, rely=0.06, anchor=tkinter.CENTER)

        self.frame7 = customtkinter.CTkFrame(master=self.frame3, width=100, height=600, corner_radius=15, fg_color=("gray70" ,"gray20"))
        self.frame7.place(relx=0.91, rely=0.5, anchor=tkinter.CENTER)

        # textarea frame 1

        # entry = customtkinter.CTkEntry(master=self.frame1, corner_radius=6, width=200, placeholder_text="nom du joueur 1", fg_color="white", text_color="black")
        # entry.place(relx=0.5, rely=self.position_y, anchor=tkinter.CENTER)
        # self.list_entry.append(entry)


        # label frame 5

        label = customtkinter.CTkLabel(master=self.frame5, text="joueurs", text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
        label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        label = customtkinter.CTkLabel(master=self.frame6, text=" 1             5            5           10           10             10           15           15           20              score"
                                        , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
        label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


        # buttons frame 2

        self.button_add_player = customtkinter.CTkButton(master=self.frame2, text="add player", corner_radius=6, command=self.add_player, width=210, height=75, text_font=("Roboto Medium", -30))
        self.button_add_player.place(relx=0.28, rely=0.3, anchor=tkinter.CENTER)
        self.list_button.append(self.button_add_player)

        self.button_remove_player = customtkinter.CTkButton(master=self.frame2, text="remove player", corner_radius=6, command=self.remove_player, width=210, height=75, text_font=("Roboto Medium", -30))
        self.button_remove_player.place(relx=0.28, rely=0.7, anchor=tkinter.CENTER)
        self.list_button.append(self.button_remove_player)

        # self.button_reset = customtkinter.CTkButton(master=self.frame2, text="reset", corner_radius=6, command=self.reset, width=210,  height=75, text_font=("Roboto Medium", -30))
        # self.button_reset.place(relx=0.72, rely=0.7, anchor=tkinter.CENTER)

        self.button_valider = customtkinter.CTkButton(master=self.frame2, text="valider", corner_radius=6, command=self.valider, width=210, height=75, text_font=("Roboto Medium", -30))
        self.button_valider.place(relx=0.72, rely=0.3, anchor=tkinter.CENTER)
        self.list_button.append(self.button_valider)

        self.optionmenu_1 = customtkinter.CTkComboBox(master=self.frame2, 
                                                    values=["ancien resultats", "clear", "save", "reset", "color:Dark", "color:Light"], 
                                                    command=self.multi, width=210, height=75,
                                                    text_font=("Roboto Medium", -30), dropdown_text_font=("Roboto Medium", -40), button_color="gray")
        self.optionmenu_1.set("       ⚙")
        self.optionmenu_1.place(relx=0.72, rely=0.7, anchor=tkinter.CENTER)
        self.list_button.append(self.optionmenu_1)


        # buttons frame 4

        self.button_write_1 = customtkinter.CTkButton(master=self.frame4, text="1", text_font=("Roboto Medium", -30), corner_radius=6, command=self.write_1, width=100, height=100)
        self.button_write_1.place(relx=0.05, rely=0.5, anchor=tkinter.CENTER)
        self.list_button.append(self.button_write_1)

        self.button_write_2 = customtkinter.CTkButton(master=self.frame4, text="2", text_font=("Roboto Medium", -30), corner_radius=6, command=self.write_2,  width=100, height=100)
        self.button_write_2.place(relx=0.135, rely=0.5, anchor=tkinter.CENTER)
        self.list_button.append(self.button_write_2)

        self.button_write_3 = customtkinter.CTkButton(master=self.frame4, text="3", text_font=("Roboto Medium", -30), corner_radius=6, command=self.write_3, width=100, height=100)
        self.button_write_3.place(relx=0.22, rely=0.5, anchor=tkinter.CENTER)
        self.list_button.append(self.button_write_3)

        self.button_write_4 = customtkinter.CTkButton(master=self.frame4, text="4", text_font=("Roboto Medium", -30), corner_radius=6, command=self.write_4, width=100, height=100)
        self.button_write_4.place(relx=0.305, rely=0.5, anchor=tkinter.CENTER)
        self.list_button.append(self.button_write_4)

        self.button_write_5 = customtkinter.CTkButton(master=self.frame4, text="5", text_font=("Roboto Medium", -30), corner_radius=6, command=self.write_5, width=100, height=100)
        self.button_write_5.place(relx=0.39, rely=0.5, anchor=tkinter.CENTER)
        self.list_button.append(self.button_write_5)

        self.button_write_6 = customtkinter.CTkButton(master=self.frame4, text="6", text_font=("Roboto Medium", -30), corner_radius=6, command=self.write_6, width=100, height=100)
        self.button_write_6.place(relx=0.475, rely=0.5, anchor=tkinter.CENTER)
        self.list_button.append(self.button_write_6)

        self.button_write_7 = customtkinter.CTkButton(master=self.frame4, text="7", text_font=("Roboto Medium", -30), corner_radius=6, command=self.write_7, width=100, height=100)
        self.button_write_7.place(relx=0.560, rely=0.5, anchor=tkinter.CENTER)
        self.list_button.append(self.button_write_7)

        self.button_write_8 = customtkinter.CTkButton(master=self.frame4, text="8", text_font=("Roboto Medium", -30), corner_radius=6, command=self.write_8, width=100, height=100)
        self.button_write_8.place(relx=0.645, rely=0.5, anchor=tkinter.CENTER)
        self.list_button.append(self.button_write_8)

        self.button_write_9 = customtkinter.CTkButton(master=self.frame4, text="9", text_font=("Roboto Medium", -30), corner_radius=6, command=self.write_9, width=100, height=100)
        self.button_write_9.place(relx=0.730, rely=0.5, anchor=tkinter.CENTER)
        self.list_button.append(self.button_write_9)

        self.button_write_0 = customtkinter.CTkButton(master=self.frame4, text="0", text_font=("Roboto Medium", -30), corner_radius=6, command=self.write_0, width=100, height=100)
        self.button_write_0.place(relx=0.815, rely=0.5, anchor=tkinter.CENTER)
        self.list_button.append(self.button_write_0)

        self.button_remove_scores = customtkinter.CTkButton(master=self.frame4, text="", image=self.retour_arriere, corner_radius=6, command=self.delete_score, width=130, height=100)
        self.button_remove_scores.place(relx=0.925, rely=0.5, anchor=tkinter.CENTER)
        self.list_button.append(self.button_remove_scores)

    def crea_fin(self):
        self.frame_fini = customtkinter.CTkFrame(master=self, width=600, height=500, corner_radius=15, fg_color=("gray70" ,"gray15"), bg_color=("gray70" ,"gray25"))
        self.frame_fini.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.button_save_and_new = customtkinter.CTkButton(master=self.frame_fini, text="sauvegarder et nouvelle partie", corner_radius=6, command=self.save_and_new,
                                                    width=575, height=100, text_font=("Roboto Medium", -30))
        self.button_save_and_new.place(relx=0.5, rely=0.125, anchor=tkinter.CENTER)

        self.button_save = customtkinter.CTkButton(master=self.frame_fini, text="sauvegarder", corner_radius=6, command=self.sauvegarder,
                                                    width=575, height=100, text_font=("Roboto Medium", -30))
        self.button_save.place(relx=0.5, rely=0.375, anchor=tkinter.CENTER)

        self.button_ancien_resultats = customtkinter.CTkButton(master=self.frame_fini, text="voir les anciens résultats", corner_radius=6, command=self.resultats,
                                                    width=575, height=100, text_font=("Roboto Medium", -30))
        self.button_ancien_resultats.place(relx=0.5, rely=0.625, anchor=tkinter.CENTER)

        self.button_quit = customtkinter.CTkButton(master=self.frame_fini, text="quitter", corner_radius=6, command=self.on_closing,
                                                    width=575, height=100, text_font=("Roboto Medium", -30))
        self.button_quit.place(relx=0.5, rely=0.875, anchor=tkinter.CENTER)

    def crea_logs(self):
        try:
            self.frame_fini.destroy()
        except:
            pass

        self.frame_logs = customtkinter.CTkFrame(master=self, width=App.WIDTH, height=App.HEIGHT, corner_radius=15, fg_color=("gray70", "gray25"))
        self.frame_logs.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.frame_left = customtkinter.CTkFrame(master=self.frame_logs, width=800, height=1000, corner_radius=15, fg_color=("gray70", "gray20"))
        self.frame_left.place(relx=0.3, rely=0.5, anchor=tkinter.CENTER)

        self.frame_right = customtkinter.CTkFrame(master=self.frame_logs, width=800, height=1000, corner_radius=15, fg_color=("gray70", "gray20"))
        self.frame_right.place(relx=0.7, rely=0.5, anchor=tkinter.CENTER)

        self.button_remove_scores = customtkinter.CTkButton(master=self.frame_logs, text="", image=self.x_mark, corner_radius=6,
                                                            command=self.supprimer, width=80, height=80)
        self.button_remove_scores.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        
# commandes
    def multi(self, arg):
        if arg == "clear":
            self.clear()
        
        elif arg == "save":
            self.sauvegarder()

        elif arg == "reset":
            self.reset()

        elif "Light" in arg:
            self.change_appearance_mode("Light")
        
        elif "Dark" in arg:
            self.change_appearance_mode("Dark")

        elif arg == "ancien resultats":
            self.resultats()
            
    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.optionmenu_1.set("more")
            
    def add_player(self):
        if self.nb_player < 5:
            self.nb_player += 1

            entry = customtkinter.CTkEntry(master=self.frame1, corner_radius=6, width=300, height=70,text_font=("Roboto Medium", -30), placeholder_text="username", fg_color="white", text_color="black")
            entry.place(relx=0.5, rely=self.position_y, anchor=tkinter.CENTER)

            self.list_entry.append(entry)

            self.position_y += 0.2

    def remove_player(self):
        if self.nb_player > 1:
            self.position_y -= 0.2
            self.nb_player -= 1
            
            entry = self.list_entry[-1]
            entry.destroy()
            self.list_entry.pop(-1)

    def reset(self):
        
        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()
        self.frame4.destroy()
        self.frame6.destroy()
        self.frame6.destroy()
        self.frame7.destroy()

        self.list_label = []
        self.list_entry = []
        self.list_button = []
        self.player_data = {}

        self.position_y = 0.1
        self.nb_player = 0
        self.current_coup = 0
        self.current_player = 0

        self.creation()
        self.add_player()
        self.click = True
        self.peut_sauvegarder = True

    def valider(self):
        if self.player_data == {}:               

            self.position_y = 0.1
            for i,entry in enumerate(self.list_entry):
                nom = entry.get()
                if nom == "":
                    nom = "anonyme"

                self.player_data[i] = [["_" for i in range(9)], nom]
                self.position_y += 0.2

            self.max_position_y = self.position_y - 0.2
            self.position_y = 0.1

            self.current_coup = 0
            self.current_player = 0

    def sauvegarder(self):
        if self.peut_sauvegarder:
            self.peut_sauvegarder = False
            self.optionmenu_1.set("more")
            date = str(datetime.date.today())
            if not exists("logs"):
                os.mkdir("logs")
            if not exists(f"logs/{date}.txt"):
                open(f"logs/{date}.txt", "w")
            for values in self.player_data.values():
                resultat = str(values[0]).replace("[","").replace("]","").replace("'","").replace("'","").replace(",","")
                nom = str(values[1])
                
                ligne = f"coups : {str(resultat)} || score : {str(values[2])} || joueur : {nom}"
                addincsv(f"logs/{date}.txt", ligne)

            self.button_save = customtkinter.CTkButton(master=self.frame_fini, text="sauvegarder ✔", corner_radius=6, command=self.sauvegarder,
                                                        width=575, height=100, text_font=("Roboto Medium", -30))
            self.button_save.place(relx=0.5, rely=0.375, anchor=tkinter.CENTER)

    def clear(self):
        self.frame3.destroy()

        self.frame3 = customtkinter.CTkFrame(master=self, width=1250, height=630, corner_radius=15, fg_color=("gray70", "gray25"))
        self.frame3.place(relx=0.635, rely=0.45, anchor=tkinter.CENTER)

        self.frame7 = customtkinter.CTkFrame(master=self.frame3, width=100, height=600, corner_radius=15, fg_color=("gray70" ,"gray20"))
        self.frame7.place(relx=0.91, rely=0.5, anchor=tkinter.CENTER)

        self.list_label = []

        self.position_y = 0.1
        self.nb_player = 0
        self.current_coup = 0
        self.current_player = 0
        
        for k,v in self.player_data.items():
            v[0] = ["_" for i in range(9)]
            self.nb_player += 1

        self.optionmenu_1.set("more")

    def save_and_new(self):
        self.sauvegarder()
        self.reset()

    def supprimer(self):
        self.frame_logs.destroy()
        if not self.click:
            self.crea_fin()
        
    def calcul(self):
        for player,liste in self.player_data.items():
            resultat = sum(liste[0])
            
            label = customtkinter.CTkLabel(master=self.frame7, text= resultat , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
            label.place(relx=0.5, rely=self.position_y, anchor=tkinter.CENTER)
            
            self.list_label.append(label)

            liste.append(resultat)

            if self.position_y < self.max_position_y:
                self.position_y += 0.2

            for button in self.list_button:
                button.configure(state=tkinter.DISABLED)

            self.crea_fin()
            
    def resultats(self):
        self.crea_logs()

        date = str(datetime.date.today())
        tous_les_fichiers = os.listdir("logs")

        y_position = 0.1
        x_position = 0.5
        self.compteur = 0
        bon_frame = self.frame_left

        for file in tous_les_fichiers:
            if os.path.isfile(os.path.join("logs", file)):

                fichier = open(os.path.join("logs", file),'r')
                lines = fichier.readlines()
                for ligne in lines:
                    
                    label = customtkinter.CTkLabel(master=bon_frame, text= ligne , text_font=("Roboto Medium", -25), text_color="white")  # font name and size in px
                    label.place(relx=x_position, rely=y_position, anchor = tkinter.CENTER)

                    if y_position < 0.8:
                        self.compteur += 1
                        y_position += 0.1
                    else:
                        self.compteur += 1
                        y_position = 0.1
                        bon_frame = self.frame_right

    def delete_score(self):
        self.click = True
        if self.nb_player > 1:
            if self.current_player == 0:
                
                self.current_player = self.nb_player - 1
                self.current_coup -= 1
                
                self.position_y = self.max_position_y

                self.list_label.pop(-1)

                self.player_data[self.current_player][0][self.current_coup] = "_"

                resultat = str(self.player_data[self.current_player][0]).replace("[","").replace("]","").replace("'","").replace("'","").replace(",","            ")
                
                label = customtkinter.CTkLabel(master=self.frame3, text= resultat , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
                label.place(relx=0.4255, rely=self.position_y, anchor=tkinter.CENTER)
                
                self.list_label.append(label)

            else:
                self.current_player -= 1
                self.position_y -= 0.2

                self.list_label.pop(-1)

                self.player_data[self.current_player][0][self.current_coup] = "_"

                resultat = str(self.player_data[self.current_player][0]).replace("[","").replace("]","").replace("'","").replace("'","").replace(",","            ")
                
                label = customtkinter.CTkLabel(master=self.frame3, text= resultat , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
                label.place(relx=0.4255, rely=self.position_y, anchor=tkinter.CENTER)
                
                self.list_label.append(label)

        else:
            self.list_label.pop(-1)

            self.player_data[self.current_player][0][self.current_coup] = "_"

            resultat = str(self.player_data[self.current_player][0]).replace("[","").replace("]","").replace("'","").replace("'","").replace(",","            ")
            
            label = customtkinter.CTkLabel(master=self.frame3, text= resultat , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
            label.place(relx=0.4255, rely=self.position_y, anchor=tkinter.CENTER)
            
            self.list_label.append(label)
            if self.current_coup > 0:
                self.current_coup -= 1
            else:
                self.current_coup = 0


    def update(self):
        
        if self.nb_player > 1:
            
            if self.position_y >= self.max_position_y:
                self.position_y = 0.1
            else:
                self.position_y += 0.2

            if self.current_player +1 == self.nb_player:
                self.current_player = 0
                self.list_label.pop(0)

                if self.current_coup < 8:
                    self.current_coup += 1
                else:
                    self.current_coup += 1
                    self.click = False
                    self.calcul()
            else:
                self.current_player += 1
        else:
            if self.current_coup < 8:
                self.current_coup += 1
            else:
                self.current_coup += 1
                self.click = False
                self.calcul()


# commandes des boutons
    def write_1(self):
        if self.click:
            self.player_data[self.current_player][0][self.current_coup] = 1

            resultat = str(self.player_data[self.current_player][0]).replace("[","").replace("]","").replace("'","").replace("'","").replace(",","            ")
            
            label = customtkinter.CTkLabel(master=self.frame3, text= resultat , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
            label.place(relx=0.4255, rely=self.position_y, anchor=tkinter.CENTER)
            
            self.list_label.append(label)

            self.update()

    def write_2(self):
        if self.click:
            self.player_data[self.current_player][0][self.current_coup] = 2

            resultat = str(self.player_data[self.current_player][0]).replace("[","").replace("]","").replace("'","").replace(",","            ")
            
            label = customtkinter.CTkLabel(master=self.frame3, text= resultat , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
            label.place(relx=0.4255, rely=self.position_y, anchor=tkinter.CENTER)

            self.list_label.append(label)

            self.update()

    def write_3(self):
        if self.click:
            self.player_data[self.current_player][0][self.current_coup] = 3
  
            resultat = str(self.player_data[self.current_player][0]).replace("[","").replace("]","").replace("'","").replace(",","            ")
            
            label = customtkinter.CTkLabel(master=self.frame3, text= resultat , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
            label.place(relx=0.4255, rely=self.position_y, anchor=tkinter.CENTER)

            self.list_label.append(label)

            self.update()

    def write_4(self):
        if self.click:
            self.player_data[self.current_player][0][self.current_coup] = 4

            resultat = str(self.player_data[self.current_player][0]).replace("[","").replace("]","").replace("'","").replace(",","            ")
            
            label = customtkinter.CTkLabel(master=self.frame3, text= resultat , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
            label.place(relx=0.4255, rely=self.position_y, anchor=tkinter.CENTER)
            
            self.list_label.append(label)

            self.update()

    def write_5(self):
        if self.click:
            self.player_data[self.current_player][0][self.current_coup] = 5
        
            resultat = str(self.player_data[self.current_player][0]).replace("[","").replace("]","").replace("'","").replace(",","            ")
            
            label = customtkinter.CTkLabel(master=self.frame3, text= resultat , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
            label.place(relx=0.4255, rely=self.position_y, anchor=tkinter.CENTER)
            
            self.list_label.append(label)  

            self.update()

    def write_6(self):
        if self.click:
            self.player_data[self.current_player][0][self.current_coup] = 6
        
            resultat = str(self.player_data[self.current_player][0]).replace("[","").replace("]","").replace("'","").replace(",","            ")
            
            label = customtkinter.CTkLabel(master=self.frame3, text= resultat , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
            label.place(relx=0.4255, rely=self.position_y, anchor=tkinter.CENTER)
            
            self.list_label.append(label)   

            self.update()

    def write_7(self):
        if self.click:
            self.player_data[self.current_player][0][self.current_coup] = 7

            resultat = str(self.player_data[self.current_player][0]).replace("[","").replace("]","").replace("'","").replace(",","            ")
            
            label = customtkinter.CTkLabel(master=self.frame3, text= resultat , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
            label.place(relx=0.4255, rely=self.position_y, anchor=tkinter.CENTER)
            
            self.list_label.append(label)    

            self.update()

    def write_8(self):
        if self.click:
            self.player_data[self.current_player][0][self.current_coup] = 8
        
            resultat = str(self.player_data[self.current_player][0]).replace("[","").replace("]","").replace("'","").replace(",","            ")
            
            label = customtkinter.CTkLabel(master=self.frame3, text= resultat , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
            label.place(relx=0.4255, rely=self.position_y, anchor=tkinter.CENTER)
            
            self.list_label.append(label)   

            self.update()

    def write_9(self):
        if self.click:
            self.player_data[self.current_player][0][self.current_coup] = 9
        
            resultat = str(self.player_data[self.current_player][0]).replace("[","").replace("]","").replace("'","").replace(",","            ")
            
            label = customtkinter.CTkLabel(master=self.frame3, text= resultat , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
            label.place(relx=0.4255, rely=self.position_y, anchor=tkinter.CENTER)
            
            self.list_label.append(label)   

            self.update()

    def write_0(self):
        if self.click:
            self.player_data[self.current_player][0][self.current_coup] = 0
        
            resultat = str(self.player_data[self.current_player][0]).replace("[","").replace("]","").replace("'","").replace(",","            ")
        
            label = customtkinter.CTkLabel(master=self.frame3, text= resultat , text_font=("Roboto Medium", -30), text_color="white")  # font name and size in px
            label.place(relx=0.4255, rely=self.position_y, anchor=tkinter.CENTER)
            
            self.list_label.append(label)

            self.update()


    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
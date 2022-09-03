# import wget
# url = "https://github.com/IshraqueSarwar/IAO-Test-suite-WinBuild/raw/main/question_datafiles/IGCSE/Chemistry_paper_1.pickle.zip"
# wget.download(url,"question_datafiles")


import tkinter
import customtkinter
import os
from tkinter import ttk
import wget
import zipfile
from tqdm import tqdm

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")


class Setup(customtkinter.CTk):
    WIDTH = 680
    HEIGHT = 500
    text_font_size =("Noto Sans CJK TC Black", -10)
    title_font =("Noto Sans CJK TC Black", -14)

    download_keys = []

    sub_dict = {
    "Biology": ["https://github.com/IshraqueSarwar/question_datafiles/raw/main/IGCSE/Biology_paper_1.pickle.zip", "https://github.com/IshraqueSarwar/question_datafiles/raw/main/IGCSE/Biology_paper_2.pickle.zip"],
    "Chemistry": ["https://github.com/IshraqueSarwar/question_datafiles/raw/main/IGCSE/Chemistry_paper_1.pickle.zip", "https://github.com/IshraqueSarwar/question_datafiles/raw/main/IGCSE/Chemistry_paper_2.pickle.zip"],
    "Physics": ["https://github.com/IshraqueSarwar/question_datafiles/raw/main/IGCSE/Physics_paper_1.pickle.zip", "https://github.com/IshraqueSarwar/question_datafiles/raw/main/IGCSE/Physics_paper_2.pickle.zip"],
    "Maths-B": ["https://github.com/IshraqueSarwar/question_datafiles/raw/main/IGCSE/Maths-B_paper_1.pickle.zip", "https://github.com/IshraqueSarwar/question_datafiles/raw/main/IGCSE/Maths-B_paper_2.pickle.zip"],
    "Maths-A": ["https://github.com/IshraqueSarwar/question_datafiles/raw/main/IGCSE/Maths-A_paper_1.pickle.zip", "https://github.com/IshraqueSarwar/question_datafiles/raw/main/IGCSE/Maths-A_paper_2.pickle.zip"],
    "PureMaths": ["https://github.com/IshraqueSarwar/question_datafiles/raw/main/IGCSE/PureMaths_paper_1.pickle.zip", "https://github.com/IshraqueSarwar/question_datafiles/raw/main/IGCSE/PureMaths_paper_2.pickle.zip"],


    "Physics1":["https://github.com/IshraqueSarwar/question_datafiles/raw/main/IAL/Physics_unit_1.pickle.zip","https://github.com/IshraqueSarwar/question_datafiles/raw/main/IAL/Physics_unit_2.pickle.zip","https://github.com/IshraqueSarwar/question_datafiles/raw/main/IAL/Physics_unit_3.pickle.zip"],
    "Physics2":["https://github.com/IshraqueSarwar/question_datafiles/raw/main/IAL/Physics_unit_4.pickle.zip","https://github.com/IshraqueSarwar/question_datafiles/raw/main/IAL/Physics_unit_5.pickle.zip","https://github.com/IshraqueSarwar/question_datafiles/raw/main/IAL/Physics_unit_6.pickle.zip"],
    "Chemistry1": ["https://github.com/IshraqueSarwar/question_datafiles/raw/main/IAL/Chemistry_unit_1.pickle.zip","https://github.com/IshraqueSarwar/question_datafiles/raw/main/IAL/Chemistry_unit_2.pickle.zip","https://github.com/IshraqueSarwar/question_datafiles/raw/main/IAL/Chemistry_unit_3.pickle.zip"],
    "Chemistry2": ["https://github.com/IshraqueSarwar/question_datafiles/raw/main/IAL/Chemistry_unit_4.pickle.zip","https://github.com/IshraqueSarwar/question_datafiles/raw/main/IAL/Chemistry_unit_5.pickle.zip","https://github.com/IshraqueSarwar/question_datafiles/raw/main/IAL/Chemistry_unit_6.pickle.zip"],
    }



    def __init__(self):
        super().__init__()

        self.title('setup')
        self.geometry(f"{Setup.WIDTH}x{Setup.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(False,False)

        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(15,weight = 1)

        self.labelTitle = customtkinter.CTkLabel(master = self, text = "Please select the subjects you want to download", text_font = Setup.title_font, justify = tkinter.CENTER)
        self.labelTitle.grid(column = 0,row = 0,pady = 4, padx=4, columnspan = 5)


        # IGCSE
        self.labelIGCSE = customtkinter.CTkLabel(master = self, text = "IGCSE", text_font = Setup.title_font)
        self.labelIGCSE.grid(row = 1,column = 0,pady = 4, padx=4, columnspan = 2,sticky = 'nsew')
       
        ttk.Separator(self, orient=tkinter.VERTICAL).grid(column=2, row=2, rowspan= 14, sticky='ns')

        self.phy = customtkinter.CTkCheckBox(master = self,text = "Physics (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.phy_func)
        self.phy.grid(row = 2, column = 0, padx = 20, pady = 10, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/Physics_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/Physics_paper_2.pickle"):
            self.phy.select()
            self.phy.configure(state = tkinter.DISABLED)


        self.chem = customtkinter.CTkCheckBox(master = self,text = "Chemistry (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.chem_func)
        self.chem.grid(row = 3, column = 0,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/Chemistry_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/Chemistry_paper_2.pickle"):
            self.chem.select()
            self.chem.configure(state = tkinter.DISABLED)


        self.bio = customtkinter.CTkCheckBox(master = self,text = "Biology (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.bio_func)
        self.bio.grid(row = 4, column = 0,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/Biology_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/Biology_paper_2.pickle"):
            self.bio.select()
            self.bio.configure(state = tkinter.DISABLED)


        self.mb = customtkinter.CTkCheckBox(master = self,text = "Maths B (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.mb_func)
        self.mb.grid(row = 2, column = 1,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/Maths-B_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/Maths-B_paper_2.pickle"):
            self.mb.select()
            self.mb.configure(state = tkinter.DISABLED)



        self.ma = customtkinter.CTkCheckBox(master = self,text = "Maths A (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.ma_func)
        self.ma.grid(row = 3, column = 1,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/Maths-A_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/Maths-A_paper_2.pickle"):
            self.ma.select()
            self.ma.configure(state = tkinter.DISABLED)

        self.pm = customtkinter.CTkCheckBox(master = self,text = "Pure Maths (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.pm_func)
        self.pm.grid(row = 4, column = 1,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/PureMaths_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/PureMaths_paper_2.pickle"):
            self.pm.select()
            self.pm.configure(state = tkinter.DISABLED)


        # IAL
        self.labelIAL = customtkinter.CTkLabel(master = self, text = "IAL", text_font = Setup.title_font, height = 20,width = 20)
        self.labelIAL.grid(row = 1,column = 3,pady = 4, padx=20, columnspan = 2, sticky = 'nsew')
        
        self.phy1 = customtkinter.CTkCheckBox(master = self,text = "Physics unit-(1-3)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.phy1_func)
        self.phy1.grid(row = 2, column = 4, padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Physics_unit_1.pickle") and os.path.exists("question_datafiles/IAL/Physics_unit_2.pickle") and os.path.exists("question_datafiles/IAL/Physics_unit_3.pickle"):
            self.phy1.select()
            self.phy1.configure(state = tkinter.DISABLED)


        self.phy2 = customtkinter.CTkCheckBox(master = self,text = "Physics unit-(4-6)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.phy2_func)
        self.phy2.grid(row = 3, column = 4,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Physics_unit_4.pickle") and os.path.exists("question_datafiles/IAL/Physics_unit_5.pickle") and os.path.exists("question_datafiles/IAL/Physics_unit_6.pickle"):
            self.phy2.select()
            self.phy2.configure(state = tkinter.DISABLED)

        self.chem1 = customtkinter.CTkCheckBox(master = self,text = "Chemistry unit-(1-3)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.chem1_func)
        self.chem1.grid(row = 4, column = 4,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Chemistry_unit_1.pickle") and os.path.exists("question_datafiles/IAL/Chemistry_unit_2.pickle") and os.path.exists("question_datafiles/IAL/Chemistry_unit_3.pickle"):
            self.chem1.select()
            self.chem1.configure(state = tkinter.DISABLED)


        self.chem2 = customtkinter.CTkCheckBox(master = self,text = "Chemistry unit-(4-6)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.chem2_func)
        self.chem2.grid(row = 5, column = 4,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Chemistry_unit_4.pickle") and os.path.exists("question_datafiles/IAL/Chemistry_unit_5.pickle") and os.path.exists("question_datafiles/IAL/Chemistry_unit_6.pickle"):
            self.chem2.select()
            self.chem2.configure(state = tkinter.DISABLED)

        self.bio1 = customtkinter.CTkCheckBox(master = self,text = "Biology unit-(1-3)",text_font = Setup.text_font_size, height = 20,width = 20)
        self.bio1.grid(row = 6, column = 4,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Biology_unit_1.pickle") and os.path.exists("question_datafiles/IAL/Biology_unit_2.pickle") and os.path.exists("question_datafiles/IAL/Biology_unit_3.pickle"):
            self.bio1.select()
            self.bio1.configure(state = tkinter.DISABLED)


        self.bio2 = customtkinter.CTkCheckBox(master = self,text = "Biology unit-(4-6)",text_font = Setup.text_font_size, height = 20,width = 20)
        self.bio2.grid(row = 7, column = 4,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Biology_unit_4.pickle") and os.path.exists("question_datafiles/IAL/Biology_unit_5.pickle") and os.path.exists("question_datafiles/IAL/Biology_unit_6.pickle"):
            self.bio2.select()
            self.bio2.configure(state = tkinter.DISABLED)



        self.p1 = customtkinter.CTkCheckBox(master = self,text = "PureMaths unit-1",text_font = Setup.text_font_size, height = 20,width = 20)
        self.p1.grid(row = 2, column = 3, padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/P1.pickle"):
            self.p1.select()
            self.p1.configure(state = tkinter.DISABLED)


        self.p2 = customtkinter.CTkCheckBox(master = self,text = "PureMaths unit-2",text_font = Setup.text_font_size, height = 20,width = 20)
        self.p2.grid(row = 3, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/P2.pickle"):
            self.p2.select()
            self.p2.configure(state = tkinter.DISABLED)

        self.p3 = customtkinter.CTkCheckBox(master = self,text = "PureMaths unit-3",text_font = Setup.text_font_size, height = 20,width = 20)
        self.p3.grid(row = 4, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/P3.pickle"):
            self.p3.select()
            self.p3.configure(state = tkinter.DISABLED)

        self.p4 = customtkinter.CTkCheckBox(master = self,text = "PureMaths unit-4",text_font = Setup.text_font_size, height = 20,width = 20)
        self.p4.grid(row = 5, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/P4.pickle"):
            self.p4.select()
            self.p4.configure(state = tkinter.DISABLED)

        self.fp1 = customtkinter.CTkCheckBox(master = self,text = "F.PureMaths unit-1",text_font = Setup.text_font_size, height = 20,width = 20)
        self.fp1.grid(row = 6, column = 3, padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Fp1.pickle"):
            self.fp1.select()
            self.fp1.configure(state = tkinter.DISABLED)


        self.fp2 = customtkinter.CTkCheckBox(master = self,text = "F.PureMaths unit-2",text_font = Setup.text_font_size, height = 20,width = 20)
        self.fp2.grid(row = 7, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Fp2.pickle"):
            self.fp2.select()
            self.fp2.configure(state = tkinter.DISABLED)

        self.fp3 = customtkinter.CTkCheckBox(master = self,text = "F.PureMaths unit-3",text_font = Setup.text_font_size, height = 20,width = 20)
        self.fp3.grid(row = 8, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Fp3.pickle"):
            self.fp3.select()
            self.fp3.configure(state = tkinter.DISABLED)


        self.m1 = customtkinter.CTkCheckBox(master = self,text = "Mechanics unit-1",text_font = Setup.text_font_size, height = 20,width = 20)
        self.m1.grid(row = 9, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/M1.pickle"):
            self.m1.select()
            self.m1.configure(state = tkinter.DISABLED)
        
        self.m2 = customtkinter.CTkCheckBox(master = self,text = "Mechanics unit-2",text_font = Setup.text_font_size, height = 20,width = 20)
        self.m2.grid(row = 10, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/M1.pickle"):
            self.m2.select()
            self.m2.configure(state = tkinter.DISABLED)


        self.m3 = customtkinter.CTkCheckBox(master = self,text = "Mechanics unit-3",text_font = Setup.text_font_size, height = 20,width = 20)
        self.m3.grid(row = 11, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/M1.pickle"):
            self.m3.select()
            self.m3.configure(state = tkinter.DISABLED)





        # Download button
        self.download_button = customtkinter.CTkButton(master = self,
                                                text = "Download",
                                                text_font = Setup.title_font,
                                                command = self.download)
        self.download_button.grid(row = 14, column = 4, pady = 10, padx=20, rowspan = 2, sticky = 's')



    def download(self):
        exit = False
        print("Starting Download! This may take a while...")
        for subject in Setup.download_keys:
            for i in range(len(Setup.sub_dict[subject])):
                link = Setup.sub_dict[subject][i]
                temp = link.split('/')
                path = temp[-2]+'/'+temp[-1]
                print(f"Downloading {temp[-1]}")
                try:
                    wget.download(link, f"question_datafiles/{path}")
                    print(f"\nUnzipping {temp[-1]}\n\n\n")
                    f = zipfile.ZipFile(f"question_datafiles/{path}", 'r')
                    f.extractall(f"question_datafiles/{temp[-2]}/")
                except KeyboardInterrupt:
                    exit = True
                    break
                except:
                    print("Failed! Check your internet...\nIf internet is okay, then the file doesn't exist yet!\n\n")
            if exit:
                break
                print('\nExitting Download!\n\n\n')

    def on_closing(self):
        self.destroy()



    # subject func
    def phy_func(self):
        if self.phy.get():
            Setup.download_keys.append("Physics")
        else:
            Setup.download_keys.remove('Physics')


    def chem_func(self):
        if self.chem.get():
            Setup.download_keys.append("Chemistry")
        else:
            Setup.download_keys.remove('Chemistry')


    def bio_func(self):
        if self.bio.get():
            Setup.download_keys.append("Biology")
        else:
            Setup.download_keys.remove('Biology')

    def mb_func(self):
        if self.mb.get():
            Setup.download_keys.append("Maths-B")
        else:
            Setup.download_keys.remove('Maths-B')

    def ma_func(self):
        if self.ma.get():
            Setup.download_keys.append("Maths-A")
        else:
            Setup.download_keys.remove('Maths-A')

    def pm_func(self):
        if self.pm.get():
            Setup.download_keys.append("PureMaths")
        else:
            Setup.download_keys.remove('PureMaths')


    def phy1_func(self):
        if self.phy1.get():
            Setup.download_keys.append("Physics1")
        else:
            Setup.download_keys.remove('Physics1')


    def phy2_func(self):
        if self.phy2.get():
            Setup.download_keys.append("Physics2")
        else:
            Setup.download_keys.remove('Physics2')


    def chem1_func(self):
        if self.chem1.get():
            Setup.download_keys.append("Chemistry1")
        else:
            Setup.download_keys.remove('Chemistry1')


    def chem2_func(self):
        if self.chem2.get():
            Setup.download_keys.append("Chemistry2")
        else:
            Setup.download_keys.remove('Chemistry2')

if __name__ == "__main__":
    S = Setup()
    S.mainloop()
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
    HEIGHT = 600
    text_font_size =("Noto Sans CJK TC Black", -10)
    title_font =("Noto Sans CJK TC Black", -14)

    download_keys = []
    base_url = "https://github.com/IshraqueSarwar/question_datafiles/raw/main"
    sub_dict = {
    "Biology": [f"{base_url}/IGCSE/Biology_paper_1.pickle.zip", f"{base_url}/IGCSE/Biology_paper_2.pickle.zip"],
    "Chemistry": [f"{base_url}/IGCSE/Chemistry_paper_1.pickle.zip", f"{base_url}/IGCSE/Chemistry_paper_2.pickle.zip"],
    "Physics": [f"{base_url}/IGCSE/Physics_paper_1.pickle.zip", f"{base_url}/IGCSE/Physics_paper_2.pickle.zip"],
    "Maths-B": [f"{base_url}/IGCSE/Maths-B_paper_1.pickle.zip", f"{base_url}/IGCSE/Maths-B_paper_2.pickle.zip"],
    "Maths-A": [f"{base_url}/IGCSE/Maths-A_paper_1.pickle.zip", f"{base_url}/IGCSE/Maths-A_paper_2.pickle.zip"],
    "PureMaths": [f"{base_url}/IGCSE/PureMaths_paper_1.pickle.zip", f"{base_url}/IGCSE/PureMaths_paper_2.pickle.zip"],
    "Accounting":[f"{base_url}/IGCSE/Accounting_paper_1.pickle.zip",f"{base_url}/IGCSE/Accounting_paper_2.pickle.zip"],
    "Eco":[f"{base_url}/IGCSE/Economics_paper_1.pickle.zip",f"{base_url}/IGCSE/Economics_paper_2.pickle.zip"],
    "Busi":[f"{base_url}/IGCSE/Business_paper_1.pickle.zip",f"{base_url}/IGCSE/Business_paper_2.pickle.zip"],
    "Comp":[f"{base_url}/IGCSE/ComputerScience_paper_1.pickle.zip"],
    "ICT":[f"{base_url}/IGCSE/ICT_paper_1.pickle.zip"],

    "Physics1":[f"{base_url}/IAL/Physics_unit_1.pickle.zip",f"{base_url}/IAL/Physics_unit_2.pickle.zip",f"{base_url}/IAL/Physics_unit_3.pickle.zip"],
    "Physics2":[f"{base_url}/IAL/Physics_unit_4.pickle.zip",f"{base_url}/IAL/Physics_unit_5.pickle.zip",f"{base_url}/IAL/Physics_unit_6.pickle.zip"],
    "Chemistry1": [f"{base_url}/IAL/Chemistry_unit_1.pickle.zip",f"{base_url}/IAL/Chemistry_unit_2.pickle.zip",f"{base_url}/IAL/Chemistry_unit_3.pickle.zip"],
    "Chemistry2": [f"{base_url}/IAL/Chemistry_unit_4.pickle.zip",f"{base_url}/IAL/Chemistry_unit_5.pickle.zip",f"{base_url}/IAL/Chemistry_unit_6.pickle.zip"],
    "Biology1": [f"{base_url}/IAL/Biology_unit_1.pickle.zip",f"{base_url}/IAL/Biology_unit_2.pickle.zip",f"{base_url}/IAL/Biology_unit_3.pickle.zip"],
    "Biology2": [f"{base_url}/IAL/Biology_unit_4.pickle.zip",f"{base_url}/IAL/Biology_unit_5.pickle.zip",f"{base_url}/IAL/Biology_unit_6.pickle.zip"],
    "P1":[f"{base_url}/IAL/P1.pickle.zip"],
    "P2":[f"{base_url}/IAL/P2.pickle.zip"],
    "P3":[f"{base_url}/IAL/P3.pickle.zip"],
    "P4":[f"{base_url}/IAL/P4.pickle.zip"],
    "FP1":[f"{base_url}/IAL/FP1.pickle.zip"],
    "FP2":[f"{base_url}/IAL/FP2.pickle.zip"],
    "FP3":[f"{base_url}/IAL/FP3.pickle.zip"],
    "M1":[f"{base_url}/IAL/M1.pickle.zip"],
    "M2":[f"{base_url}/IAL/M2.pickle.zip"],
    "M3":[f"{base_url}/IAL/M3.pickle.zip"],
    "S1":[f"{base_url}/IAL/S1.pickle.zip"],
    "S2":[f"{base_url}/IAL/S2.pickle.zip"],
    "D1":[f"{base_url}/IAL/D1.pickle.zip"],
    }



    def __init__(self):
        super().__init__()

        self.title('setup')
        self.geometry(f"{Setup.WIDTH}x{Setup.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(False,False)

        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(20,weight = 1)

        self.labelTitle = customtkinter.CTkLabel(master = self, text = "Please select the subjects you want to download", text_font = Setup.title_font, justify = tkinter.CENTER)
        self.labelTitle.grid(column = 0,row = 0,pady = 4, padx=4, columnspan = 5)


        # IGCSE ########################################################
        self.labelIGCSE = customtkinter.CTkLabel(master = self, text = "IGCSE", text_font = Setup.title_font)
        self.labelIGCSE.grid(row = 1,column = 0,pady = 4, padx=4, columnspan = 2,sticky = 'nsew')
       
        ttk.Separator(self, orient=tkinter.VERTICAL).grid(column=2, row=2, rowspan= 20, sticky='ns')

        self.phy = customtkinter.CTkCheckBox(master = self,text = "Physics (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.phy_func)
        self.phy.grid(row = 2, column = 0, padx = 20, pady = 10, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/Physics_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/Physics_paper_2.pickle"):
            self.phy.select()
            Setup.download_keys.remove("Physics")
            self.phy.configure(state = tkinter.DISABLED)


        self.chem = customtkinter.CTkCheckBox(master = self,text = "Chemistry (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.chem_func)
        self.chem.grid(row = 3, column = 0,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/Chemistry_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/Chemistry_paper_2.pickle"):
            self.chem.select()
            Setup.download_keys.remove("Chemistry")
            self.chem.configure(state = tkinter.DISABLED)


        self.bio = customtkinter.CTkCheckBox(master = self,text = "Biology (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.bio_func)
        self.bio.grid(row = 4, column = 0,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/Biology_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/Biology_paper_2.pickle"):
            self.bio.select()
            Setup.download_keys.remove("Biology")
            self.bio.configure(state = tkinter.DISABLED)

        self.comp = customtkinter.CTkCheckBox(master = self,text = "Computer Science (1)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.comp_func)
        self.comp.grid(row = 5, column = 0,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/ComputerScience_paper_1.pickle"):
            self.comp.select()
            Setup.download_keys.remove("Comp")
            self.comp.configure(state = tkinter.DISABLED)

        

        self.eco = customtkinter.CTkCheckBox(master = self,text = "Economics (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.eco_func)
        self.eco.grid(row = 6, column = 0,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/Economics_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/Economics_paper_2.pickle"):
            self.eco.select()
            Setup.download_keys.remove("Eco")
            self.eco.configure(state = tkinter.DISABLED)


        self.busi = customtkinter.CTkCheckBox(master = self,text = "Business (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.busi_func)
        self.busi.grid(row = 7, column = 0,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/Business_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/Business_paper_2.pickle"):
            self.busi.select()
            Setup.download_keys.remove("Busi")
            self.busi.configure(state = tkinter.DISABLED)



        self.ict = customtkinter.CTkCheckBox(master = self,text = "ICT (1)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.ict_func)
        self.ict.grid(row = 8, column = 0,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/ICT_paper_1.pickle"):
            self.ict.select()
            Setup.download_keys.remove("ICT")
            self.ict.configure(state = tkinter.DISABLED)


        self.mb = customtkinter.CTkCheckBox(master = self,text = "Maths B (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.mb_func)
        self.mb.grid(row = 2, column = 1,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/Maths-B_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/Maths-B_paper_2.pickle"):
            self.mb.select()
            Setup.download_keys.remove("Maths-B")
            self.mb.configure(state = tkinter.DISABLED)



        self.ma = customtkinter.CTkCheckBox(master = self,text = "Maths A (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.ma_func)
        self.ma.grid(row = 3, column = 1,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/Maths-A_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/Maths-A_paper_2.pickle"):
            self.ma.select()
            Setup.download_keys.remove("Maths-A")
            self.ma.configure(state = tkinter.DISABLED)

        self.pm = customtkinter.CTkCheckBox(master = self,text = "Pure Maths (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.pm_func)
        self.pm.grid(row = 4, column = 1,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/PureMaths_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/PureMaths_paper_2.pickle"):
            self.pm.select()
            Setup.download_keys.remove("PureMaths")
            self.pm.configure(state = tkinter.DISABLED)


        self.acc = customtkinter.CTkCheckBox(master = self,text = "Accounting (1-2)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.acc_func)
        self.acc.grid(row = 5, column = 1,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IGCSE/Accounting_paper_1.pickle") and os.path.exists("question_datafiles/IGCSE/Accounting_paper_2.pickle"):
            self.acc.select()
            Setup.download_keys.remove("Accounting")
            self.acc.configure(state = tkinter.DISABLED)





        # IAL #####################################################################
        self.labelIAL = customtkinter.CTkLabel(master = self, text = "IAL", text_font = Setup.title_font, height = 20,width = 20)
        self.labelIAL.grid(row = 1,column = 3,pady = 4, padx=20, columnspan = 2, sticky = 'nsew')
        
        self.phy1 = customtkinter.CTkCheckBox(master = self,text = "Physics unit-(1-3)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.phy1_func)
        self.phy1.grid(row = 2, column = 4, padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Physics_unit_1.pickle") and os.path.exists("question_datafiles/IAL/Physics_unit_2.pickle") and os.path.exists("question_datafiles/IAL/Physics_unit_3.pickle"):
            self.phy1.select()
            Setup.download_keys.remove("Physics1")
            self.phy1.configure(state = tkinter.DISABLED)


        self.phy2 = customtkinter.CTkCheckBox(master = self,text = "Physics unit-(4-6)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.phy2_func)
        self.phy2.grid(row = 3, column = 4,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Physics_unit_4.pickle") and os.path.exists("question_datafiles/IAL/Physics_unit_5.pickle") and os.path.exists("question_datafiles/IAL/Physics_unit_6.pickle"):
            self.phy2.select()
            Setup.download_keys.remove("Physics2")
            self.phy2.configure(state = tkinter.DISABLED)

        self.chem1 = customtkinter.CTkCheckBox(master = self,text = "Chemistry unit-(1-3)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.chem1_func)
        self.chem1.grid(row = 4, column = 4,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Chemistry_unit_1.pickle") and os.path.exists("question_datafiles/IAL/Chemistry_unit_2.pickle") and os.path.exists("question_datafiles/IAL/Chemistry_unit_3.pickle"):
            self.chem1.select()
            Setup.download_keys.remove("Chemistry1")
            self.chem1.configure(state = tkinter.DISABLED)


        self.chem2 = customtkinter.CTkCheckBox(master = self,text = "Chemistry unit-(4-6)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.chem2_func)
        self.chem2.grid(row = 5, column = 4,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Chemistry_unit_4.pickle") and os.path.exists("question_datafiles/IAL/Chemistry_unit_5.pickle") and os.path.exists("question_datafiles/IAL/Chemistry_unit_6.pickle"):
            self.chem2.select()
            Setup.download_keys.remove("Chemistry2")
            self.chem2.configure(state = tkinter.DISABLED)

        self.bio1 = customtkinter.CTkCheckBox(master = self,text = "Biology unit-(1-3)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.bio1_func)
        self.bio1.grid(row = 6, column = 4,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Biology_unit_1.pickle") and os.path.exists("question_datafiles/IAL/Biology_unit_2.pickle") and os.path.exists("question_datafiles/IAL/Biology_unit_3.pickle"):
            self.bio1.select()
            Setup.download_keys.remove("Biology1")
            self.bio1.configure(state = tkinter.DISABLED)


        self.bio2 = customtkinter.CTkCheckBox(master = self,text = "Biology unit-(4-6)",text_font = Setup.text_font_size, height = 20,width = 20, command = self.bio2_func)
        self.bio2.grid(row = 7, column = 4,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/Biology_unit_4.pickle") and os.path.exists("question_datafiles/IAL/Biology_unit_5.pickle") and os.path.exists("question_datafiles/IAL/Biology_unit_6.pickle"):
            self.bio2.select()
            Setup.download_keys.remove("Biology2")
            self.bio2.configure(state = tkinter.DISABLED)



        self.p1 = customtkinter.CTkCheckBox(master = self,text = "PureMaths unit-1",text_font = Setup.text_font_size, height = 20,width = 20, command = self.p1_func)
        self.p1.grid(row = 2, column = 3, padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/P1.pickle"):
            self.p1.select()
            Setup.download_keys.remove("P1")
            self.p1.configure(state = tkinter.DISABLED)


        self.p2 = customtkinter.CTkCheckBox(master = self,text = "PureMaths unit-2",text_font = Setup.text_font_size, height = 20,width = 20, command = self.p2_func)
        self.p2.grid(row = 3, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/P2.pickle"):
            self.p2.select()
            Setup.download_keys.remove("P2")
            self.p2.configure(state = tkinter.DISABLED)

        self.p3 = customtkinter.CTkCheckBox(master = self,text = "PureMaths unit-3",text_font = Setup.text_font_size, height = 20,width = 20, command = self.p3_func)
        self.p3.grid(row = 4, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/P3.pickle"):
            self.p3.select()
            Setup.download_keys.remove("P3")
            self.p3.configure(state = tkinter.DISABLED)

        self.p4 = customtkinter.CTkCheckBox(master = self,text = "PureMaths unit-4",text_font = Setup.text_font_size, height = 20,width = 20, command = self.p4_func)
        self.p4.grid(row = 5, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/P4.pickle"):
            self.p4.select()
            Setup.download_keys.remove("P4")
            self.p4.configure(state = tkinter.DISABLED)

        self.fp1 = customtkinter.CTkCheckBox(master = self,text = "F.PureMaths unit-1",text_font = Setup.text_font_size, height = 20,width = 20, command = self.fp1_func)
        self.fp1.grid(row = 6, column = 3, padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/FP1.pickle"):
            self.fp1.select()
            Setup.download_keys.remove("FP1")
            self.fp1.configure(state = tkinter.DISABLED)


        self.fp2 = customtkinter.CTkCheckBox(master = self,text = "F.PureMaths unit-2",text_font = Setup.text_font_size, height = 20,width = 20, command = self.fp2_func)
        self.fp2.grid(row = 7, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/FP2.pickle"):
            self.fp2.select()
            Setup.download_keys.remove("FP2")
            self.fp2.configure(state = tkinter.DISABLED)

        self.fp3 = customtkinter.CTkCheckBox(master = self,text = "F.PureMaths unit-3",text_font = Setup.text_font_size, height = 20,width = 20, command = self.fp3_func)
        self.fp3.grid(row = 8, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/FP3.pickle"):
            self.fp3.select()
            Setup.download_keys.remove("FP3")
            self.fp3.configure(state = tkinter.DISABLED)


        self.m1 = customtkinter.CTkCheckBox(master = self,text = "Mechanics unit-1",text_font = Setup.text_font_size, height = 20,width = 20, command = self.m1_func)
        self.m1.grid(row = 9, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/M1.pickle"):
            self.m1.select()
            Setup.download_keys.remove("M1")
            self.m1.configure(state = tkinter.DISABLED)
        
        self.m2 = customtkinter.CTkCheckBox(master = self,text = "Mechanics unit-2",text_font = Setup.text_font_size, height = 20,width = 20, command = self.m2_func)
        self.m2.grid(row = 10, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/M2.pickle"):
            self.m2.select()
            Setup.download_keys.remove("M2")
            self.m2.configure(state = tkinter.DISABLED)


        self.m3 = customtkinter.CTkCheckBox(master = self,text = "Mechanics unit-3",text_font = Setup.text_font_size, height = 20,width = 20, command = self.m3_func)
        self.m3.grid(row = 11, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/M3.pickle"):
            self.m3.select()
            Setup.download_keys.remove("M3")
            self.m3.configure(state = tkinter.DISABLED)


        self.s1 = customtkinter.CTkCheckBox(master = self,text = "Statistics unit-1",text_font = Setup.text_font_size, height = 20,width = 20, command = self.s1_func)
        self.s1.grid(row = 12, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/S1.pickle"):
            self.s1.select()
            Setup.download_keys.remove("S1")
            self.s1.configure(state = tkinter.DISABLED)



        self.s2 = customtkinter.CTkCheckBox(master = self,text = "Statistics unit-2",text_font = Setup.text_font_size, height = 20,width = 20, command = self.s2_func)
        self.s2.grid(row = 13, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/S2.pickle"):
            self.s2.select()
            Setup.download_keys.remove("S2")
            self.s2.configure(state = tkinter.DISABLED)


        self.d1 = customtkinter.CTkCheckBox(master = self,text = "Decision Maths unit-1",text_font = Setup.text_font_size, height = 20,width = 20, command = self.d1_func)
        self.d1.grid(row = 14, column = 3,padx = 20, pady = 4, sticky = 'w')
        if os.path.exists("question_datafiles/IAL/D1.pickle"):
            self.d1.select()
            Setup.download_keys.remove("D1")
            self.d1.configure(state = tkinter.DISABLED)



        # Download button
        self.download_button = customtkinter.CTkButton(master = self,
                                                text = "Download",
                                                text_font = Setup.title_font,
                                                command = self.download)
        self.download_button.grid(row = 19, column = 4, pady = 10, padx=20, rowspan = 2, sticky = 's')

        self.exit = customtkinter.CTkButton(master = self,
                                                text = "Exit",
                                                text_font = Setup.title_font,
                                                command = self.on_closing, 
                                                fg_color = '#f75348',
                                                hover_color= '#f58078')
        self.exit.grid(row = 19, column = 0, pady = 10, padx=20, rowspan = 2, sticky = 's')



    def download(self):
        exit = False
        print("Starting Download! This may take a while...")
        for subject in Setup.download_keys:
            for i in range(len(Setup.sub_dict[subject])):
                link = Setup.sub_dict[subject][i]
                temp = link.split('/')
                path = temp[-2]+'/'+temp[-1]
                print(path)
                print(f"Downloading {temp[-1]}")
                try:
                    wget.download(link, f"question_datafiles/{path}")
                    print(f"\nUnzipping {temp[-1]}\n\n\n")
                    f = zipfile.ZipFile(f"question_datafiles/{path}", 'r')
                    f.extractall(f"question_datafiles/{temp[-2]}/")
                    os.remove(f"question_datafiles/{path}")
                except KeyboardInterrupt:
                    exit = True
                    break
                except:
                    print("Failed! Check your internet...\nIf internet is okay, then the file doesn't exist yet!\n\n")
            if exit:
                break
                print('\nExitting Download!\n\n\n')


        print("##### Download Completed #####")

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

    def acc_func(self):
        if self.acc.get():
            Setup.download_keys.append("Accounting")
        else:
            Setup.download_keys.remove('Accounting')


    def eco_func(self):
        if self.eco.get():
            Setup.download_keys.append("Eco")
        else:
            Setup.download_keys.remove('Eco')


    def busi_func(self):
        if self.busi.get():
            Setup.download_keys.append("Busi")
        else:
            Setup.download_keys.remove("Busi")

    def comp_func(self):
        if self.comp.get():
            Setup.download_keys.append("Comp")
        else:
            Setup.download_keys.remove("Comp")
    

    def ict_func(self):
        if self.ict.get():
            Setup.download_keys.append("ICT")
        else:
            Setup.download_keys.remove("ICT")






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


    def bio1_func(self):
        if self.bio1.get():
            Setup.download_keys.append("Biology1")
        else:
            Setup.download_keys.remove('Biology1')


    def bio2_func(self):
        if self.bio2.get():
            Setup.download_keys.append("Biology2")
        else:
            Setup.download_keys.remove('Biology2')


    def p1_func(self):
        if self.p1.get():
            Setup.download_keys.append("P1")
        else:
            Setup.download_keys.remove("P1")


    def p2_func(self):
        if self.p2.get():
            Setup.download_keys.append("P2")
        else:
            Setup.download_keys.remove("P2")



    def p3_func(self):
        if self.p3.get():
            Setup.download_keys.append("P3")
        else:
            Setup.download_keys.remove("P3")




    def p4_func(self):
        if self.p4.get():
            Setup.download_keys.append("P4")
        else:
            Setup.download_keys.remove("P4")


    def fp1_func(self):
        if self.fp1.get():
            Setup.download_keys.append("FP1")
        else:
            Setup.download_keys.remove("FP1")


    def fp2_func(self):
        if self.fp2.get():
            Setup.download_keys.append("FP2")
        else:
            Setup.download_keys.remove("FP2")



    def fp3_func(self):
        if self.fp3.get():
            Setup.download_keys.append("FP3")
        else:
            Setup.download_keys.remove("FP3")

    def m1_func(self):
        if self.m1.get():
            Setup.download_keys.append("M1")
        else:
            Setup.download_keys.remove("M1")


    def m2_func(self):
        if self.m2.get():
            Setup.download_keys.append("M2")
        else:
            Setup.download_keys.remove("M2")



    def m3_func(self):
        if self.m3.get():
            Setup.download_keys.append("M3")
        else:
            Setup.download_keys.remove("M3")


    def s1_func(self):
        if self.s1.get():
            Setup.download_keys.append("S1")
        else:
            Setup.download_keys.remove("S1")


    def s2_func(self):
        if self.s2.get():
            Setup.download_keys.append("S2")
        else:
            Setup.download_keys.remove("S2")


    def d1_func(self):
        if self.d1.get():
            Setup.download_keys.append("D1")
        else:
            Setup.download_keys.remove("D1")


if __name__ == "__main__":
    S = Setup()
    S.mainloop()
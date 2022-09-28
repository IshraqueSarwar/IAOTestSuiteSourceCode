import tkinter
import tkinter.messagebox
import customtkinter
import os
import pickle
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import utils
import cv2
import time
import multiprocessing


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")
class App(customtkinter.CTk):
	WIDTH = 780
	HEIGHT = 520

	# some fonts = Purisa,Noto Sans CJK TC Black
	App_text_font_size =("Noto Sans CJK TC Black", -14)

	GEN_BUT_NAME = 'Generate'

	# Backend
	combo_save_file = "datsavfiles/combinations.pickle"
	save_data_file = "datsavfiles/dat.pickle"


	qualification_path = 'IGCSE'
	# qs_files = os.listdir(f"question_datafiles/{qualification_path}/")
	# sub_names = [i.replace('.pickle','').replace('_',' ') for i in qs_files]


	sub_names = []
	qs_files = os.listdir(f"question_datafiles/{qualification_path}/")
	for i in qs_files:
		name,ext = os.path.splitext(i)
		if ext=='.pickle':
			sub_names.append(i.replace('.pickle','').replace('_',' '))
	sub_names = sorted(sub_names)
	sub_names.insert(0, 'None')


	if len(sub_names):
		sub_key = sub_names[0].replace(' ', '_')

	output_path = None
	front_page_path = None
	# output_path, front page path
	if os.path.exists(save_data_file):
		save_data = pickle.load(open(save_data_file, 'rb'))
		if save_data[0] is not None:
			output_path = save_data[0]
		if save_data[1] is not None:
			front_page_path = save_data[1]



	qs_data = None
	saved_combinations_file = None


	# Remove any file in /Lab

	def __init__(self):
		super().__init__()

		self.text = ''

		self.title("IAO Test-Suite")
		self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
		self.maxsize(App.WIDTH+70, App.HEIGHT)
		self.minsize(App.WIDTH, App.HEIGHT)
		self.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.resizable(True,False)

		# ========== Create two frames ============
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0,weight = 1)

		self.frame_left = customtkinter.CTkFrame(master = self,
													width = 150,
													corner_radius = 0)
		self.frame_left.grid(row = 0, column = 0, sticky = 'nswe', rowspan = 2)

		self.frame_right = customtkinter.CTkFrame(master = self, corner_radius = 7)
		self.frame_right.grid(row = 0, column = 1, sticky = 'nswe',padx = 10, pady = (10,0))
		
		self.cright= customtkinter.CTkLabel(master = self,text = "© Ishraque sarwar 2022, All rights reserved.", text_font = ("Noto Sans CJK TC Black", -10))
		self.cright.grid(row = 1, column =1, sticky='sw', padx = 10, pady = 0)

		# ========== Frame Left ===================
		self.frame_left.grid_rowconfigure(0, minsize = 10)
		self.frame_left.grid_rowconfigure(5, weight = 1)
		self.frame_left.grid_rowconfigure(8, minsize = 20)
		self.frame_left.grid_rowconfigure(10, minsize = 10)

		self.AppName = customtkinter.CTkLabel(self.frame_left,
												text = "IAO TestSuite",
												text_font=("Noto Sans CJK TC Black", -20),)
		self.AppName.grid(row = 1, column = 0, pady = 8, padx=8)



		self.quali_label = customtkinter.CTkLabel(master = self.frame_left, text = 'Select Qualification:')
		self.quali_label.grid(row = 2, column = 0, pady=10, padx =20)


		self.quali_options = customtkinter.CTkOptionMenu(master = self.frame_left,
															values= ['IGCSE', 'IAL'],
															command = self.change_qualification,
															fg_color = '#4d84d6',
															button_color = '#1561d4',
															button_hover_color = '#3a75cf')
		self.quali_options.grid(row = 3, column = 0, pady=5, padx = 20)



		self.reset_all_button = customtkinter.CTkButton(master = self.frame_left,
														text = "Reset Progress",
														text_font = App.App_text_font_size,
														command = self.reset_all_combination_data,
														fg_color = '#1561d4',
														hover_color = '#3a75cf')

		self.reset_all_button.grid(row= 4, column=0, pady = 5, padx = 20)


		self.appearance_label = customtkinter.CTkLabel(master = self.frame_left,
														text = 'Appearance:')
		self.appearance_label.grid(row = 7, column = 0, pady=10, padx = 20)

		self.appearance = customtkinter.CTkOptionMenu(master = self.frame_left,
													values = ["Dark", "Light", "System"],
													command = self.change_appearance_mode,
													fg_color = '#4d84d6',
													button_color = '#1561d4',
													button_hover_color = '#3a75cf')
		self.appearance.grid(row = 8, column = 0, pady = 5, padx = 20, sticky = 'w')

		self.credit_button = customtkinter.CTkButton(master=self.frame_left,
													text = "Credit",
													text_font = App.App_text_font_size,
													command = self.show_credit)

		self.credit_button.grid(row = 9, column=0, pady=5, padx=20)

		self.button_exit = customtkinter.CTkButton(master = self.frame_left,
													text = "Exit",
													text_font = App.App_text_font_size,
													command = self.on_closing,
													fg_color = '#f75348',
													hover_color= '#f58078')#('#f58078','#f75348')
		self.button_exit.grid(row = 10, column=0, pady=10,padx=20)




		# ============== frame right ===============
		self.frame_right.rowconfigure((0,1,2,3), weight = 1)
		self.frame_right.rowconfigure(9, weight = 10)
		self.frame_right.columnconfigure((0,1), weight = 1)
		self.frame_right.columnconfigure(2, weight=0)

		self.frame_right.pack_propagate(0)

		self.info_board = customtkinter.CTkFrame(master = self.frame_right)
		self.info_board.grid(row=0, column=0, columnspan = 3, rowspan = 4, pady = 10, padx = 10, sticky = 'nsew')
		# ============= info board =================
		self.info_board.rowconfigure(2,weight=1)
		self.info_board.columnconfigure(0, weight=1)

		self.greetings= ("Hiya candidate! Welcome to IAO Test-Suite!\n"+
						'You can select between Edexcel IGCSE and IAL on your\n'+
						'Left and select various subjects from those qualifications.\n'+
						'But first let the program know where to\n'+
						'save your paper and mark scheme below.')
		self.info_label = customtkinter.CTkLabel(master = self.info_board,
													text =self.greetings,
													height = 180,
													corner_radius = 6,
													fg_color = ('white',"gray38"),
													text_font = ("Purisa", -14),
													justify = tkinter.CENTER)
		self.info_label.grid(row = 0, column =0, sticky = 'nwe', pady=10, padx=10)




		# Add output location path selection button
		self.output_path = tkinter.StringVar()
		if App.output_path is not None:
			self.output_path.set(App.output_path)
		else:
			self.output_path.set("Browse output path")
		self.browse_path_button = customtkinter.CTkButton(master = self.info_board,text = self.output_path.get(),
															text_font = App.App_text_font_size, 
															command = self.browse_button,
															fg_color = '#1561d4',
															hover_color = '#3a75cf')
		self.browse_path_button.grid(row = 1, column = 0, pady=5, padx=10)




		# Progress bar
		self.progressbar = customtkinter.CTkProgressBar(master = self.info_board)
		self.progressbar.grid(row = 2, column = 0, sticky = 'ew', pady=10, padx=10)


		# lower left part
		self.front_page_header = customtkinter.CTkLabel(master = self.frame_right,
															text = "Front page (if any) path:",
															text_font = App.App_text_font_size,)
		self.front_page_header.grid(row = 4, column = 0,padx=10, pady= 1)

		self.front_page_path = tkinter.StringVar()
		if App.front_page_path is not None:
			self.front_page_path.set(App.front_page_path)
		else:
			self.front_page_path.set("Browse Path")
		self.front_page_path_label = customtkinter.CTkEntry(master = self.frame_right,
															placeholder_text = self.front_page_path.get(),
															width = 300,
															text_font = App.App_text_font_size)

		self.front_page_path_label.grid(row =5, column = 0, sticky = 'w',padx = 10, pady = 10)
		self.front_page_path_label.configure(state = "disabled")
		
		self.front_page_path_button = customtkinter.CTkButton(master = self.frame_right,
																text = "Browse",
																text_font = App.App_text_font_size,
																command = self.get_front_page_path,
																fg_color = '#1561d4',
																hover_color = '#3a75cf')
		self.front_page_path_button.grid(row = 5, column = 1, padx = 10, pady = 1)


		self.subject_label = customtkinter.CTkLabel(master = self.frame_right,
													text = 'Subject:',
													text_font = App.App_text_font_size)
		self.subject_label.grid(row = 6,column=0, pady = 10, padx = 10 )
		self.subject_options = customtkinter.CTkOptionMenu(master = self.frame_right,
															values = App.sub_names,
															command = self.change_subject_choice,
															width = 300,
															fg_color = '#4d84d6',
															button_color = '#1561d4',
															button_hover_color = '#3a75cf',)
															# dropdown_text_font = ("Noto Sans CJK", -12))
		self.subject_options.grid(row = 7, column = 0, pady = 2, padx = 10,)
		

		self.reset_button = customtkinter.CTkButton(master = self.frame_right,
													text = 'Reset',
													text_font =App.App_text_font_size,
													command  =self.reset_button,
													fg_color = '#f75348',
													hover_color= '#f58078')
		self.reset_button.grid(row = 7, column = 1, pady = 2, padx = 10)

		# right part
		self.test_type_radio_var = tkinter.IntVar(value = 0)
		self.test_type_label = customtkinter.CTkLabel(master = self.frame_right,
														text = 'Type to test: ',
														text_font = App.App_text_font_size)
		self.test_type_label.grid(row = 4, column = 2, pady = 5, padx = 10)

		self.test_option_1 = customtkinter.CTkRadioButton(master = self.frame_right,
															variable = self.test_type_radio_var,
															value = 1,
															text = "Full test",
															text_font = App.App_text_font_size,
															fg_color = '#1561d4',
															hover_color = '#3a75cf')
		self.test_option_1.grid(row = 5, column = 2, pady = 5, padx = 10)
		self.test_option_2 = customtkinter.CTkRadioButton(master = self.frame_right,
															variable = self.test_type_radio_var,
															value = 0,
															text = "MCQ test",
															text_font = App.App_text_font_size,
															fg_color = '#1561d4',
															hover_color = '#3a75cf')
		self.test_option_2.grid(row = 6, column = 2, pady = 5, padx = 10)
		
		self.generate_button = customtkinter.CTkButton(master = self.frame_right,
												text = "Generate",
												text_font = App.App_text_font_size,
												command = self.generate)
		self.generate_button.grid(row = 7, column = 2, pady = 1, padx=10, rowspan = 2)

		# select default test type: Full test
		self.test_option_1.select()


			
	def resave_saved_combinations_file(self):
		if App.saved_combinations_file is not None:
			pickle.dump(App.saved_combinations_file, open(App.combo_save_file,'wb'))


	def update_dat_file(self):
		if App.output_path is None:
			output = 'Browse output path' 
		else:
			output = str(App.output_path)
		if App.front_page_path is None:
			front = "Browse path"
		else:	
			front = str(App.front_page_path)
		pickle.dump([output, front], open(App.save_data_file, 'wb'))


	def update_info_label(self):
		self.info_label.configure(text = self.text, justify = tkinter.LEFT)


# =========================UTILS FOR GENERATION===============================
	
	def retrieve_or_generate_combinations(self,combo_save_file,qs_data):
		if not os.path.exists(combo_save_file):
			subject_combinations = {f"{App.sub_key}": utils.get_combination(qs_data)}
			current_combo_index = {f"{App.sub_key}":[0,0,0]}
			print("saving combinations for later use...")
			pickle.dump([subject_combinations, current_combo_index], open(combo_save_file,'wb'))
		else:
			print("\nLoading...")
			# NOTE: saved_combinations_file = [subject_combination_dictionary, current_combo_index_dictionary]
			# 		subject_combination_dictionary = {subject_name: [[qs_combo_lists],[mcq_combo_lists]], ...}
			# 		current_combo_index_dictionary = {subject_name: [qs_combo_index, mcq_combo_index]}
			saved_combinations_file = pickle.load(open(combo_save_file,'rb'))
			subject_combinations = saved_combinations_file[0]
			current_combo_index = saved_combinations_file[1]


			if App.sub_key in subject_combinations.keys():
				print("The subject combination is in the file")
			else:
				print("Not in file, thus generating combinations")
				subject_combinations[App.sub_key] = utils.get_combination(qs_data)
				current_combo_index[App.sub_key] = [0,0,0]
				print("Saving combinations for later use...")
				pickle.dump([subject_combinations, current_combo_index], open(combo_save_file,'wb'))

		return [subject_combinations[App.sub_key], current_combo_index[App.sub_key]]
			
			





	def reverse_sort_img_files(self,img_files):
	    files = []
	    path_origin = ''
	    for i in img_files:
	        split_list = i.split('/')
	        files.append(int( split_list[-1].replace(".jpeg", '') ))
	        
	        if path_origin == '':
	            for x in split_list[:-1]:
	                path_origin+=x+'/'
	    

	    files = sorted(files, reverse = True)
	    # del split_list

	    img_files = [path_origin+str(i)+".jpeg" for i in files]

	    return img_files


	def create_pages(self,combination_ids, id_to_img, id_used,v_lim = 1490, h_fixed = 1054):
		pages = []
		qs_num = 1
		image = None
		for id_ in combination_ids:
			mark = id_used[id_][-1]
			for i in range(len(id_to_img[id_])):
				img = id_to_img[id_][i]
				img = cv2.cvtColor(cv2.resize(img, (h_fixed, img.shape[0])), cv2.COLOR_GRAY2RGB)
				if i == 0:
					# Adding number and white bg to the number only used if first page of id
					cv2.rectangle(img, (0,0), (45,80), color = (255,255,255),thickness = -1)
					cv2.putText(img,f'{qs_num}.',(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,0,2,2)
					qs_num+=1

				if i == len(id_to_img[id_])-1:
					# adding marks of the qs and white bg for mark, only used of last page of id
					cv2.rectangle(img, (0, img.shape[0]-25), (img.shape[1], img.shape[0]), color = (255,255,255),thickness = -1)
					if int(mark)>1:
						mt = 'marks'
					else:
						mt = 'mark'
					sentence = f"(Total for question {qs_num-1} is {mark} {mt})"
					cv2.putText(img, sentence, (img.shape[1]-600,img.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 1,0,2,2)


				if image is None:
					image = img
				elif image.shape[0]+img.shape[0]<=v_lim:
					image = np.concatenate((image, img), axis = 0)
				else:
					image = cv2.copyMakeBorder(image, 0, abs(v_lim-image.shape[0]), 0, 0, cv2.BORDER_CONSTANT, None, [255,255,255])
					pages.append(image)
					image = img

			image = cv2.copyMakeBorder(image, 0, abs(v_lim-image.shape[0]), 0, 0, cv2.BORDER_CONSTANT, None, [255,255,255])
			pages.append(image)
			image = None

		for i in range(len(pages)):
			cv2.imwrite(f'Lab/{i}.jpeg', pages[i])

		files = reverse_sort_img_files(glob.glob("Lab/*.jpeg"))[::-1]
		with open('test.pdf','wb')as f:
			f.write(img2pdf.convert(files))
		for file in tqdm(files):
			os.remove(file)
		
	
# ======================= UTILS FOR GENERATION======================================

	def resave_saved_combinations_file(self):
		if App.saved_combinations_file is not None:
			pickle.dump(App.saved_combinations_file, open(App.combo_save_file,'wb'))


	

	def change_gen_button(self, ):
		self.generate_button.configure(text = App.GEN_BUT_NAME)
		self.generate_button.after(10,self.change_gen_button)


	def generate(self):
		self.progressbar.set(0)
		if App.sub_key !="None":
			self.GEN_BUT_NAME = "Working..."
			t1 = multiprocessing.Process(target = self.change_gen_button)
			t1.start()
			t1.join()
			qs_data = pickle.load(open(f"question_datafiles/{App.qualification_path}/{App.sub_key}.pickle" ,'rb'))


			combinations, combo_index =  self.retrieve_or_generate_combinations(App.combo_save_file,qs_data)
			self.info_label.configure(text = "Generation complete!",
										justify = tkinter.CENTER)
			

			if combinations[2] is None and not self.test_type_radio_var.get():
				self.info_label.configure(text=f"Generation complete!\n No seperate MCQ test option\n for {App.sub_key.replace('_',' ')}")

			#[qs_score_to_id, qs_id_to_img, qs_id_used,mcq_score_to_id, mcq_id_to_img, mcq_id_used, num_papers,ms_id_to_img, qs_target_marks, mcq_target_marks]

			total = len(combinations[0])
			if not self.test_type_radio_var.get():
				# only mcq test
				paper_num = combo_index[2]+1

				try:
					
					if combo_index[2]+1<=total:
						mcq_combination_ids = combinations[2][combo_index[2]]
						combo_index[2]+=1
					else:
						mcq_combination_ids = combinations[2][combo_index[2]-1]

				except:
					mcq_combination_ids = None
				qs_combination_ids= None
			else:
				# Full test
				paper_num = combo_index[0]+1

				try:
					if combo_index[1]+1<=total:
						mcq_combination_ids = combinations[1][combo_index[1]]
						combo_index[1]+=1
					else:
						mcq_combination_ids = combinations[1][combo_index[1]-1]
				except:
					mcq_combination_ids = None
				if combo_index[0]+1<=total:

					qs_combination_ids = combinations[0][combo_index[0]]
					combo_index[0]+=1
				else:
					qs_combination_ids = combinations[0][combo_index[0]-1]


			print("paper number:", paper_num)
			qs_id_to_img = qs_data[1]
			qs_id_used = qs_data[2]
			mcq_id_to_img= qs_data[4]
			mcq_id_used = qs_data[5]
			ms_id_to_img = qs_data[-3]


			# Front page
			front_page = cv2.imread('datsavfiles/front_page.jpeg')
			# Qualification
			cv2.putText(front_page,f'{App.qualification_path}',(250,340),cv2.FONT_HERSHEY_SIMPLEX,2,0,6,2)
			# Subject name
			cv2.putText(front_page,f"{App.sub_key.replace('_',' ')}",(250,480),cv2.FONT_HERSHEY_SIMPLEX,2,0,6,2)
			# Mark
			if self.test_type_radio_var.get():
				mark = qs_data[-1]+qs_data[-2]
			else:
				mark = qs_data[-1]
			cv2.putText(front_page,f'{mark}',(540,1060),cv2.FONT_HERSHEY_SIMPLEX,1,0,2,2)
			front_page = cv2.resize(front_page,(1054, 1490))

			if self.output_path.get()=='Browse output path' or self.output_path.get() is None:
				output= '..'
			else:
				output = self.output_path.get()
			utils.create_pages(mcq_combination_ids, mcq_id_to_img, mcq_id_used ,qs_combination_ids, qs_id_to_img, qs_id_used, ms_id_to_img,front_page,full_test = self.test_type_radio_var.get() ,v_lim = 1490, h_fixed = 1054, output_qs_file = f"{output}/{App.sub_key.replace('_',' ')}_test_{paper_num}.pdf",output_ms_file = f"{output}/{App.sub_key.replace('_',' ')}_ms_test_{paper_num}.pdf")



			# UPDATE THE COMBO index and save the saved combination file depending on the type of test.
			if App.saved_combinations_file is None:
				App.saved_combinations_file = pickle.load(open(App.combo_save_file,'rb'))

			App.saved_combinations_file[1][App.sub_key] = combo_index
			self.resave_saved_combinations_file()
			del qs_data
		self.progressbar.set(1)
		self.GEN_BUT_NAME = "Generate"
		# t2 = multiprocessing.Process(target = self.change_gen_button)
		# t2.start()
		# t2.join()	
		self.generate_button.configure(state = 'normal')


	def update_qs_files(self):
		App.sub_names = []
		App.qs_files = os.listdir(f"question_datafiles/{App.qualification_path}/")
		for i in App.qs_files:
			name,ext = os.path.splitext(i)
			if ext=='.pickle':
				App.sub_names.append(i.replace('.pickle','').replace('_',' '))
		App.sub_names = sorted(App.sub_names)
		App.sub_names.insert(0, 'None')


		self.subject_options.configure(values = App.sub_names)
		self.subject_options.set("None")
		App.sub_key = 'None'
		

	def change_qualification(self, quali):
		App.qualification_path = quali
		self.update_qs_files()
		print(App.sub_key)

	def reset_all_combination_data(self):
		reset = messagebox.askokcancel("Reset", "Are you sure you want to reset all progress?")
		if reset:
			try:
				os.remove(App.combo_save_file)
				self.info_label.configure(text = 'removed All the progress')
			except:
				self.info_label.configure(text = "all progresses have already\n been removed")

		self.saved_combinations_file = None

	def change_appearance_mode(self, new_appearance_mode):
		customtkinter.set_appearance_mode(new_appearance_mode)

	def show_credit(self):
		self.credit_text = ('This software is created by Ishraque sarwar\n'+
							'and is under MIT license.\n'+
							 "Instagram: @ishraque_sarwar\n"+
							 "Facebook: Isharaque sarwar")
		self.info_label.configure(text = self.credit_text, justify = tkinter.CENTER)
		print("Created by Ishraque Sarwar")


	def change_subject_choice(self, new_subject):
		if new_subject!='None':
			self.text = ''
			App.sub_key = new_subject.replace(' ','_')
			# NOTE: saved_combinations_file = [subject_combination_dictionary, current_combo_index_dictionary]
			# 		subject_combination_dictionary = {subject_name: [[qs_combo_lists],[mcq_combo_lists]], ...}
			# 		current_combo_index_dictionary = {subject_name: [qs_combo_index, mcq_combo_index]}
			if App.saved_combinations_file is None:
				if os.path.exists(App.combo_save_file):
					App.saved_combinations_file = pickle.load(open(App.combo_save_file,'rb'))
					subject_combinations = App.saved_combinations_file[0]
					current_combo_index = App.saved_combinations_file[1]


					if App.sub_key in subject_combinations.keys():
						total = len(subject_combinations[App.sub_key][0])
						done = current_combo_index[App.sub_key][0]

						
						if subject_combinations[App.sub_key][2]:
							total_mcq = len(subject_combinations[App.sub_key][2])
							done_mcq = current_combo_index[App.sub_key][2]
						else:
							total_mcq = 0
							done_mcq = 0

						self.text+=(f"### {new_subject} ###\n"+
									f"Total tests: {total}\n"+
									f"Tests completed: {done}\n"+
									f"Tests remaining: {total-done}\n"+
									f"MCQ tests done: {done_mcq}\n"+
									f"MCQ tests remain: {total_mcq- done_mcq}\n")

						self.update_info_label()

						# ============ progress bar update ============
						pct = done/total
						self.progressbar.set(pct)

						if subject_combinations[App.sub_key][1] is None:
							self.test_option_2.configure(state = "disabled")
						else:
							self.test_option_2.configure(state = 'normal')


					else:
						App.saved_combinations_file = None
						self.text+=f'{new_subject} is absent in combination file...\nNeed to Generate.\n'
						self.update_info_label()
						# self.test_option_2.configure(state = 'disabled')
					self.text = ''
					print(App.sub_key)


				else:
					self.info_label.configure(text = 'Combination needs to be generated...\n'+
														'This may take a while...\n'+
														'wait for generation to complete.\n',
												justify = tkinter.CENTER)
			else:
				subject_combinations = App.saved_combinations_file[0]
				current_combo_index = App.saved_combinations_file[1]



				if App.sub_key in subject_combinations.keys():
					total = len(subject_combinations[App.sub_key][0])
					done = current_combo_index[App.sub_key][0]

					if subject_combinations[App.sub_key][2]:
						total_mcq = len(subject_combinations[App.sub_key][2])
						done_mcq = current_combo_index[App.sub_key][2]
					else:
						total_mcq = 0
						done_mcq = 0

					self.text+=(f"### {new_subject} ###\n"+
								f"Total tests: {total}\n"+
								f"Tests completed: {done}\n"+
								f"Tests remaining: {total-done}\n"+
								f"MCQ tests done: {done_mcq}\n"+
								f"MCQ tests remain: {total_mcq- done_mcq}\n")


					self.update_info_label()

					# ============ progress bar update ============
					pct = done/total
					self.progressbar.set(pct)

					if subject_combinations[App.sub_key][1] is None:
						self.test_option_2.configure(state = "disabled")
					else:
						self.test_option_2.configure(state = 'normal')


				else:
					App.saved_combinations_file = None
					self.text+=f'{new_subject} is absent in combination file...\nNeed to Generate.\n'
					self.update_info_label()
					# self.test_option_2.configure('disabled')
				self.text = ''
				print(App.sub_key)

		else:
			App.sub_key = 'None'
			self.info_label.configure(text = "No subject is selected.")
			

			



	def get_front_page_path(self):
		filename = filedialog.askopenfilename(filetypes=[('Photo','.jpeg .jpg'), ('Pdf', '.pdf')])
		self.front_page_path.set(filename)

		if self.front_page_path.get()!='' :
			self.front_page_path_label.configure(state = 'normal')
			self.front_page_path_label.configure(placeholder_text = self.front_page_path.get())
			self.front_page_path_label.configure(state = 'disabled')
			App.front_page_path = self.front_page_path.get()
			self.update_dat_file()

	def browse_button(self):
	    filename = filedialog.askdirectory()
	    self.output_path.set(filename)
	    if self.output_path.get() != '':
	    	App.output_path = self.output_path.get()
	    	self.browse_path_button.configure(text = App.output_path)
	    	self.update_dat_file()

	def on_closing(self):
		close = messagebox.askokcancel("Close", "Would you like to close the program?")
		self.update_dat_file()
		if close:
			self.destroy()
		# self.destroy()

	def reset_button(self):
		if App.saved_combinations_file is None: 
			if os.path.exists(App.combo_save_file):
				App.saved_combinations_file = pickle.load(open(App.combo_save_file, 'rb'))


		try:
			del App.saved_combinations_file[0][App.sub_key]
			del App.saved_combinations_file[1][App.sub_key]
			self.info_label.configure(text = f"Your prgress of {App.sub_key.replace('_',' ')} tests\n have been resetted...")
			self.resave_saved_combinations_file()
		except:
			pass

if __name__=='__main__':
	app = App()
	app.mainloop()
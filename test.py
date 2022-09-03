# import utils
# import pickle
# import os
# import random
# from tqdm import tqdm
# import numpy as np
# import cv2
# import matplotlib.pyplot as plt
# from PIL import Image
# import glob
# import img2pdf

# # Hyper parameters
# combo_save_file = "datsavfiles/combinations.pickle"
# path = "question_datafiles/IGCSE"
# reset_combinations = False
# # path_qs = "question_datafiles/Physics_paper_2.pickle"

# files = os.listdir(path)
# sub_names = [i.replace('.pickle','').replace('_',' ') for i in files]
# print("Which subject do you want to generate tests of? ")
# for i in range(len(sub_names)):
# 	print(f'{i}. {sub_names[i]}')

# subject_index = int(input("\nEnter option from above:"))
# qs_path = f"{path}/{files[subject_index]}"
# subject_key = files[subject_index].replace('.pickle','')

# # Load the datafile
# qs_data = pickle.load(open(qs_path, 'rb'))
# qs_id_to_img = qs_data[1]
# mcq_id_to_img = qs_data[4]

# qs_id_used = qs_data[2]
# mcq_id_used = qs_data[5]

# ms_id_to_img = qs_data[-3]



# # NOTE: saved_combinations_file = [subject_combination_dictionary, current_combo_index_dictionary]
# # 		subject_combination_dictionary = {subject_name: [[qs_combo_lists],[mcq_combo_lists]], ...}
# # 		current_combo_index_dictionary = {subject_name: [qs_combo_index, mcq_combo_index], ...}
# subject_combinations, current_combo_index = utils.retrieve_or_generate_combinations(combo_save_file, files, subject_index, qs_data)
# qs_combination_list = subject_combinations[subject_key][0]
# mcq_combination_list = subject_combinations[subject_key][1]

# qs_combination_ids = qs_combination_list[2]#current_combo_index[subject_key][0]]
# if mcq_combination_list:
# 	mcq_combination_ids = mcq_combination_list[current_combo_index[subject_key][1]]
# else:
# 	print(mcq_combination_list)
# 	mcq_combination_ids = None

# def reverse_sort_img_files(img_files):
#     files = []
#     path_origin = ''
#     for i in img_files:
#         split_list = i.split('/')
#         files.append(int( split_list[-1].replace(".jpeg", '') ))
        
#         if path_origin == '':
#             for x in split_list[:-1]:
#                 path_origin+=x+'/'
    

#     files = sorted(files, reverse = True)
#     # del split_list

#     img_files = [path_origin+str(i)+".jpeg" for i in files]

#     return img_files

# def create_pages(mcq_combination_ids, mcq_id_to_img, mcq_id_used ,qs_combination_ids, qs_id_to_img, qs_id_used, ms_id_to_img ,v_lim = 1490, h_fixed = 1054, output_file = 'test.pdf'):
# 	pages = []
# 	pages_ms = []
# 	qs_num = 1
# 	image = None
# 	if mcq_combination_ids is not None:
# 		for id_ in mcq_combination_ids:
# 			mark = mcq_id_used[id_][-1]
# 			for i in range(len(mcq_id_to_img[id_])):
# 				img = mcq_id_to_img[id_][i]
# 				img = cv2.cvtColor(cv2.resize(img, (h_fixed, img.shape[0])), cv2.COLOR_GRAY2RGB)
# 				if i == 0:
# 					# Adding number and white bg to the number only used if first page of id
# 					cv2.rectangle(img, (0,0), (45,80), color = (255,255,255),thickness = -1)
# 					cv2.putText(img,f'{qs_num}.',(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,0,2,2)
					

# 				if i == len(mcq_id_to_img[id_])-1:
# 					# adding marks of the qs and white bg for mark, only used of last page of id
# 					cv2.rectangle(img, (0, img.shape[0]-25), (img.shape[1], img.shape[0]), color = (255,255,255),thickness = -1)
# 					if int(mark)>1:
# 						mt = 'marks'
# 					else:
# 						mt = 'mark'
# 					sentence = f"(Total for question {qs_num} is {mark} {mt})"
# 					cv2.putText(img, sentence, (img.shape[1]-600,img.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 1,0,2,2)


# 				if image is None:
# 					image = img
# 				elif image.shape[0]+img.shape[0]<=v_lim:
# 					image = np.concatenate((image, img), axis = 0)
# 				else:
# 					image = cv2.copyMakeBorder(image, 0, abs(v_lim-image.shape[0]), 0, 0, cv2.BORDER_CONSTANT, None, [255,255,255])
# 					pages.append(image)
# 					image = img

# 			for i in range(len(ms_id_to_img[id_])):
# 				print(i)
# 				img = ms_id_to_img[id_][i]
# 				img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
				
# 				if i == 0:
# 					# Adding number and white bg to the number only used if first page of id
# 					cv2.rectangle(img, (0,0), (45,80), color = (255,255,255),thickness = -1)
# 					cv2.putText(img,f'{qs_num}.',(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,0,2,2)
# 				pages_ms.append(img)


# 			qs_num+=1
# 			image = cv2.copyMakeBorder(image, 0, abs(v_lim-image.shape[0]), 0, 0, cv2.BORDER_CONSTANT, None, [255,255,255])
# 			pages.append(image)
# 			image = None


# 	for id_ in qs_combination_ids:
# 		mark = qs_id_used[id_][-1]
# 		for i in range(len(qs_id_to_img[id_])):
# 			img = qs_id_to_img[id_][i]
# 			img = cv2.cvtColor(cv2.resize(img, (h_fixed, img.shape[0])), cv2.COLOR_GRAY2RGB)
# 			if i == 0:
# 				# Adding number and white bg to the number only used if first page of id
# 				cv2.rectangle(img, (0,0), (45,80), color = (255,255,255),thickness = -1)
# 				cv2.putText(img,f'{qs_num}.',(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,0,2,2)
				

# 			if i == len(qs_id_to_img[id_])-1:
# 				# adding marks of the qs and white bg for mark, only used of last page of id
# 				cv2.rectangle(img, (0, img.shape[0]-25), (img.shape[1], img.shape[0]), color = (255,255,255),thickness = -1)
# 				if int(mark)>1:
# 					mt = 'marks'
# 				else:
# 					mt = 'mark'
# 				sentence = f"(Total for question {qs_num-1} is {mark} {mt})"
# 				cv2.putText(img, sentence, (img.shape[1]-600,img.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 1,0,2,2)


# 			if image is None:
# 				image = img
# 			elif image.shape[0]+img.shape[0]<=v_lim:
# 				image = np.concatenate((image, img), axis = 0)
# 			else:
# 				image = cv2.copyMakeBorder(image, 0, abs(v_lim-image.shape[0]), 0, 0, cv2.BORDER_CONSTANT, None, [255,255,255])
# 				pages.append(image)
# 				image = img
				
# 		for i in range(len(ms_id_to_img[id_])):
# 			img = ms_id_to_img[id_][i]
# 			img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
# 			if i == 0:
# 				# Adding number and white bg to the number only used if first page of id
# 				cv2.rectangle(img, (0,0), (45,80), color = (255,255,255),thickness = -1)
# 				cv2.putText(img,f'{qs_num}.',(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,0,2,2)
# 			pages_ms.append(img)


# 		qs_num+=1
# 		image = cv2.copyMakeBorder(image, 0, abs(v_lim-image.shape[0]), 0, 0, cv2.BORDER_CONSTANT, None, [255,255,255])
# 		pages.append(image)
# 		image = None

# 	for i in range(len(pages)):
# 		cv2.imwrite(f'Lab/{i}.jpeg', pages[i])

# 	files = reverse_sort_img_files(glob.glob("Lab/*.jpeg"))[::-1]
# 	with open(output_file,'wb')as f:
# 		f.write(img2pdf.convert(files))
# 	for file in tqdm(files):
# 		os.remove(file)


# 	for i in range(len(pages_ms)):
# 		cv2.imwrite(f'Lab/{i}.jpeg', pages_ms[i])

# 	files = reverse_sort_img_files(glob.glob("Lab/*.jpeg"))[::-1]
# 	with open('test_ms.pdf','wb')as f:
# 		f.write(img2pdf.convert(files))
# 	for file in tqdm(files):
# 		os.remove(file)
		
	



# create_pages(mcq_combination_ids, mcq_id_to_img, mcq_id_used,qs_combination_ids, qs_id_to_img, qs_id_used,ms_id_to_img)




# # 






# '''
# files = glob.glob('*.jpeg')
# new = []
# image = cv2.imread(files[0])

# # Adding number and white bg to the number only used if first page of id
# cv2.rectangle(image, (0,0), (45,90), color = (255,255,255),thickness = -1)
# cv2.putText(image,'1.',(10,65),cv2.FONT_HERSHEY_SIMPLEX,1,0,2,2)

# # adding marks of the qs and white bg for mark, only used of last page of id
# cv2.rectangle(image, (0, image.shape[0]-25), (image.shape[1],image.shape[0]), color = (255,255,255),thickness = -1)
# cv2.putText(image, "mark 5", (image.shape[1]-150,image.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 1,0,2,2)

# # plt.imshow(image)
# # plt.show()
# for i in range(1, len(files)):
# 	img = cv2.imread(files[i])
# 	cv2.rectangle(img, (0,0), (45,90), color = (255,255,255),thickness = -1)
# 	cv2.putText(img,f'{i+1}.',(10,55),cv2.FONT_HERSHEY_SIMPLEX,1,0,2,2)

# 	cv2.rectangle(image, (0, image.shape[0]-25), (image.shape[1],image.shape[0]), color = (255,255,255),thickness = -1)
# 	cv2.putText(image, "mark 5", (image.shape[1]-150,image.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 1,0,2,2)

# 	if image.shape[0]+img.shape[0]<=1490:
# 		image = np.concatenate((image, img), axis = 0)
# 	else:
# 		image = cv2.copyMakeBorder(image, 0, (1490-image.shape[0]), 0, 0, cv2.BORDER_CONSTANT, None, [255,255,255])
# 		new.append(image)
# 		image = img

# cv2.rectangle(image, (0, image.shape[0]-25), (image.shape[1],image.shape[0]), color = (255,255,255),thickness = -1)
# cv2.putText(image, "mark 5", (image.shape[1]-150,image.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 1,0,2,2)

# image = cv2.copyMakeBorder(image, 0, (1490-image.shape[0]), 0, 0, cv2.BORDER_CONSTANT, None, [255,255,255])
# new.append(image)

# for i in range(len(new)):
# 	cv2.imwrite(f'Lab/{i}.jpeg', new[i])

# files = glob.glob("Lab/*.jpeg")[::-1]
# with open('test.pdf','wb')as f:
# 	f.write(img2pdf.convert(files))
# for file in files:
# 	os.remove(file)
# '''


# import matplotlib.pyplot as plt
# import cv2


# subject_name = "Chemistry unit 4"
# img = cv2.imread('front_page.jpeg')

# # Qualification
# cv2.putText(img,f'IAL',(250,340),cv2.FONT_HERSHEY_SIMPLEX,2,0,6,2)
# # Subject name
# cv2.putText(img,f'{subject_name}',(250,480),cv2.FONT_HERSHEY_SIMPLEX,2,0,6,2)
# # Mark
# cv2.putText(img,f'90',(540,1060),cv2.FONT_HERSHEY_SIMPLEX,1,0,2,2)


# plt.imshow(img)
# plt.show()


import sys
from tkinter import Tk, Button, Frame
from tkinter.scrolledtext import ScrolledText
import time

class PrintLogger(object):  # create file like object

    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref

    def write(self, text):
        self.textbox.configure(state="normal")  # make field editable
        self.textbox.insert("end", text)  # write text to textbox
        self.textbox.see("end")  # scroll to end
        self.textbox.configure(state="disabled")  # make field readonly

    def flush(self):  # needed for file like object
       	pass


class MainGUI(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.root = Frame(self)
        self.root.pack()
        self.redirect_button = Button(self.root, text="Redirect console to widget", command=self.redirect_logging)
        self.redirect_button.pack()
        self.redirect_button = Button(self.root, text="Redirect console reset", command=self.reset_logging)
        self.redirect_button.pack()
        self.test_button = Button(self.root, text="Test Print", command=self.test_print)
        self.test_button.pack()
        self.log_widget = ScrolledText(self.root, height=4, width=120, font=("consolas", "8", "normal"))
        self.log_widget.pack()
        self.redirect_logging()






    def reset_logging(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def test_print(self):
        print("Am i working?")

    def redirect_logging(self):
        logger = PrintLogger(self.log_widget)

        sys.stdout = logger
        sys.stderr = logger


if __name__ == "__main__":
    app = MainGUI()
    app.mainloop()

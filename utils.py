import utils
import pickle
import os
import random
from tqdm import tqdm
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import glob
import img2pdf
import numpy as np

class Combinator:
	def __init__(self,score_to_id, target, id_used, papers_used ,mcq = True):
		self.score_to_id = score_to_id
		self.target = target
		self.papers_used = papers_used
		self.id_used = id_used
		self.mcq = mcq
		self.combinations = []
		self.score_dict_ = {}

	def backtrack(self,candidates ,cur, pos, target):
		if target==0:
			self.combinations.append(cur.copy())
		if target<=0:
			return


		prev = -1
		for i in range(pos, len(candidates)):
			if candidates[i]==prev:
				continue
			cur.append(candidates[i])
			self.backtrack(candidates, cur, i+1, target- candidates[i])
			cur.pop()
			prev = candidates[i]

	def generate_combinations(self):
		candidates = []
		for score in self.score_to_id:
			self.score_dict_[int(score)] = len(self.score_to_id[score])
			for i in range(len(self.score_to_id[score])):
				candidates.append(int(score))
		candidates = sorted(candidates)
		self.backtrack(candidates,[], 0, self.target)


		if self.mcq:
			for i in range(self.score_dict_[1]//self.target):
				self.combinations.append([1]*self.target)
		
		if len(self.combinations)<self.papers_used*2:
			self.combinations*=self.papers_used

		np.random.shuffle(self.combinations)
		# print(self.combinations)
		# if len(self.combinations)>1000:
		# 	self.combinations = self.combinations[:1000]
			# print(len(self.combinations))
		combo_list = []

		for pos in range(len(self.combinations)):
		    score_dict = self.score_dict_.copy()

		    combo = []
		    for i in range(pos, len(self.combinations)):
		        use_combo = True
		        for x in range(len(self.combinations[i])):
		            score = self.combinations[i][x]
		            if score_dict[score]>0:
		                score_dict[score]-=1
		            else:
		                use_combo = False
		                for c in range(x):
		                    score_dict[self.combinations[i][c]]+=1
		                break
		        if use_combo:
		            combo.append(self.combinations[i])
		        
		        if len(combo)==self.papers_used:
		            break
		    print(score_dict)       
		    if len(combo) == self.papers_used:
		        combo_list.append(combo)

		    if len(combo_list)>self.papers_used:
		    	break


		return combo_list


	def get_idlist_of_combinations(self,combos):
		combination_ids = []

		for combination in combos:
			ids = []
			for score in combination:
				for id_ in self.score_to_id[str(score)]:
					if not self.id_used[id_][0]:
						self.id_used[id_][0] = True
						ids.append(id_)
						break
			combination_ids.append(ids)
		return combination_ids


# datafiles_struct = 
#		[qs_score_to_id, qs_id_to_img, qs_id_used,mcq_score_to_id, mcq_id_to_img, mcq_id_used, num_papers, ms_id_to_img, qs_target_mark, mcq_target_mark]

def randomize_score_to_ID(score_to_id):
	if len(score_to_id): 
		for score in score_to_id.keys():
			# print(score_to_id[score])
			for i in range(random.randint(2,4)):
				random.shuffle(score_to_id[score])
			# print(score_to_id[score])
	return score_to_id



def get_combination(qs_data):
	qs_target = qs_data[-2]
	mcq_target = qs_data[-1]

	qs_score_to_id = randomize_score_to_ID(qs_data[0])
	mcq_score_to_id = randomize_score_to_ID(qs_data[3])
	# total = 0
	# for score in qs_score_to_id.keys():
	# 	total+=int(score)*len(qs_score_to_id[score])
	# print(total/110)


	# qs_id_to_img = qs_data[1]
	# mcq_id_to_img = qs_data[4]

	qs_id_used = qs_data[2]
	mcq_id_used = qs_data[5]

	num_papers_used = qs_data[-4]

	return_values = []

	# variables to change when sub is changed, papers_used
	qs_combinator= Combinator(qs_score_to_id, qs_target, qs_id_used,papers_used = num_papers_used,mcq = False)
	qs_combo_list =qs_combinator.generate_combinations()
	qs_combos = qs_combo_list[random.randint(0, len(qs_combo_list)-1)]
	qs_combo_ids = qs_combinator.get_idlist_of_combinations(qs_combos)
	return_values.append(qs_combo_ids)
	if mcq_target:
		mcq_combinator = Combinator(mcq_score_to_id, mcq_target, mcq_id_used, papers_used = num_papers_used,mcq = True)
		mcq_combo_list = mcq_combinator.generate_combinations()
		mcq_combos = mcq_combo_list[random.randint(0, len(mcq_combo_list)-1)]
		mcq_combos_2 = mcq_combo_list[random.randint(0, len(mcq_combo_list)-1)]
		mcq_combo_ids = mcq_combinator.get_idlist_of_combinations(mcq_combos)

		for key in mcq_id_used.keys():
			mcq_id_used[key][0] = False


		mcq_combo_ids_2 = mcq_combinator.get_idlist_of_combinations(mcq_combos_2)
		return_values.append(mcq_combo_ids)
		return_values.append(mcq_combo_ids_2)
	else:
		return_values.append(None)
		return_values.append(None)

	return return_values


def save_combination_file(combo_save_file, subject_combinations, current_combo_index):
	pass


def retrieve_or_generate_combinations(combo_save_file, files, subject_index, qs_data):
	if not os.path.exists(combo_save_file):
		subject_combinations = {f"{files[subject_index].replace('.pickle','')}": get_combination(qs_data)}
		current_combo_index = {f"{files[subject_index].replace('.pickle','')}":[0,0,0]}
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


		if files[subject_index].replace('.pickle','') in subject_combinations.keys():
			print("The subject combination is in the file")
		else:
			print("Not in file, thus generating combinations")
			subject_combinations[f"{files[subject_index].replace('.pickle','')}"] = get_combination(qs_data)
			current_combo_index[f"{files[subject_index].replace('.pickle','')}"] = [0,0,0]
			print("Saving combinations for later use...")
			pickle.dump([subject_combinations, current_combo_index], open(combo_save_file,'wb'))

	return [subject_combinations, current_combo_index]
			



def reverse_sort_img_files(img_files):
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

def create_pages(mcq_combination_ids, mcq_id_to_img, mcq_id_used ,qs_combination_ids, qs_id_to_img, qs_id_used, ms_id_to_img,front_page,full_test = True ,v_lim = 1490, h_fixed = 1054, output_qs_file = f'test.pdf',output_ms_file = 'test_ms.pdf'):
	pages = []
	pages_ms = []
	qs_num = 1
	image = None
	if mcq_combination_ids is not None:
		for id_ in mcq_combination_ids:
			mark = mcq_id_used[id_][1]
			for i in range(len(mcq_id_to_img[id_])):
				img = mcq_id_to_img[id_][i]
				img = cv2.cvtColor(cv2.resize(img, (h_fixed, img.shape[0])), cv2.COLOR_GRAY2RGB)
				if i == 0:
					# Adding number and white bg to the number only used if first page of id
					cv2.rectangle(img, (0,0), (45,80), color = (255,255,255),thickness = -1)
					cv2.putText(img,f'{qs_num}.',(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,0,2,2)
					

				if i == len(mcq_id_to_img[id_])-1:
					# adding marks of the qs and white bg for mark, only used of last page of id
					cv2.rectangle(img, (0, img.shape[0]-25), (img.shape[1], img.shape[0]), color = (255,255,255),thickness = -1)
					if int(mark)>1:
						mt = 'marks'
					else:
						mt = 'mark'
					sentence = f"(Total for question {qs_num} is {mark} {mt})"
					cv2.putText(img, sentence, (img.shape[1]-600,img.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 1,0,2,2)


				if image is None:
					image = img
					# print(image.shape)
				elif (image.shape[0]+img.shape[0])<=v_lim:
					print(f"joint: {image.shape[0]+img.shape[0]}")
					image = np.concatenate((image, img), axis = 0)
				
				else:
					# print('Adding pages together...')
					image = cv2.copyMakeBorder(image, 0, abs(v_lim-image.shape[0]), 0, 0, cv2.BORDER_CONSTANT, None, [255,255,255])
					pages.append(image)
					image = img




			for i in range(len(ms_id_to_img[id_])):
				img = ms_id_to_img[id_][i]
				img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
				
				if i == 0:
					# Adding number and white bg to the number only used if first page of id
					cv2.rectangle(img, (0,0), (45,80), color = (255,255,255),thickness = -1)
					cv2.putText(img,f'{qs_num}.',(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,0,2,2)
				pages_ms.append(img)


			qs_num+=1
		image = cv2.copyMakeBorder(image, 0, abs(v_lim-image.shape[0]), 0, 0, cv2.BORDER_CONSTANT, None, [255,255,255])
		pages.append(image)
		image = None

	if full_test:
		print("full test")
		for id_ in qs_combination_ids:
			mark = qs_id_used[id_][1]
			for i in range(len(qs_id_to_img[id_])):
				img = qs_id_to_img[id_][i]
				img = cv2.cvtColor(cv2.resize(img, (h_fixed, img.shape[0])), cv2.COLOR_GRAY2RGB)
				if i == 0:
					# Adding number and white bg to the number only used if first page of id
					cv2.rectangle(img, (0,0), (45,80), color = (255,255,255),thickness = -1)
					cv2.putText(img,f'{qs_num}.',(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,0,2,2)
					

				if i == len(qs_id_to_img[id_])-1:
					# adding marks of the qs and white bg for mark, only used of last page of id
					cv2.rectangle(img, (0, img.shape[0]-25), (img.shape[1], img.shape[0]), color = (255,255,255),thickness = -1)
					if int(mark)>1:
						mt = 'marks'
					else:
						mt = 'mark'
					sentence = f"(Total for question {qs_num} is {mark} {mt})"
					cv2.putText(img, sentence, (img.shape[1]-600,img.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 1,0,2,2)



				if image is None:
					image = img
				elif image.shape[0]+img.shape[0]<=v_lim:
					image = np.concatenate((image, img), axis = 0)
				else:
					image = cv2.copyMakeBorder(image, 0, abs(v_lim-image.shape[0]), 0, 0, cv2.BORDER_CONSTANT, None, [255,255,255])
					pages.append(image)
					image = img



			for i in range(len(ms_id_to_img[id_])):
				img = ms_id_to_img[id_][i]
				img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
				if i == 0:
					# Adding number and white bg to the number only used if first page of id
					cv2.rectangle(img, (0,0), (45,80), color = (255,255,255),thickness = -1)
					cv2.putText(img,f'{qs_num}.',(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,0,2,2)
				pages_ms.append(img)


			qs_num+=1
			image = cv2.copyMakeBorder(image, 0, abs(v_lim-image.shape[0]), 0, 0, cv2.BORDER_CONSTANT, None, [255,255,255])
			pages.append(image)
			image = None

	last_page = pages[-1]
	cv2.rectangle(last_page, (10,v_lim-30), (396,v_lim), color = (0,200,0),thickness = -1)
	cv2.putText(last_page,f'IAO TestSuite by Ishraque sarwar',(10, v_lim-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,0,2,2)
	pages[-1] = last_page
	for i in range(len(pages)):
		cv2.imwrite(f'Lab/{i}.jpeg', pages[i])

	files = reverse_sort_img_files(glob.glob("Lab/*.jpeg"))[::-1]



	cv2.imwrite('Lab/front_page.jpeg', front_page)
	files.insert(0, 'Lab/front_page.jpeg')
	with open(output_qs_file,'wb')as f:
		f.write(img2pdf.convert(files))
	for file in tqdm(files):
		os.remove(file)


	# for i in range(len(pages)):
	# 	cv2.imwrite(f'Lab/{i}.jpeg', pages_ms[i])
	
	# files = reverse_sort_img_files(glob.glob("Lab/*.jpeg"))[::-1]
	# cv2.imwrite('Lab/front_page.jpeg', front_page)
	# files.insert(0, 'Lab/front_page.jpeg')
	# with open(output_ms_file,'wb')as f:
	# 	f.write(img2pdf.convert(files))
	# for file in tqdm(files):
	# 	os.remove(file)
	


	for i in range(len(pages_ms)):
		cv2.imwrite(f'Lab/{i}.jpeg', pages_ms[i])

	files = reverse_sort_img_files(glob.glob("Lab/*.jpeg"))[::-1]
	with open(output_ms_file,'wb')as f:
		f.write(img2pdf.convert(files))
	for file in tqdm(files):
		os.remove(file)
	


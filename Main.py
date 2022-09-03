import utils
import pickle
import os
import random
from tqdm import tqdm


# Hyper parameters
combo_save_file = "datsavfiles/combinations.pickle"
reset_combinations = False
# path_qs = "question_datafiles/Physics_paper_2.pickle"

files = os.listdir("question_datafiles")
sub_names = [i.replace('.pickle','').replace('_',' ') for i in files]
print("Which subject do you want to generate tests of? ")
for i in range(len(sub_names)):
	print(f'{i}. {sub_names[i]}')

subject_index = int(input("\nEnter option from above:"))
qs_path = f"question_datafiles/{files[subject_index]}"

# Load the datafile
qs_data = pickle.load(open(qs_path, 'rb'))
qs_id_to_img = qs_data[1]
mcq_id_to_img = qs_data[4]


subject_combinations, current_combo_index = utils.retrieve_or_generate_combinations(combo_save_file, files, subject_index)



def create_pages(combination_ids, id_to_img):
	pass
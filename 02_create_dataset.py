import csv
import os
import pickle
import sys
import fakenews_lib

# This code is adapted from https://github.com/nayakneha/fakenews

# Define paths here

TRAIN_STANCES_PATH = "../fnc-1/train_stances.csv"
TEST_STANCES_PATH = "../fnc-1/competition_test_stances.csv"
TRAIN_OUTPUT_DIR = "./train_examples/"
TEST_OUTPUT_DIR = "./test_examples/"
TRAIN_DATASET_NAME = "DUPLICATE_TRAIN_DATASET"
TEST_DATASET_NAME = "TEST_DATASET"

def write_dataset(dataset_output_file,output_dir,data_path):

  headline_number_map = {} # Headline text to number
  headlines_xml_map = {} # Headline number to text
  bodies_xml_map = {} # Body number to text

  for file_name in os.listdir(output_dir):
    text_number = os.path.basename(file_name).split('.')[0]

    if file_name.endswith('.body'):
      continue

    with open(output_dir + file_name, 'r') as f:
      file_text = f.read()

    if file_name.endswith('.headline'):
      headline_number_map[file_text] = text_number
    elif file_name.endswith('.headline.xml'):
      headlines_xml_map[text_number] = file_text
    else:
      assert file_name.endswith('body.xml')
      bodies_xml_map[text_number] = file_text

  # Read in stance dict
  examples = []
  with open(data_path) as csv_file:
    stances_reader = csv.reader(csv_file)
    _ = stances_reader.next()
    for row in stances_reader:
      headline, body_id, stance = row
      examples.append(fakenews_lib.Example(
        headline_number_map[headline], body_id, stance))

  dataset = fakenews_lib.Dataset(headlines_xml_map, bodies_xml_map, examples)

  with open(dataset_output_file, 'w') as out_file:
    pickle.dump(dataset, out_file)


def main():
  write_dataset(TRAIN_DATASET_NAME,TRAIN_OUTPUT_DIR,TRAIN_STANCES_PATH)
  write_dataset(TEST_DATASET_NAME,TEST_OUTPUT_DIR,TEST_STANCES_PATH)

if __name__ == "__main__":
  main()

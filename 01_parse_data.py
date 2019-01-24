import os
import sys

# This code is adapted from https://github.com/nayakneha/fakenews

# Define paths here

TRAIN_OUTPUT_DIR = "./train_examples/"
TEST_OUTPUT_DIR = "./test_examples/"
PATH_TO_CORENLP = "../stanford-corenlp-full-2018-10-05/"

def run_parser(output_dir,path_to_corenlp,start_range=0,end_range=4000):
  
  command_line =("java -Xmx5g -cp"
  " \"{}*\""  
  " edu.stanford.nlp.pipeline.StanfordCoreNLP -file "
  " \"{}{}\"" 
  " -outputDirectory \"{}\"") 

  for file_name in os.listdir(output_dir):
    if (file_name.endswith('.headline') or file_name.endswith('.body')) \
        and (file_name + '.xml' not in os.listdir(output_dir)):
      file_number = int(filter(lambda x:x.isdigit(),file_name))
      if (file_number >= start_range) and (file_number < end_range):
        print(file_name)
        os.system(command_line.format(path_to_corenlp,output_dir,file_name,output_dir))
  

def main():
  # To parallelize, pass in non overlapping start and end ranges 
  try:
    start_range = int(sys.argv[1])
    end_range = int(sys.argv [2])
    run_parser(TRAIN_OUTPUT_DIR,PATH_TO_CORENLP,start_range,end_range)
    run_parser(TEST_OUTPUT_DIR,PATH_TO_CORENLP,start_range,end_range)
  except:
    run_parser(TRAIN_OUTPUT_DIR,PATH_TO_CORENLP)
    run_parser(TEST_OUTPUT_DIR,PATH_TO_CORENLP)

if __name__ == "__main__":
  main()

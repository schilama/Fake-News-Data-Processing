import sklearn
import csv
import os

# This code is adapted from https://github.com/nayakneha/fakenews

# Define paths here

TRAIN_BODIES_PATH = "../fnc-1/train_bodies.csv"
TEST_BODIES_PATH = "../fnc-1/competition_test_bodies.csv"
TRAIN_HEADLINE_PATH = "../fnc-1/train_stances.csv"
TEST_HEADLINE_PATH = "../fnc-1/competition_test_stances.csv"
TRAIN_HEADLINE_MAP_PATH = "./train_headline_map.csv"
TEST_HEADLINE_MAP_PATH = "./test_headline_map.csv"
TRAIN_OUTPUT_DIR = "./train_examples/"
TEST_OUTPUT_DIR = "./test_examples/"

class Label(object):
  UNRELATED='unrelated'
  AGREE='agree'
  DISAGREE='disagree'
  DISCUSS='discuss'

class FileType(object):
  STANCE='stance'
  HEADLINE='headline'
  BODY='body'

ID_hdr = "Body ID"
BODY_hdr = "articleBody"
HEADLINE_hdr = "Headline"
STANCE_hdr = "Stance"

VALID_LABELS = [Label.UNRELATED, Label.AGREE, Label.DISCUSS, Label.DISAGREE]
file_types = [FileType.STANCE, FileType.HEADLINE, FileType.BODY]

class Example(object):
  def __init__(self, headline, body, stance, identifier):
    self.headline = headline
    self.body = body
    assert stance in VALID_LABELS
    self.stance = stance
    self.identifier = identifier

def get_file_name(output_dir, key, file_type):
  key_str = key.zfill(4)
  return "".join([output_dir, key_str, ".", file_type])
  
def read_bodies(data_path,output_dir):

  with open(data_path) as csv_file:
	  article_reader = csv.DictReader(csv_file)
	  for row in article_reader:
	    body_id, body = row[ID_hdr], row[BODY_hdr]
	    with open(get_file_name(output_dir,body_id,FileType.BODY),'w') as f:
		    f.write(body)
	  
def read_headlines(data_path,headline_map_path, output_dir):

  headlines = set()
  with open(data_path) as csv_file:
    stance_reader = csv.reader(csv_file)
    for i, row in enumerate(stance_reader):
      headline, body_id, stance = row
      headlines.add(headline)

  headline_list = sorted(list(headlines))
  headline_map = { headline: str(headline_list.index(headline)).zfill(4)
                   for headline in headline_list}

  with open(headline_map_path,'w') as output_csv_file:
   headline_writer = csv.writer(output_csv_file)
   for headline, headline_id in headline_map.iteritems():
     headline_writer.writerow([headline, headline_id])

  for headline in headline_list:
    headline_id = headline_map[headline]
    with open(get_file_name(output_dir, headline_id, FileType.HEADLINE), 'w') as f:
      f.write(headline)

def main():
  read_headlines(TRAIN_HEADLINE_PATH, TRAIN_HEADLINE_MAP_PATH, TRAIN_OUTPUT_DIR)
  read_headlines(TEST_HEADLINE_PATH, TEST_HEADLINE_MAP_PATH, TEST_OUTPUT_DIR)
  read_bodies(TRAIN_BODIES_PATH,TRAIN_OUTPUT_DIR)
  read_bodies(TEST_BODIES_PATH,TEST_OUTPUT_DIR)

if __name__ == "__main__":
  main()

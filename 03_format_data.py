import sys
reload(sys)
sys.setdefaultencoding('utf8')
import pickle

# Modify paths here

TRAIN_DATASET_NAME = "./TRAIN_DATASET"
TEST_DATASET_NAME = "./TEST_DATASET"
TRAIN_FILE_NAME = "./train_dataschil800.txt"
DEV_FILE_NAME = "./eval_dataschil800.txt"
TEST_FILE_NAME = "./test_dataschil800.txt"
MAX_SEQ_LEN = 800

DOMAIN_PLACEHOLDER = "fakenews"
S = "schil" # A separator that is not present in the data

def format(dataset,filename,start_range=0,stop_range=50000,max_seq_len=100000):
  with open(dataset,'rb') as fp:
    d = pickle.load(fp)
    examples = d.examples
    headlines_map = d.headlines_map
    bodies_map = d.bodies_map
    sentence_id = 0
    fp = open(filename,"w")
    for example in examples[start_range:stop_range]:
      headline_number = example.headline_number
      body_number = example.body_number
      stance = example.stance
      # Headline processing
      headline = headlines_map[headline_number]
      sentence = headline.sentence
      nodes = list(sentence.dependency_parse.nodes.keys())
      nodes.sort(key=lambda x:int(x))
      writethis = ""
      tokenidoffset = 0
      for i,node in enumerate(nodes):
        if node == '0':
          continue
        n = sentence.dependency_parse.nodes[node]
        towrite = DOMAIN_PLACEHOLDER + S + str(sentence_id) + S + str(int(n.idx)-1) + S + n.text + S
        towrite += sentence.tokens['POS'][i-1] + S + sentence.tokens['POS'][i-1] + S + n.governor_idx + S + n.dep_type + S
        towrite += '-' + S + '-' + S + sentence.tokens['lemma'][i-1] + S + '-' + S + '-' + S + '<S1>' + S + stance + "\n"
        writethis += towrite
        tokenidoffset += 1
      # Separator line
      towrite = DOMAIN_PLACEHOLDER + S + str(sentence_id) + S + str(tokenidoffset) + S + '<SEP>' + S
      towrite += '<SEP>' + S + '<SEP>' + S + str(tokenidoffset) + S + 'root' + S
      towrite += '-' + S + '-' + S + '<SEP>' + S + '-' + S + '-' + S + '<SEP>' + S + stance + "\n"
      writethis += towrite
      tokenidoffset += 1
      # Body processing
      body = bodies_map[body_number]
      for sentence in body.sentences:
        nodes = list(sentence.dependency_parse.nodes.keys())
        nodes.sort(key=lambda x:int(x))
        thissentenceoffset = 0
        for i,node in enumerate(nodes):
          if node == '0':
            continue
          n = sentence.dependency_parse.nodes[node]
          towrite = DOMAIN_PLACEHOLDER + S + str(sentence_id) + S + str(int(n.idx)+tokenidoffset-1) + S + n.text + S
          towrite += sentence.tokens['POS'][i-1] + S + sentence.tokens['POS'][i-1] + S + str(int(n.governor_idx)+tokenidoffset) + S
          towrite += n.dep_type + S
          towrite += '-' + S + '-' + S + sentence.tokens['lemma'][i-1] + S + '-' + S + '-' + S + '<S2>' + S + stance + "\n"
          writethis += towrite
          thissentenceoffset += 1
        tokenidoffset += thissentenceoffset
      writethis += "\n"
      if tokenidoffset <= max_seq_len:
        fp.write(writethis)
      sentence_id += 1
    fp.close()     

def main():
  format(TRAIN_DATASET_NAME,TRAIN_FILE_NAME,0,40001,MAX_SEQ_LEN)
  format(TRAIN_DATASET_NAME,DEV_FILE_NAME,40001,50000,MAX_SEQ_LEN)
  format(TEST_DATASET_NAME,TEST_FILE_NAME,0,50000,MAX_SEQ_LEN)

if __name__ == "__main__":
	main()

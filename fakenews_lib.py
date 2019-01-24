import collections
import lxml.etree as ET

# This code is taken from https://github.com/nayakneha/fakenews

REQUIRED_TAGS = ['word', 'lemma', 'POS']
STANCES = ['agree', 'disagree', 'discuss', 'unrelated']

OPEN_CLASS_TAGS = ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS",
    "RB", "RBR", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

class DependencyNode(object):
  def __init__(self, idx, text, governor_idx, dep_type):
    self.idx = idx
    self.text = text
    self.governor_idx= governor_idx
    self.dep_type = dep_type
    self.children = []


class DependencyParse(object):
  def __init__(self):
    root_node = DependencyNode("0", "ROOT", "-1", "None")
    self.nodes = {"0":root_node}
    pass

  def add_dependency(self, dependency):
    assert dependency.tag == "dep"
    for child in dependency:
      if child.tag == "governor":
        governor_idx = child.get("idx")
      else:
        assert child.tag == "dependent"
        dependent_idx = child.attrib["idx"]
        dependent_text = child.text
    self.nodes[dependent_idx] = DependencyNode(dependent_idx, dependent_text,
        governor_idx, dependency.attrib["type"])

  def assemble_tree(self):
    for idx, node in self.nodes.iteritems():
      if idx == "0":
        continue
      self.nodes[node.governor_idx].children.append((node.dep_type, node))


class Sentence(object):
  def __init__(self, sentence_xml):
    xml_sentence = ET.XML(sentence_xml)
    if xml_sentence.tag != "sentence":
      for i in xml_sentence:
        if i.tag == "document":
          for sentences in i:
            if sentences.tag == "sentences":
              sentence_xml = sentences[0]
              break
    else:
      sentence_xml = xml_sentence #TODO: fix this horrible thing

    self.dependency_parse = DependencyParse()

    for elem in sentence_xml:
      if elem.tag == "tokens":
        self.tokens = self.add_tokens(elem)
      else:
        assert elem.tag == "dependencies"
        for dep in elem:
          self.dependency_parse.add_dependency(dep)
    self.dependency_parse.assemble_tree()
    self.lemmas = self.tokens['lemma']
    self.open_class = [lemma for lemma, pos in zip(self.tokens['lemma'],
      self.tokens['POS']) if pos in OPEN_CLASS_TAGS]

  def add_tokens(self, tokens):
    tag_lists = collections.defaultdict(list)
    for token in tokens:
      for child in token:
        if child.tag in REQUIRED_TAGS:
          tag_lists[child.tag].append(child.text)
    return tag_lists


class Headline(object):
  def __init__(self, headline_xml, headline_number):
    self.sentence = Sentence(headline_xml)
    self.headline_number = headline_number


class Body(object):
  def __init__(self, body_xml, body_number):
    xml_body = ET.XML(body_xml)
    for i in xml_body:
      if i.tag == "document":
        for sentences in i:
          if sentences.tag == "sentences":
            self.sentences = [Sentence(ET.tostring(sentence_xml)) for
                sentence_xml in sentences]
    self.body_number = body_number


class Example(object):
  def __init__(self, headline_number, body_number, stance=None):
    self.headline_number = headline_number.zfill(4)
    self.body_number = body_number.zfill(4)
    assert stance is None or stance in STANCES
    self.stance = stance

  def headline_lemmas(self, dataset):
    return dataset.headlines_map[self.headline_number].sentence.lemmas

  def body_lemmas(self, dataset):
    return sum([sentence.lemmas for sentence in
        dataset.bodies_map[self.body_number].sentences], [])

  def headline_open_class(self, dataset):
    return dataset.headlines_map[self.headline_number].sentence.open_class

  def body_open_class(self, dataset):
    return sum([sentence.open_class for sentence in
        dataset.bodies_map[self.body_number].sentences], [])



class Dataset(object):
  def __init__(self, headlines_xml_map, bodies_xml_map, examples):
    self.headlines_map = {}
    for headline_number, headline_xml in headlines_xml_map.iteritems():
      self.headlines_map[headline_number] = Headline(headline_xml, headline_number)

    self.bodies_map = {}
    for body_number, body_xml in bodies_xml_map.iteritems():
      self.bodies_map[body_number] = Body(body_xml, body_number)

    self.examples = examples

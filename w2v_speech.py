import gensim, logging, cython, scipy, numpy,re

logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

class MySpeeches(object):
	def __init__(self, file_name):
		self.file = open(file_name, 'r')

	def __iter__(self):
		for line in self.file:
			line = re.sub('\"', '', line)
			yield line.strip().split()

if __name__=='__main__':
	file_name = './all_speech.txt'

	text = MySpeeches(file_name)
	model = gensim.models.Word2Vec()

	logging.info("\n\n\n\nBuilding vocabulary...\n\n\n\n")
	model.build_vocab(text)

	logging.info('\n\n\n\nTraining words...\n\n\n\n')
	model.train(text)

	logging.info('\n\n\n\nModel saved...\n\n\n\n')
	model.save('./w2v_model.mod')

	logging.info('\n\n\n\nExiting gracefully.\n\n\n\n')

	## model has  words





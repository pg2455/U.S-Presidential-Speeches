from textblob import TextBlob, Word
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from functools32 import lru_cache
from nltk.corpus import wordnet
import re, json, logging

logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

class speech_to_text(object):
	
	def __init__(self, file_name):
		self.speeches = open(file_name, 'r').read()
		## Lemmatizer with cache
		self.lemmatize = (lru_cache(maxsize = 50000))(WordNetLemmatizer().lemmatize)
		self.exclude = set(stopwords.words('english'))
		self.not_processed =0
		logger.info("Instance created.")

	def store_indices(self):		
		iterable, self.indices  = re.finditer('\*\*\*', self.speeches), [] ## i.start and i.end represent starting and closing indices
		for i in iterable:
			self.indices.append((i.start(), i.end()))
		self.indices.append((len(self.speeches), len(self.speeches)))


	def extract_data(self):
		self.data = []
		for count,(start, end) in enumerate(self.indices):
			try: 
				speech ={}
				sp = self.speeches[ end + 2 : self.indices[count+1][0] ]
				speech['what'] = sp[:sp.find('\n')]
				sp = sp[ sp.find('\n')+1 : ]
				speech['who'] = sp[:sp.find('\n')]
				sp = sp[ sp.find('\n') + 1 : ]
				speech['date']=  sp[:sp.find('\n')]
				sp = sp[ sp.find('\n') + 2 : ]
				speech['speech'] = sp
				self.data.append(speech)
			except IndexError:
				pass

	def save_data(self):
		with open('data_processed.txt','w') as f:
			f.write(json.dumps(self.data))
		return True

	def write_processed_speeches(self):
		with open('all_speech.txt', 'a') as f:
			for v,i in enumerate(self.data):
				if v%25 ==0:
					logging.info("Progress: @ %d", v)
				f.write(self.clean(i['speech']) + '\n')
		logging.info('File saved as all_speeches.txt')
		return True

	## body clean
	def clean(self, body):
		body =  re.sub('\n',' ', body).strip()
		try:
			body = TextBlob(body)
			tags = body.tags
			tags = [(i[0], pos(i[1])) for i in tags if self.is_word(i[0])] ##store tuples
			words = [self.lemmatize(i, t).lower().decode('utf-8', 'ignore') for i,t in tags if t]
			return " ".join(words)
		except:
			self.not_processed +=1
			return ""

	def is_word(self, word):
		if len(word) <4 or len(word) > 20:
			return False
		if word in self.exclude:
			return False
		return True

'''keep only those words which are | adjective | verb | noun | adverb |'''
def pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


if __name__ == '__main__':
	work = speech_to_text('../speech/data/speech.txt')
	work.store_indices()
	work.extract_data()
	work.save_data()
	work.write_processed_speeches()



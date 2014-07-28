from gensim.models import Word2Vec
from tsne import bh_sne
import numpy, pylab,json,re


class stuff(object):
	def __init__(self):
		self.model = Word2Vec.load('w2v_model.mod')
		self.data =  json.loads(open('data_processed.txt','r').read()) ## a list
		self.processed_speeches = open('all_speech.txt','r')

	def speech_vectors(self):
		l = len(self.data)
		speech_matrix = numpy.zeros(shape = (l, 100))
		for v, line in enumerate(self.processed_speeches):
			words = re.sub('\"','',line).strip().split()
			speech_matrix[v,] = sum(self.model[word] for word in words if word in self.model)
		numpy.save('speech_vectors.npy', speech_matrix)
		self.speech_matrix = speech_matrix

	def tsne(self):
		self.speech_2d = bh_sne(self.speech_matrix)


	def create_plot_2d_speeches(self, withLabels = True):
		if withLabels:
			font = { 'fontname':'Tahoma', 'fontsize':0.5, 'verticalalignment': 'top', 'horizontalalignment':'center' }
			labels= [ (i['who'], i['date']) for i in self.data ]
			pylab.subplots_adjust(bottom =0.1)
			pylab.scatter(self.speech_2d[:,0], self.speech_2d[:,1], marker = '.' ,cmap = pylab.get_cmap('Spectral'))
			for label, x, y in zip(labels, self.speech_2d[:, 0], self.speech_2d[:, 1]):
			    pylab.annotate(
			        label, 
			        xy = (x, y), xytext = None,
			        ha = 'right', va = 'bottom', **font)
			        #,textcoords = 'offset points',bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
			        #arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

			pylab.title('U.S. Presidential Speeches(1790-2006)')
			pylab.xlabel('X')	
			pylab.ylabel('Y')

			pylab.savefig('plot_with_labels', bbox_inches ='tight', dpi = 1000, orientation = 'landscape', papertype = 'a0')
		else:
			pylab.subplots_adjust(bottom =0.1)
			pylab.scatter(self.speech_2d[:,0], self.speech_2d[:,1], marker = 'o' ,cmap = pylab.get_cmap('Spectral'))
			pylab.title('U.S. Presidential Speeches(1790-2006)')
			pylab.xlabel('X')	
			pylab.ylabel('Y')
			pylab.savefig('plot_without_labels', bbox_inches ='tight', dpi = 1000, orientation = 'landscape', papertype = 'a0')
		pylab.close()

if __name__ =='__main__':
	work = stuff()
	work.speech_vectors()
	work.tsne()
	work.create_plot_2d_speeches(True)
	work.create_plot_2d_speeches(False)


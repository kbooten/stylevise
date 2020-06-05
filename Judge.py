from nltk import pos_tag,tokenize,ngrams


import editdistance

import json

with open('easy_medium_hard_expert_evil.json','r') as f:
	easy_medium_hard_expert_evil =  json.load(f)
	
import spacy

try:
	nlp = spacy.load("en")
except:
	nlp = spacy.load("en_core_web_sm")

import re
	


class Judge:
 

	def __init__(self):
		self.minimum_distance = 1
		self._initialize_gram_count_dictionary()
		self.max_level = 4
		self.gram_length = 7


	def _initialize_gram_count_dictionary(self):
		"""
		dictionary for speedier lookup
		"""
		self.gram2level = {}
		for level,grams in easy_medium_hard_expert_evil.items():
			for g in grams:
				g = tuple(g)
				#print(g)
				try:
					self.gram2level[g]=int(level)
				except:
					pass

		
	def _tag_rep(self,sentence):
		sentence = nlp(sentence)
		return tuple([i.tag_ for i in sentence])
	

	def _pos_tag(self,sentence):
		sentence = nlp(sentence)
		return [(t.text,t.tag_) for t in sentence]
		

	def _turn_into_features(self,sentence):
		tags = self._tag_rep(sentence)#[token.lower() if (token.lower() in stops)==True else tag for token,tag in tagged ]
		if len(tags)<=self.gram_length:
			return [tags]
		grams = list(ngrams(tags,self.gram_length))
		return grams


	def is_it_unique_enough(self,newsent,oldsents):
		nearest_dist = 100
		nearest = None
		newsent_processed = self._tag_rep(newsent)
		for o in oldsents:
			o_processed = self._tag_rep(o)
			dist = editdistance.eval(newsent_processed,o_processed)
			if dist<nearest_dist:
				nearest_dist=dist
				nearest = o
		if nearest_dist<self.minimum_distance:
			return (False,nearest)
		return (True,None)


	def _wrap_with_annotation(self,token):
		if token[0]!="<":
			return "<%s>" % token
		return token   


	def _annotate(self,tagged,overlap):
		taggedcopy = tagged[:]
		for o in overlap:
			for i in range(len(tagged)-len(overlap)):
				if o==tuple([tag for token,tag in tagged[i:i+len(o)]]):
					for t in range(i,i+len(o)):
						token,tag = taggedcopy[t]
						taggedcopy[t] = (self._wrap_with_annotation(token),tag)
		just_tags = [token for token,tag in taggedcopy]
		tokens = [token for token,tag in taggedcopy]
		return tokens


	def get_banned(self,level):
		temp_banned = []
		for l in easy_medium_hard_expert_evil.keys():
			if int(l)<=level:
				temp_banned+=easy_medium_hard_expert_evil[l]
		return [tuple(i) for i in temp_banned]


	def is_it_interesting_enough(self,newsent,level):
		tagged = self._pos_tag(newsent)
		banned = self.get_banned(level)
		grams = self._turn_into_features(newsent)
		overlap = []
		for g in list(set(grams)):
			try:
				gram_level = self.gram2level[g]
				if gram_level <= level:
					overlap.append(g)
			except:
				## unique,
				pass
		if overlap!=[]:
			annotated = self._annotate(tagged,overlap)
			return (False, annotated)
		return (True,None)


		
	def input_and_test_new_sent(self,newsent,level=0,oldsents=[]):
		results = self.is_it_unique_enough(newsent,oldsents),self.is_it_interesting_enough(newsent,level)

		formattedResults =  {"interesting":results[1][0],\
							"markedUp":results[1][1],\
							"unique":results[0][0],\
							"prevSent":results[0][1]}

		formattedResults['originalLine'] = newsent
		return formattedResults


def main():
	sv = Judge()
	print(sv.input_and_test_new_sent("The dog was in the house.",level=0))
	print(sv.input_and_test_new_sent("I was once amazed with the cloud.",level=3,oldsents=["I who was once amazed under the tree"]))



if __name__ == '__main__':
	main()

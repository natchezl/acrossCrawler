from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from sklearn.preprocessing import normalize
from nltk.stem.snowball import SnowballStemmer
from nltk import WordPunctTokenizer
import numpy
from string import punctuation as punctuation
import scipy
# from lxml import html
import json
import os
# import sys
# import glob
from operator import itemgetter
import math

LIMIT = 20;
EPSILON = 0.01

# ==Database Initilization====================================================================
from pymongo import MongoClient

client = MongoClient('mongodb://128.199.109.231:9999')
db = client.Scrapy_Reviews
REVIEW_COLLECTION = db.review_all
SUMMARY_COLLECTION = db.summary

# =============================================================================================

en_stem = SnowballStemmer("english")
wpt = WordPunctTokenizer()
stopwords_list = []
stopwords_list.extend(stopwords.words('english'))
stopwords_list.extend(punctuation)

# def en_synonyms(word):
# 	synonyms = set()
# 	synsets = wn.synsets(word)
# 	for synset in synsets:
# 		synonyms.update(synset.lemma_names)
# 	synonyms.add(word)
# 	return synonyms

def tokenize_and_clean(sentence):
	tokens = wpt.tokenize(sentence)
	filtered_tokens = [w for w in tokens if not w in stopwords_list]
# 	print sentence
# 	print filtered_tokens
	return filtered_tokens

def  count_term_in_dictionary(A,i):
	count = 0;
	for j in A[i]:
		if(j>0):
			count = count+1;
	return count;

def cutMatrix(matrix,columnlist):
	columnlist= sorted(columnlist, reverse = True);
	newMatrix = matrix
	print columnlist;
	for col in columnlist:
		newMatrix= scipy.delete(newMatrix,col,1)
	return newMatrix

def createVlist(V):
	V_list = list()
	VT=V.T
	for i in range(0,VT.shape[1]):
		V_list.append((i,0,V[i].sum()))
	V_list = sorted(V_list, key=itemgetter(2,1), reverse=True)
	return V_list

topic = ['cleanliness','comfort','location','staff','value']
summary = dict()
summary2=dict()
summaryFinal= dict()
# == Fetch keywords from json file =========================================
script_dir = os.path.dirname(__file__)
json_data=open('keywords.json')
keywords = json.load(json_data)
json_data.close()


# ==Import reviews from json===========================================
# hotel = glob.glob("bookingJPjson/*")
# hotel = glob.glob("exampleReview/*")
# for json_dir in hotel:
# 	# json_dir = "bookingJPjson\jp-grand-prince-takanawa.json"
# 	json_data=open(json_dir)
# 	reviews = json.load(json_data)
# 	json_data.close()
# 	if len(reviews) < 100:
# 		continue
# 	print json_dir
# 	# json_summary = 'jp-summary/'+json_dir.split("\\")[1][:-5]+'_summary.json';
# 	json_summary = 'exampleSummary/'+json_dir.split("/")[1][:-5]+'_summary.json';
# 	print json_summary

# ==Query data from database====================================================================
items = REVIEW_COLLECTION.find()
# items = alldata
print items.count()
# print items
# =============================================================================
for item in items:
# 	print item
	hotelTitle= item.get("_id")
	comments = item.get("comment")
	sentences =[]
	
# 	for comment in comments:
# 		sent_tokens = sent_tokenize(comment.strip())
# 		for sent_token in sent_tokens:
# 			if(len(tokenize_and_clean(sent_token))>0):
# 				sentences.append(sent_token)

	# /Test/ Use full review sentences
	for comment in comments:
		if(len(tokenize_and_clean(comment))>2):
			sentences.append(comment.strip())
# 		print comment.strip()
	print '\n\n=============================================================================='
	
	for t in topic:
		print 'topic = ' +t
		summary["_id"] = hotelTitle
		summary[t]=list()
		summary2["_id"] = hotelTitle
		summary2[t]=list()
		summaryFinal["_id"] = hotelTitle
		summaryFinal[t]=list()
		feature = list(set(keywords[t]))
	
		feature_mat = dict();
		for c in feature:
			c_stem = en_stem.stem(c)
			feature_mat[c_stem] = list()
	
		key_list = []
		for key, value in feature_mat.iteritems() :
			key_list.append(key);
# 			print key, value
		# ==================================================================================
# 	#for Booking reviews	
# 		for review in reviews:
# 			if review['comment'][0]:
# 				sent_tokens = sent_tokenize(review['comment'][0][0])
# 				for sent_token in sent_tokens:
# 					sentences.append('pos - '+sent_token)
# 			if review['comment'][1]:
# 				sent_tokens = sent_tokenize(review['comment'][1][0])
# 				for sent_token in sent_tokens:
# 					sentences.append('neg - '+sent_token)
# =================================================================================
	
		#tokenized each sentence and count for feature term
		i=0
		for sentence in sentences:	
			for row in feature_mat:
				feature_mat[row].append(0.0)
			filtered_tokens = tokenize_and_clean(sentence)
			for token in filtered_tokens :
				stemmed_token = en_stem.stem(token)
				if(stemmed_token in feature_mat):
					feature_mat[stemmed_token][i] = feature_mat[stemmed_token][i]+1.0
			i=i+1


		# print 'sentences',len(sentences)
		# make matrix A
		# A = list(); #A term-sentence matrix //use tf-idf method to fill each row-col
		U = list(); #U term-topic mat

		#Method1 : Use A the same as Feature Matrix
		# for row in feature_mat:
		# 	A.append(feature_mat[row])
		
		#Method2 : Use tf-idf to initialize A
		A = numpy.zeros((len(feature_mat),i))
		print A.shape
		i=0
		for row in feature_mat:
			count = count_term_in_dictionary(feature_mat,row);
			number_of_sentences = A.shape[1]+0.0
			# print count_term_in_dictionary,count,number_of_sentences/(1+count),'------------------'
			idf = math.log(number_of_sentences/(1+count));
			j=0
			for score in feature_mat[row]:
				sentence_tokens = tokenize_and_clean(sentences[j])
				tf = score/len(sentence_tokens);
				A[i][j] = (tf*idf);
				j = j+1
			i=i+1

		#select sentences of maximum each term for matrix U
		#if number of term is equal, count for other keywords.
		#if they are still equal, choose longest sentence.
		#term feature i, sentence j
		key_use = []
		U_list = list();
		term_sum = numpy.sum(A,axis=0)
		for i in range(0,len(A)):
			sen = 0 #selected sentece
			max_i_term = 0 #maximum of term in the selected sentence
			max_terms = 0 #maximum of all feature terms
			max_len = 0 #length of selected sentece
			for j in range(0,len(A[i])):
				if A[i][j] > max_i_term:
					max_i_term = A[i][j]
					sen = j

			if max_i_term == 0:
				sen = -1
			if sen != -1:
				key_use.append(key_list[i])
			if sen not in U_list:
				U_list.append(sen)

		A = numpy.mat(A)
		print 'A',A.shape
		AT = A.T
		
		# U_list = (list(set(U_list)))
		for u in U_list:
			if(u != -1):
				U.append(AT[u].tolist()[0])

		U = numpy.mat(U)
		U = U.T

		U = normalize(U, norm='l1', axis=1)

		a1 = numpy.dot(U.T,U)
		a1 = numpy.mat(a1)

		print 'a1',a1.shape
		
		#make V: sentence-topic matrix

		try:
			a1_inv = a1.I
		except:
			a1_inv = numpy.linalg.pinv(a1)
			continue
			print 'xxx'

		print 'ai',a1_inv.shape
		print 'U',U.shape
		print 'A',A.shape

		# V = (a1).I*U.T*A 
		V = a1_inv*U.T*A
		#****change to what I think it should be for calculating******
		V = V.T

		print 'U',U.shape
		print 'V',V.shape

		is_converge = False
		lim = 0;
		while (not is_converge) and (lim < LIMIT):
		# for i in range(0,10):
			is_converge = True
			a1 = A*V
			a2 = U*V.T*V;
			b1 = A.T*U
			b2 = V*U.T*U
			U_tmp = U #make temporary U for calculation and converge check
			for i in range(0,U.shape[0]):
				for j in range(0,U.shape[1]):
					U_ij = U.item(i,j)
					a1_ij = a1.item(i,j)
					a2_ij = a2.item(i,j)
					if(a2_ij != 0):
						U_tmp.itemset((i,j),U_ij*a1_ij/a2_ij)

			for i in range(0,V.shape[0]):
				for j in range(0,V.shape[1]):
					V_ij = V.item(i,j)
					b1_ij = b1.item(i,j)
					b2_ij = b2.item(i,j)
					if(b2_ij != 0):
						V.itemset((i,j),V_ij*b1_ij/b2_ij)

			U_tmp = normalize(U_tmp, norm='l1', axis=1)
			#check if converge
			for i in range(0,U.shape[0]):
				for j in range(0,U.shape[1]):
					if(abs(U[i][j]-U_tmp[i][j])>EPSILON):
							is_converge = False
			U = U_tmp
			lim = lim+1
		#end while not is_converge

# 		VT = V.T
		#VT : topic-sentence matrix
# 		V_list = list()
# 		for i in range(0,VT.shape[0]):
# 			max_sen = 0
# 			sen = 0
# 			VT_list = VT[i].tolist()[0]
# 			for j in range(0,len(VT_list)):
# 				if(VT_list[j] > max_sen):
# 					max_sen = VT_list[j]
# 					sen = j
# 			# print "V[sen]",V[sen]
# 			V_list.append((sen,max_sen,V[sen].sum()))

		# print VT
	
	
		V_list = createVlist(V)	
		j=0
		for i in V_list:
			print i
			# t is topic
			summary[t].append(sentences[i[0]])
			# print V[i]
			j = j+1
			if(j>=20):
				break;
		
		
# 		print V_list;
		# print V
		# print key_use
		columnlist = set()
		for i in range (0,3):
			row = V_list[i][0]
# 			print V[row]
			for j in range(0,V.shape[1]):
				if(V.item((row,j))>0):
					columnlist.add(j);
		newV = cutMatrix(V, list(columnlist))
		
		V_list2 = createVlist(newV)
		
		j=0

		for i in V_list2:
			# t is topic
			summary2[t].append(sentences[i[0]])
			# print V[i]
			j = j+1
			if(j>=20):
				break;

		# sys.exit(1)
		summaryFinalTemp = set()
		for i in range(0,5):
			summaryFinalTemp.add(summary[t][i])
# 			print summary[t][i]
		print "\t\tsummary2"	
		
		for i in range(0,10):
			if(len(summaryFinalTemp)==10 ):
				break
			summaryFinalTemp.add(summary2[t][i])
# 			print summary[t][i]
# 		print summaryFinalTemp	
		summaryFinal[t].extend(list(summaryFinalTemp))	
		print '-------------------------------------------------------'
		
	json_summary = 'exampleSummary/summary_1.json';
	with open(json_summary,'a') as fp:
		print 'summary1'
# 		print summary
# 		json.dump(summary,fp,indent=4)
		print "===========TOPIC=============",t
		# print V_list
	
	json_summary = 'exampleSummary/summary_2.json';
	with open(json_summary,'a') as fp:
		print 'summary2'
# 		print summary
		json.dump(summary2,fp,indent=4)
# 		SUMMARY_COLLECTION.update({"_id": summary["_id"]},summary,upsert=True)
	
	json_summary = 'exampleSummary/summary_Final.json';
	with open(json_summary,'a') as fp:
		print 'summaryFinal !!!!'
# 		print summaryFinal
		json.dump(summaryFinal,fp,indent=4)
		SUMMARY_COLLECTION.update({"_id": summary["_id"]},summaryFinal,upsert=True)
	
	# break
#end for json_dir
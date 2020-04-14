# -*- coding: utf-8 -*-
import urllib, urllib2, json, re, datetime, sys, cookielib
import sys,getopt,datetime,codecs
from nltk.corpus import stopwords
from .. import models
from textblob import TextBlob as tb #NLP module
from pyquery import PyQuery
import pandas as pd
from unicodedata import normalize
import csv
import pandas as pd
from fuzzywuzzy import process
from fuzzywuzzy import fuzz 


palavras_chave_contexto_inicio = ["start", "adapt", "begin"]
palavras_chave_contexto_meio = ["years", "many years"]
palavras_chave_contexto_pregnancy= ["pregnancy"]
palavras_chave_contexto_desmame = ["withdraw", "stop"]

palavras_chave_estudo = ["article", "study", "comparison"]
palavras_chave_opiniao = ["I", "me", "my"]
palavras_chave_opiniao_espanhol = ["tengo", "mio", "y"]
palavras_chave_especialista = ["http", "https", "www", "pic" , "tipica", "html", "ssri"]
palavras_chave_propaganda = ["facebook", "twitter","video", "youtube", "buy", "help"]
palavras_chave_pedido = ["need", "ask", "please", "thanks", "?"]
palavras_chave_pedido_espanhol = ["solicito", "pedido", "favor", "gracia", "?"]
 
#
palavras_fora = ["pic", "tic", "scar", "anger", "Tic", "Pic", "Scar", "Anger"]

lista_medicamentos_covid = pd.read_csv('Drug_ADR.csv')

lista_medicamentos = pd.read_csv('Drug_ADR - Copia backup 12042020.csv')
#  
lista_sintomas = pd.read_csv('ADR_DRUG.csv')
#
lista_doencas = pd.read_csv('arqdoencasCOVID.csv')

lista_sintomas_covid = pd.read_csv('sintomasCOVID.csv')

class Tweet:
	
	
	def __init__(self):
		pass


def clean_tweet(tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\/\/\S+)", " ", tweet).split())
		

class sintomas():
	def __init__(self, sintoma):
		self.sintoma = sintoma
#

class argumento():

	def __init__(self, querySearch):
		self.argumento = querySearch
	
class TweetManager:
	
		
	def __init__(self):
		pass
#
	@staticmethod

	def getTweets(tweetCriteria, receiveBuffer=None, bufferLength=800, proxy=None):
		refreshCursor = ''
		contdup = 0
		aceitos = []
		aceitostxt = []
		results = []
		resultsAux = []
		cookieJar = cookielib.CookieJar()

		if hasattr(tweetCriteria, 'username') and (
				tweetCriteria.username.startswith("\'") or tweetCriteria.username.startswith("\"")) and (
				tweetCriteria.username.endswith("\'") or tweetCriteria.username.endswith("\"")):
			tweetCriteria.username = tweetCriteria.username[1:-1]

		active = True
		argumento = tweetCriteria.querySearch

		while active:
			json = TweetManager.getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy)
			print ('passou do 1o break')
			print (len(json['items_html'].strip())) 
			
			if len(json['items_html'].strip()) == 0:
				break

			refreshCursor = json['min_position']
			scrapedTweets = PyQuery(json['items_html'])
			# Remove incomplete tweets withheld by Twitter Guidelines
			scrapedTweets.remove('div.withheld-tweet')
			tweets = scrapedTweets('div.js-stream-tweet')
			
			print (len(tweets)) 
			
			if len(tweets) == 0:
				break
			print ('passou do 1o break')
			for tweetHTML in tweets:
				tweetPQ = PyQuery(tweetHTML)
				tweet = Tweet()

				usernameTweet = tweetPQ("span:first.username.u-dir b").text()
				txt = ' '
				txtorig = ' ' 
				txtorig = txt
				txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', ' ').replace('@ ', ' ').replace(', ', ' ')).encode('utf-8')
				txtorig = txt
				letters_only = re.sub("[^a-zA-Z]", " ",str(txt))
				vocabulos= letters_only.lower().split()                             
				irrelevantes  = set(stopwords.words("english"))                  
				palavras_relevantes = [w for w in vocabulos if not w in irrelevantes ] 
				txt_class =  " ".join(palavras_relevantes)

					
				retweets = str(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr(
					"data-tweet-stat-count").replace(",", ""))
				favorites = str(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr(
					"data-tweet-stat-count").replace(",", ""))
				dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"))
				id = ' '
				id = tweetPQ.attr("data-tweet-id")
				permalink = tweetPQ.attr("data-permalink-path")
			
				tweet.id = id
				tweet.username = usernameTweet
				tweet.text = txtorig
				tweet.text_class = txt_class
				indice = 0
 
	 
				geo = ''
				geoSpan = tweetPQ('span.Tweet-geo')
				if len(geoSpan) > 0:
					geo = geoSpan.attr('title')
				tweet.med1 = ''
				tweet.med2 = ''
				tweet.med3 = ''
				achou0 = 0
				indice = 0
			
		
				while indice < len(lista_medicamentos_covid) and achou0 <4:
	 							   
					if lista_medicamentos_covid.DRUG_NAME[indice].lower() in txt.lower():
						achou0 = achou0 + 1
						if achou0 == 1:
							tweet.med1 = lista_medicamentos_covid.DRUG_NAME[indice]
#							print ('caso1 -> ' , lista_medicamentos.DRUG_NAME[indice])
						elif achou0 == 2:
							tweet.med2 = lista_medicamentos_covid.DRUG_NAME[indice]
#							print ('caso2 -> ' , lista_medicamentos.DRUG_NAME[indice])
						elif achou0 == 3:
							tweet.med3 = lista_medicamentos_covid.DRUG_NAME[indice]
#							print ('caso3 -> ' , lista_medicamentos.DRUG_NAME[indice])
					indice = indice + 1
#   
				tweet.sin1 = ''
				tweet.sin2 = ''
				tweet.sin3 = ''
				indice = 0
				achousc = 0
				indice = 0
			 
				while indice < len(lista_sintomas_covid) and achousc <4:
				
#				   print ('drug -> ' , lista_medicamentos.DRUG_NAME[indice].lower())
								   
				   if lista_sintomas_covid.sintomaCOVID[indice].lower() in txt.lower():
						achousc = achou0 + 1
						if achousc == 1:
							tweet.sin1 = lista_sintomas_covid.sintomaCOVID[indice]
#							print ('caso1 -> ' , lista_medicamentos.DRUG_NAME[indice])
						elif achousc == 2:
							tweet.sin2 = lista_sintomas_covid.sintomaCOVID[indice]
#							print ('caso2 -> ' , lista_medicamentos.DRUG_NAME[indice])
						elif achousc == 3:
							tweet.sin3 = lista_sintomas_covid.sintomaCOVID[indice]
#							print ('caso3 -> ' , lista_medicamentos.DRUG_NAME[indice])
				   indice = indice + 1
				tweet.doe1 = ''
				tweet.doe2 = ''
				tweet.doe3 = ''
				indice = 0
				achou2 = 0
				 
				while indice < len(lista_doencas) and achou2 < 4:
					if lista_doencas.doenca[indice].lower() in txt.lower():
						achou2 = achou2 + 1
						if achou2 == 1:
				  			tweet.doe1 = lista_doencas.doenca[indice]
						elif achou2 == 2:
							tweet.doe2 = lista_doencas.doenca[indice]
						elif achou2 == 3:
							tweet.doe3 = lista_doencas.doenca[indice]
					indice = indice + 1

				indice = 0
				achou1 = 0
	 				   				
				 
				
#   Fazendo analise de sentimento pelo TextBlob
#
				tweet.aval = ' '	
				tweet.aval_class = ' '
				tweet.argumento = tweetCriteria.querySearch
				analysis = None
			 
				analysis = tb(clean_tweet(txt))
				if analysis.sentiment.polarity > 0.0:
					tweet.aval = "Positivo"
				else:
					if analysis.sentiment.polarity < 0.0:
						tweet.aval = "Negativo"
					else:
						tweet.aval = "Neutro"

				tweet.nota = analysis.sentiment.polarity
				
				analysis = tb(clean_tweet(txt_class))
				if analysis.sentiment.polarity > 0.0:
					tweet.aval_class = "Positivo"
				else:
					if analysis.sentiment.polarity < 0.0:
						tweet.aval_class = "Negativo"
					else:
						tweet.aval_class = "Neutro"

				tweet.nota_class = analysis.sentiment.polarity
#
# definindo os dominios de credibilidade e contexto
#
			  
				fopiniao = "False" 
					
				for i in range (len(palavras_chave_opiniao)):
					if palavras_chave_opiniao[i].lower() in tweet.text.lower():
					   fopiniao = "True"
					   break
				for i in range  (len(palavras_chave_opiniao_espanhol)):
					if palavras_chave_opiniao_espanhol[i].lower() in tweet.text.lower():
					   fopiniao = "True"
					   break
				festudo = "False"
				for i in range (len(palavras_chave_estudo)):
					if palavras_chave_estudo[i].lower() in tweet.text.lower():
					   festudo = "True"
					   break
				fespecialista = "False"
				
				for i in range (len(palavras_chave_especialista)):
					if palavras_chave_especialista[i].lower() in tweet.text.lower():
					   fespecialista = "True"
					   break
			
				fpropaganda = "False"		
				
				for i in range (len(palavras_chave_propaganda)):
					if palavras_chave_propaganda[i].lower() in tweet.text.lower():
					   fpropaganda = "True"
					   break
		 
				fpedido = "False"		
				
				for i in range (len(palavras_chave_pedido)):
					if palavras_chave_pedido[i].lower() in tweet.text.lower():
					   fpedido = "True"
					   break
					
				for i in range (len(palavras_chave_pedido_espanhol)):
					if palavras_chave_pedido_espanhol[i].lower() in tweet.text.lower():
					   fpedido = "True"
					   break
#
# atribuindo valores defaults
#					   
				credibilidade = "propaganda"
				contexto = "meio"
				 
			 
				if fpropaganda == "True":
				    credibilidade = 'propaganda'
				elif fespecialista == "True":
				   credibilidade = "especialista"
				elif festudo == "True":
				   credibilidade = "study" 
				elif  fopiniao == "True":
				   credibilidade = "opinion"
				elif fpedido == "True":
				   credibilidade = "pedido" 
				finicio = "False"
				fmeio = "False"
				if finicio == "True":
				   contexto = "inicio"
				elif fmeio == "True":
				   contexto = "meio"
	 				   
				tweet.datatw = datetime.datetime.fromtimestamp(dateSec)
				tweet.horatw = datetime.datetime.fromtimestamp(dateSec)
				## tweet.horatw = datetime.datetime.fromtimestamp(dateSec)
				tweet.retweets = retweets
				tweet.favorites = favorites
	#			tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))
	#			tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))
	#			tweet.geo = geo
				
				
				tweet.credibilidade = credibilidade
				tweet.contexto = contexto
			 					
				
				if tweet.text == " ":
				   continue
   
				aceitos.append(tweet.id)
				aceitostxt.append(tweet.text)
				results.append(tweet)
				resultsAux.append(tweet)

				if receiveBuffer and len(resultsAux) >= bufferLength:
					receiveBuffer(resultsAux)
					resultsAux = []

				if tweetCriteria.maxTweets > 0 and len(results) >= tweetCriteria.maxTweets:
					active = False
					break

			if receiveBuffer and len(resultsAux) > 0:
				receiveBuffer(resultsAux)

		return results

	@staticmethod

	def getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy):
		url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"

		urlGetData = ''

		if hasattr(tweetCriteria, 'username'):
			urlGetData += ' from:' + tweetCriteria.username

		if hasattr(tweetCriteria, 'querySearch'):
			urlGetData += ' ' + tweetCriteria.querySearch

		if hasattr(tweetCriteria, 'near'):
			urlGetData += "&near:" + tweetCriteria.near + " within:" + tweetCriteria.within

		if hasattr(tweetCriteria, 'since'):
			urlGetData += ' since:' + tweetCriteria.since

		if hasattr(tweetCriteria, 'until'):
			urlGetData += ' until:' + tweetCriteria.until

		if hasattr(tweetCriteria, 'topTweets'):
			if tweetCriteria.topTweets:
				url = "https://twitter.com/i/search/timeline?q=%s&src=typd&max_position=%s"

		url = url % (urllib.quote(urlGetData), urllib.quote(refreshCursor))

		headers = [
			('Host', "twitter.com"),
			('User-Agent',
			 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"),
			('Accept', "application/json, text/javascript, */*; q=0.01"),
			('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
			('X-Requested-With', "XMLHttpRequest"),
			('Referer', url),
			('Connection', "keep-alive")
		]

		if proxy:
			opener = urllib2.build_opener(urllib2.ProxyHandler({'http': proxy, 'https': proxy}),
										  urllib2.HTTPCookieProcessor(cookieJar))
		else:
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		opener.addheaders = headers

		try:
			response = opener.open(url)
			jsonResponse = response.read()
		except:
			print
			"Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd" % urllib.quote(
				urlGetData)
			sys.exit()
			return

		dataJson = json.loads(jsonResponse)

		return dataJson
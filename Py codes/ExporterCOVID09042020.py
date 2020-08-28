# -*- coding: utf-8 -*-
import sys,getopt,datetime,codecs
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def main(argv):

	if len(argv) == 0:
		print('You must pass some parameters. Use \"-h\" to help.')
		return

	if len(argv) == 1 and argv[0] == '-h':
		f = open('exporter_help_tex.txt', 'r')
		print f.read()
		f.close()
		return

	arg = " "
	outputFile = " "
	outputFileName = "output2_got.csv"
	
	try:
			opts,args = getopt.getopt(argv, "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output="))
			tweetCriteria = got.manager.TweetCriteria()

			for opt,arg in opts:
					if opt == '--username':
						tweetCriteria.username = arg
					elif opt == '--since':
						tweetCriteria.since = arg
					elif opt == '--until':
						tweetCriteria.until = arg
					elif opt == '--querysearch':
						tweetCriteria.querySearch = arg
					elif opt == '--toptweets':
						tweetCriteria.topTweets = True
					elif opt == '--maxtweets':
						tweetCriteria.maxTweets = int(arg)
					elif opt == '--near':
						tweetCriteria.near = '"' + arg + '"'
					elif opt == '--within':
						tweetCriteria.within = '"' + arg + '"'
					elif opt == '--within':
						tweetCriteria.within = '"' + arg + '"'
					elif opt == '--output':
						outputFileName = arg
				
			outputFile = codecs.open(outputFileName, "w+", "utf-8")
			 
			outputFile.write('username;datatw;horatw;retweets;favorites;text;text_class;id;med1;med2;med3;sin1;sin2;sin3;aval;nota;aval_class;nota_class;argumento;doe1;doe2;doe3;credibilidade;contexto')
 
			
			print('Searching...\n')
			

			def receiveBuffer(tweets):
				print('tweets ')
				print len(tweets)
				for t in tweets:
				   
				   
 				   outputFile.write(('\n%s;"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s"' % (t.username,t.datatw.strftime ("%d/%m/%Y"),t.horatw.strftime ("%H:%M"),t.retweets,t.favorites,t.text_class,t.text_class,t.id,t.med1,t.med2,t.med3,t.sin1,t.sin2,t.sin3,t.aval,t.nota,t.aval_class,t.nota_class,t.argumento,t.doe1,t.doe2,t.doe3,t.credibilidade,t.contexto)))
					
				   
				outputFile.flush()
				print('More %d saved on file...\n' % len(tweets))

			got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

	except arg:
		print('Arguments parser error, try -h' + arg)
	finally:
   #####    #  		outputFile.close()
		print('Done. Output file generated %s.' % outputFileName)

if __name__ == '__main__':
	main(sys.argv[1:])

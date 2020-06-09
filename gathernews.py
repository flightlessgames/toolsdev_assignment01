import nltk
import newspaper
import datetime
import webbrowser

### ### ### VARIABLES ### ### ###

url1 = 'https://cnn.com/'
url2 = 'https://nytimes.com/'
url3 = 'https://wsj.com/'

news_sources = (url1, url2, url3)
collected_articles = list()
keyworded_articles = list()

save_txt_path = 'news_summary.txt'

### ### ### FUNCTIONS ### ### ###

#transform the source into a newspaper type, then compile each article into the article list,
#proccess is scalable for multiple newspapers by continuing to append to the "collected_articles" list
def scrape(source):
	source_paper = newspaper.build(source, memoize_articles=False)
	print("scrape size: " + str(source_paper.size()))
	for article in source_paper.articles:
		collected_articles.append(article)

#possibly start here, simply GO-TO scrape for each source in list
def scrape_list(sources):
	newspapers = list()
	for source in sources:
		scrape(source)

###	###	###	### RUNTIME ### ### ### ###

#start here, select a news source
selector = input('Choose a News Source: [CNN]; [New York Times]; [Wall Street Journal]; [All] ')

if selector.lower() in ('cnn', 'cable news network'):
	#parse our url1
	print('You have selected: CNN. ')
	scrape(url1)
elif selector.lower() in ('nyt', 'nytimes', 'new york times', 'the times'):
	#parse out url2
	print('You have selected: NEW YORK TIMES. ')
	scrape(url2)
elif selector.lower() in ('wsj', 'wall street journal'):
	#parse out url3
	print('You have selected: WALL STREET JOURNAL. ')
	scrape(url3)
else:
	#display "error", parse out all 3
	print('Now scraping All available news sources...')
	scrape_list(news_sources)

#after master list of articles is compiled, ask for a keyword sort
#TODO? make the keyword filter before the master compile to save on resources at runtime??
keyword = input('Would you like to narrow your search by entering a Keyword?\n[HIT ENTER TO NOT USE A KEYWORD] ')

#create a second list for keyworded articles
for article in collected_articles:
	if keyword in article.url:
		keyworded_articles.append(article)

print("Found " + str(len(keyworded_articles)) + " articles")

#begin the proccess of writing all found articles onto a .txt file
writer = open(save_txt_path, 'w', encoding="utf-8") #encoding fixes bug issues

#fun little bonus extra feature #1
writer.write('==== Entry Date: ' + str(datetime.datetime.now()) + ' ====\n')


for article in keyworded_articles:	
	#some links are defunct and lead to 404 errors, use try/catch to eliminate bad links
	try: 
		article.download()
		article.parse()
	except:
		continue
	#.txt formatting: "title" - "authors" \n "summary" \n\n
	writer.write('\n' + str(article.title))
	writer.write(' - ')

	for author in article.authors:
		if author != article.authors[0]:
			writer.write(', ')
	
		writer.write(str(author))
	
	article.nlp()
	writer.write('\n' + article.summary + '\n')

writer.close()

#bonus feature #2, open articles on webapp
open_articles = input('Do you want to open all ' + str(len(keyworded_articles)) + ' articles on the web?\n[Y] OPEN; [N] DO NOT OPEN; ')

if open_articles.lower() in ('y', 'yes', 'confirm'):
	#open first article as a new browser window, pop into focus
	webbrowser.open(collected_articles[0].url, new=1, autoraise=True)
	for num in range(1, len(keyworded_articles)-1):
		#open subsequent articles as new tabs on the window
		webbrowser.open(collected_articles[num].url, new=2)
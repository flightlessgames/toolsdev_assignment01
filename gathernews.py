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
selector = input('Choose a News Source: "CNN", "New York Times", or "Wall Street Journal", or select "All" ')

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
	#display error, parse out all 3
	print('Now scraping All available news sources...')
	scrape_list(news_sources)

#after master list of articles is compiled, as for a keyword sort
#TODO? make this before the master compile to save on resources at runtime?
keyword = input('Would you like to narrow your search by entering a Keyword?\nHIT ENTER TO NOT USE A KEYWORD] ')

counter = 0

for article in collected_articles:
	if keyword in article.url:
		keyworded_articles.append(article)
		counter = counter + 1

print("Found " + str(counter) + " articles")

writer = open(save_txt_path, 'w', encoding="utf-8")

writer.write('==== Entry Date: ' + str(datetime.datetime.now()) + ' ====\n')

for article in keyworded_articles:
	
	try: #some links are defunct and lead to 404 errors, use try/catch to eliminate bad links
		article.download()
		article.parse()
	except:
		continue

	writer.write('\n' + str(article.title))
	writer.write(' - ')

	for author in article.authors:
		if author != article.authors[0]:
			writer.write(', ')
	
		writer.write(str(author))
	
	article.nlp()
	writer.write('\n' + article.summary + '\n')

writer.close()

open_articles = input('Do you want to open all ' + str(counter) + ' articles on the web?\n[Y] OPEN; [N] DO NOT OPEN; ')

if open_articles.lower() in ('y', 'yes', 'confirm'):
	#open first article as a new browser window
	webbrowser.open(collected_articles[0].url, new=1)
	for num in range(1, counter-1):
		#open subsequent articles as new tabs on the window
		webbrowser.open(collected_articles[num].url, new=2)
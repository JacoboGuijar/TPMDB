import random
import requests
from bs4 import BeautifulSoup
import time
import json
import tmdbsimple as tmdb

tmdb.API_KEY = ''#INSERT YOUR TMDB API KEY
SITE = 'https://letterboxd.com/' #The site we are scraping from
SAVED_MOVIES = 'downloaded_movies.txt' #File to write a movie after it has being downloaded

def get_image(ids, url):
	#https://stackoverflow.com/questions/34692009/download-image-from-url-using-python-urllib-but-receiving-http-error-403-forbid
	opener = urllib.request.build_opener()
	opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
	urllib.request.install_opener(opener)

	urllib.request.urlretrieve(url, PATH+ids+url[-4:])

def get_poster(tmdb_url):
	#We will pick the highest voted poster if exists
	try:
		tmdb_id = tmdb_url.replace('https://www.themoviedb.org/movie/','').split('/')[0]
		movie = tmdb.Movies(tmdb_id)
		response = movie.info()
		movie_posters = movie.images()['posters']
		highest_vote = 0.0
		final_poster = None
		for poster in movie_posters:
			if poster['vote_average'] > highest_vote and 'en' in poster['iso_639_1']:
				final_poster = poster 
				highest_vote = poster['vote_average']
		if final_poster == None and len(movie_posters) > 1:
			for poster in movie_posters:
				if poster['vote_average'] > highest_vote:
					final_poster = poster 
					highest_vote = poster['vote_average']
		elif final_poster == None and len(movie_posters) == 1:
			final_poster = movie_posters[0]

		final_poster_url = 'https://www.themoviedb.org/t/p/original' + final_poster['file_path']
	except requests.exceptions.HTTPError:
		final_poster_url = None
	return final_poster_url

def movie_not_saved(movie):
#Check if a movie hasn't been already downladed
	not_saved = True
	with open(SAVED_MOVIES, 'r') as f:
		saved_lines = f.readlines()
		for saved_line in saved_lines:
			if movie in saved_line:
				not_saved = False
				break
	return not_saved

def get_movie_info(movie):
#Here is where the magic takes place.
#This simply grabs all the info from the html tags
	info = []

	r = requests.get(SITE + movie)
	bs = BeautifulSoup(r.text, 'lxml')
	try:
		title = 'title : {} : {}'.format(bs.find('h1', {'class':'headline-1 js-widont prettify'}).text, movie.split('/')[-2])
		info.append('{}'.format(title))
	except AttributeError:
		title = '??;;NO??;;TITLE??;;'
		info.append('{}'.format(title))
	if title != '??;;NO??;;TITLE??;;':
		try:
			year = bs.find('small', {'class':'number'})
			info.append('year : {}'.format(year.a.text))
		except AttributeError:
			year = 0
			year = bs.find('small', {'class':'number'})
			info.append('year : {}'.format(year))

		if bs.find('p', {'class':'text-link text-footer'}) != None:
			time = bs.find('p', {'class':'text-link text-footer'}).text.replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').split(' ')[0]
			if time != 'More':
				info.append('time : {}'.format(time))
			else:
				time = None 
				info.append('time : {}'.format(time))

		
		if bs.find('a', {'data-id':'cast'}) != None:
			cast = bs.find_all('a', {'class':'text-slug tooltip'})
			for actor in cast:
				try:
					info.append('{} : {} : {}'.format(actor.text, actor['title'], actor['href'].split('/')[-2]))
				except KeyError:
					info.append('{} : {} : {}'.format(actor.text, actor['href'], actor['href'].split('/')[-2]))

		if bs.find('a', {'data-id':'crew'}) != None:
			crew_bs = bs.find('div', {'id':'tab-crew'})
			jobs = crew_bs.find_all('a', {'class':'text-slug'})
			for job in jobs:
				info.append('{} : {} : {}'.format(job['href'].split('/')[1], job.text, job['href'].split('/')[-2]))

		if bs.find('a', {'data-id':'details'}) != None:
			details_bs = bs.find('div', {'id':'tab-details'})
			details = details_bs.find_all('a', {'class':'text-slug'})
			for detail in details:
				if detail['href'].split('/')[1] == 'films':
					info.append('{} : {} : {}'.format(detail['href'].split('/')[2], detail.text, detail['href'].split('/')[-2]))
				else:
					info.append('{} : {} : {}'.format(detail['href'].split('/')[1], detail.text, detail['href'].split('/')[-2]))

			if details_bs.find('div', {'class':'text-indentedlist'}) != None:
				lenguages = details_bs.find('div', {'class':'text-indentedlist'})
				info.append('Other lenguages : {}'.format(lenguages.text.replace('\t', '').replace('\n', '')))

		if bs.find('a', {'data-id':'genres'}) != None:
			genres_bs = bs.find('div', {'id':'tab-genres'})
			genres = genres_bs.find_all('a', {'class':'text-slug'})
			for genre in genres:
				info.append('{} : {} : {}'.format(genre['href'].split('/')[2], genre.text, genre['href'].split('/')[-2]))

		if bs.find('h4', {'class':'tagline'}) != None:
			tagline = bs.find('h4', {'class':'tagline'})
			info.append('tagline : {}'.format(tagline.text))
		if bs.find('div', {'class':'truncate'}) != None:
			synopsis = bs.find('div', {'class':'truncate'})
			info.append('synopsis : {}'.format(synopsis.text).replace('\n',''))

		try:
			tmdb_url = bs.find('a', {'data-track-action':'TMDb'})['href']
			poster_url = get_poster(tmdb_url)
		except TypeError:
			poster_url = None
		info.append('poster_url : {}'.format(poster_url))
		
		stats_url = SITE + 'esi/' + movie + 'stats/'
		r = requests.get(stats_url)
		bs2 = BeautifulSoup(r.text, 'lxml')
		try:
			members = bs2.find('a', {'href': '/' + movie + 'members/'})['title'].split(' ')[-1].replace(u'\xa0', ' ').split(' ')[0]
			lists = bs2.find('a', {'href': '/' + movie + 'lists/by/popular/'})['title'].split(' ')[-1].replace(u'\xa0', ' ').split(' ')[0]
			likes = bs2.find('a', {'href': '/' + movie + 'likes/'})['title'].split(' ')[-1].replace(u'\xa0', ' ').split(' ')[0]
		except TypeError:
			movie = 'film/' + bs.find('meta', {'name':'twitter:url'})['content'].split('/')[-2] + '/'
			members = bs2.find('a', {'href': '/' + movie + 'members/'})['title'].split(' ')[-1].replace(u'\xa0', ' ').split(' ')[0]
			lists = bs2.find('a', {'href': '/' + movie + 'lists/by/popular/'})['title'].split(' ')[-1].replace(u'\xa0', ' ').split(' ')[0]
			likes = bs2.find('a', {'href': '/' + movie + 'likes/'})['title'].split(' ')[-1].replace(u'\xa0', ' ').split(' ')[0]
		info.append('members : {}'.format(members))
		info.append('lists : {}'.format(lists))
		info.append('likes : {}'.format(likes))
		
		ratings_url = SITE + 'csi/' + movie + 'rating-histogram/'
		r = requests.get(ratings_url)
		bs = BeautifulSoup(r.text, 'lxml')

		if bs.find('a', {'href':'/' + movie + 'ratings/', 'class':'tooltip display-rating'}) != None:
			rating = bs.find('a', {'href':'/' + movie + 'ratings/', 'class':'tooltip display-rating'})['title'].split(' ')[3]
		elif bs.find('a', {'href':'/' + movie + 'ratings/', 'class':'tooltip display-rating -highlight'}) != None:
			rating = bs.find('a', {'href':'/' + movie + 'ratings/', 'class':'tooltip display-rating -highlight'})['title'].split(' ')[3]
		else:
			rating = None
		info.append('rating : {}'.format(rating))
	else:
		info = None
	return info


#Here is where the code begins
#Remember to run this program you need the following files and empty folder:
#movies_one_line.txt, downloaded_movies.txt and movies_txt/
lines = []
#movies_one_line.txt is the file where all the non downloaded movies are
with open('movies_one_line.txt', 'r') as f:
	for line in f:
		lines.append(line.replace('\n',''))

movies = lines[0].split(';')

#This loop simply runs the function movie_not_saved(movie) but with a few security meassures
#Just in case letterboxd decides you can access their web anymore.
for movie in movies:
	if movie_not_saved(movie) == True:
		try:
			print(movie)
			info = get_movie_info(movie)
			
		except requests.exceptions.ConnectionError:
			time.sleep(60)
			try:
				info = get_movie_info(movie)
				
			except requests.exceptions.ConnectionError:
				time.sleep(300)
				try:
					info = get_movie_info(movie)
					time.sleep(0.5)
				except requests.exceptions.ConnectionError:
					time.sleep(600)
					try:
						info = get_movie_info(movie)
						time.sleep(0.5)
					except requests.exceptions.ConnectionError:
						time.sleep(1200)
						info = []

		except requests.exceptions.Timeout:
			time.sleep(60)
			try:
				info = get_movie_info(movie)
				
			except requests.exceptions.Timeout:
				time.sleep(300)
				try:
					info = get_movie_info(movie)
					time.sleep(0.5)
				except requests.exceptions.Timeout:
					time.sleep(600)
					try:
						info = get_movie_info(movie)
						time.sleep(0.5)
					except requests.exceptions.Timeout:
						time.sleep(1200)
						info = []

		if info != None:
			with open('movies_txt/' + movie.split('/')[-2] + '.txt', 'wb+') as f: 
				for detail in info:
					f.write((detail + '\n').encode('utf-8'))

		with open(SAVED_MOVIES, 'a') as f:
			f.write(movie + '\n')

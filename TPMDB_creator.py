import sqlite3
import os
import extract_info_from_txt_files
import random
from operator import itemgetter

MOVIES_TXT_FOLDER = ''#Insert the folder where you have saved all your txt files.

def create_database():
	conn = sqlite3.connect('movie_db_13_10_2021_1_no_jobs.db')
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS movies (
			  title_url text PRIMARY KEY,
			  title text, 
			  year integer,
			  lenght integer,
			  tagline text,
			  synopsis text,
			  poster_url text,
			  members integer,
			  lists integer,
			  likes integer,
			  rating real
			  )""")

	c.execute("""CREATE TABLE IF NOT EXISTS crew (
			  name_url text PRIMARY KEY,
			  name text
			  )""")

	c.execute("""CREATE TABLE IF NOT EXISTS crew_movie_relation (
			  title_url text,
			  name_url text,
			  job text
			  )""")

	c.execute("""CREATE TABLE IF NOT EXISTS cast (
			  name_url text PRIMARY KEY,
			  name text
			  )""")

	c.execute("""CREATE TABLE IF NOT EXISTS cast_movie_relation (
			  title_url text,
			  name_url text,
			  character text
			  )""")

	c.execute("""CREATE TABLE IF NOT EXISTS genre (
			  genre_url text PRIMARY KEY,
			  genre text
			  )""")

	c.execute("""CREATE TABLE IF NOT EXISTS genre_movie_relation (
			  title_url text,
			  genre_url text
			  )""")

	c.execute("""CREATE TABLE IF NOT EXISTS studio (
			  studio_url text PRIMARY KEY,
			  studio text
			  )""")

	c.execute("""CREATE TABLE IF NOT EXISTS studio_movie_relation (
			  title_url text,
			  studio_url text
			  )""")

	c.execute("""CREATE TABLE IF NOT EXISTS language (
			  language_url text PRIMARY KEY,
			  language text
			  )""")

	c.execute("""CREATE TABLE IF NOT EXISTS language_movie_relation (
			  title_url text,
			  language_url text
			  )""")

	c.execute("""CREATE TABLE IF NOT EXISTS country (
			  country_url text PRIMARY KEY,
			  country text
			  )""")

	c.execute("""CREATE TABLE IF NOT EXISTS country_movie_relation (
			  title_url text,
			  country_url text
			  )""")

	conn.commit()
	conn.close()

def write_in_database():
	create_database()

	conn = sqlite3.connect('movie_db_13_10_2021_1_no_jobs.db')
	c = conn.cursor()

	sample = os.listdir(MOVIES_TXT_FOLDER)
	n = 0
	for file in sample:
		info = extract_info_from_txt_files.get_info_from_file(file)
		
		c.execute("""INSERT INTO movies VALUES (
				  :title_url, :title, :year, :length, :tagline, :synopsis, 
	       		  :poster_url, :members, :lists, :likes, :rating)""", info)
		
		for human in info['crew']:
			c.execute("INSERT or IGNORE INTO crew VALUES(:name_url, :name)", {'name_url':human['name_url'].split('/')[-1], 'name':human['name']})
			c.execute("""INSERT INTO crew_movie_relation VALUES(
				      :title_url, :name_url, :job)""", 
				      {'title_url':info['title_url'], 'name_url':human['name_url'].split('/')[-1], 'job':human['job']})
		
		for human in info['cast']:
			c.execute("INSERT or IGNORE INTO cast VALUES(:name_url, :name)", {'name_url':human['name_url'], 'name':human['name']})

			for character in human['characters']:
				c.execute("""INSERT INTO cast_movie_relation VALUES(
					      :title_url, :name_url, :character)""", 
					      {'title_url':info['title_url'], 'name_url':human['name_url'], 'character':character})
		
		for genre in info['genre']:
			c.execute("INSERT or IGNORE INTO genre VALUES(:genre_url, :genre)", genre)
			c.execute("INSERT INTO genre_movie_relation VALUES (:title_url, :genre_url)", {'title_url': info['title_url'], 'genre_url':genre['genre_url']})

		for studio in info['studio']:
			c.execute("INSERT or IGNORE INTO studio VALUES(:studio_url, :studio)", studio)
			c.execute("INSERT INTO studio_movie_relation VALUES (:title_url, :studio_url)", {'title_url': info['title_url'], 'studio_url':studio['studio_url']})

		for language in info['language']:
			c.execute("INSERT or IGNORE INTO language VALUES(:language_url, :language)", language)
			c.execute("INSERT INTO language_movie_relation VALUES (:title_url, :language_url)", {'title_url': info['title_url'], 'language_url':language['language_url']})

		for country in info['country']:
			c.execute("INSERT or IGNORE INTO country VALUES(:country_url, :country)", country)
			c.execute("INSERT INTO country_movie_relation VALUES (:title_url, :country_url)", {'title_url': info['title_url'], 'country_url':country['country_url']})

		n+=1
		if n % 1000 == 0:
			print(n)
			conn.commit()

	conn.commit()
	conn.close()

	
def main():
	write_in_database()

if __name__ == "__main__":
	main()
import sqlite3
import os 
import random

MOVIES_TXT_FOLDER = ''#Insert the folder where you have saved all your txt files.

def get_files_array():
	return os.listdir(MOVIES_TXT_FOLDER)

def get_info_from_file(file):
	
	movie_dict = {'title': None,
				  'title_url': None,
				  'year': None,
				  'length': None,
				  'crew': [],
				  'cast': [],
				  'studio': [],
				  'country':[],
				  'language':[],
				  'Other languages': None,
				  'genre':[],
				  'tagline':None,
				  'synopsis':None,
				  'poster_url':None,
				  'members': None,
				  'lists': None,
				  'likes': None,
				  'rating':None
				  }
	with open(MOVIES_TXT_FOLDER + file, 'rb') as f:
		for line in f:
			stripped_line = line.decode('utf-8').strip('\n').split(' : ')
			if stripped_line[0] == 'title':
				if len(stripped_line) > 3:
					stripped_line[1:-1] = [' : '.join(stripped_line[1:-1])]
					title = stripped_line[1]
				else:
					title = stripped_line[1]
				movie_dict['title'] = title
				movie_dict['title_url'] = stripped_line[-1]
			elif stripped_line[0] == 'year':
				movie_dict['year'] = stripped_line[1]

			elif stripped_line[0] == 'time':
				movie_dict['length'] = stripped_line[1]

			elif stripped_line[0] == 'studio':
				movie_dict['studio'].append({'studio_url':stripped_line[-1], 'studio':stripped_line[1]})

			elif stripped_line[0] == 'country':
				movie_dict['country'].append({'country_url':stripped_line[-1], 'country':stripped_line[1]})

			elif stripped_line[0] == 'language':
				movie_dict['language'].append({'language_url':stripped_line[-1], 'language':stripped_line[1]})

			elif stripped_line[0] == 'Other lenguages':
				movie_dict['Other languages'] = stripped_line[1].split(', ')

			elif stripped_line[0] == 'genre':
				movie_dict['genre'].append({'genre':stripped_line[-1], 'genre_url':stripped_line[1]})

			elif stripped_line[0] == 'tagline':
				movie_dict['tagline'] = stripped_line[1]

			elif stripped_line[0] == 'synopsis':
				movie_dict['synopsis'] = stripped_line[1]

			elif stripped_line[0] == 'poster_url':
				movie_dict['poster_url'] = stripped_line[1]

			elif stripped_line[0] == 'members':
				movie_dict['members'] = stripped_line[1]

			elif stripped_line[0] == 'lists':
				movie_dict['lists'] = stripped_line[1]

			elif stripped_line[0] == 'likes':
				movie_dict['likes'] = stripped_line[1]

			elif stripped_line[0] == 'rating':
				movie_dict['rating'] = stripped_line[1]
			else:
				if stripped_line[0] == 'director':
					movie_dict['crew'].append({'job': 'director', 'name': stripped_line[1], 'name_url' : 'director/'+stripped_line[-1]})

				elif stripped_line[0] == 'co-director':
					movie_dict['crew'].append({'job': 'co-director', 'name': stripped_line[1], 'name_url' : 'co-director/'+stripped_line[-1]})

				elif stripped_line[0] == 'producer':
					movie_dict['crew'].append({'job': 'producer', 'name': stripped_line[1], 'name_url' : 'producer/'+stripped_line[-1]})

				elif stripped_line[0] == 'writer':
					movie_dict['crew'].append({'job': 'writer', 'name': stripped_line[1], 'name_url' : 'writer/'+stripped_line[-1]})

				elif stripped_line[0] == 'editor':
					movie_dict['crew'].append({'job': 'editor', 'name': stripped_line[1], 'name_url' : 'editor/'+stripped_line[-1]})

				elif stripped_line[0] == 'cinematography':
					movie_dict['crew'].append({'job': 'cinematography', 'name': stripped_line[1], 'name_url' : 'cinematography/'+stripped_line[-1]})

				elif stripped_line[0] == 'production-design':
					movie_dict['crew'].append({'job': 'production-design', 'name': stripped_line[1], 'name_url' : 'production-design/'+stripped_line[-1]})

				elif stripped_line[0] == 'art-direction':
					movie_dict['crew'].append({'job': 'art-direction', 'name': stripped_line[1], 'name_url' : 'art-direction/'+stripped_line[-1]})

				elif stripped_line[0] == 'set-decoration':
					movie_dict['crew'].append({'job' : 'set-decoration', 'name' : stripped_line[1], 'name_url' : 'set-decoration/'+stripped_line[-1]})

				elif stripped_line[0] == 'visual-effects':
					movie_dict['crew'].append({'job' : 'visual-effects', 'name' : stripped_line[1], 'name_url' : 'visual-effects/'+stripped_line[-1]})

				elif stripped_line[0] == 'composer':
					movie_dict['crew'].append({'job' : 'composer', 'name' : stripped_line[1], 'name_url' : 'composer/'+stripped_line[-1]})

				elif stripped_line[0] == 'sound':
					movie_dict['crew'].append({'job' : 'sound', 'name' : stripped_line[1], 'name_url' : 'sound/'+stripped_line[-1]})

				elif stripped_line[0] == 'costumes':
					movie_dict['crew'].append({'job' : 'costumes', 'name' : stripped_line[1], 'name_url' : 'costumes/'+stripped_line[-1]})

				elif stripped_line[0] == 'make-up':
					movie_dict['crew'].append({'job' : 'make-up', 'name' : stripped_line[1], 'name_url' : 'make-up/'+stripped_line[-1]})
					
				else:
					if len(stripped_line) > 3:
						stripped_line[1:-1] = [' : '.join(stripped_line[1:-1])]
						if ' / ' in stripped_line[1] and '/actor/' not in stripped_line[1]:
							characters = stripped_line[1].split(' / ')

						elif '/ ' in stripped_line[1] and '/actor/' not in stripped_line[1]:
							characters = stripped_line[1].split('/ ')

						elif ' /' in stripped_line[1] and '/actor/' not in stripped_line[1]:
							characters = stripped_line[1].split(' /')

						elif '/' in stripped_line[1] and '/actor/' not in stripped_line[1]:
							characters = stripped_line[1].split('/')

						elif '/actor/' in stripped_line[1]:
							characters = ['UNKNOWN']

						else:
							characters = stripped_line[1]

					elif ' / ' in stripped_line[1] and '/actor/' not in stripped_line[1]:
						characters = stripped_line[1].split(' / ')

					elif '/ ' in stripped_line[1] and '/actor/' not in stripped_line[1]:
						characters = stripped_line[1].split('/ ')

					elif ' /' in stripped_line[1] and '/actor/' not in stripped_line[1]:
						characters = stripped_line[1].split(' /')

					elif '/' in stripped_line[1] and '/actor/' not in stripped_line[1]:
						characters = stripped_line[1].split('/')

					elif '/actor/' in stripped_line[1]:
						characters = ['UNKNOWN']

					else:
						characters = [stripped_line[1]]

					movie_dict['cast'].append({'name' : stripped_line[0],'name_url' : stripped_line[-1],'characters' : characters})

	return movie_dict

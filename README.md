# TPMDB
The Public Movie Database (TPMDB) is a repository with the tools I used to create one of the biggest public movie databases on the internet. In this folder you wil find all the files you will need to recreate a project like this one. You will need to modify are the following variables:

·The folder where the txt files will be downloaded.

·The folder where the MOVIES_DOWNLOADED file is.

·The folder where the MOVIES_ONE_LINE is.

Once you have changed this. you will need to run first the TPMDB_scraper.py, then TPMDB_creator to create the database once all the movie information has been downloaded. In case you don't want to run the web scraper, the movies.txt and movies_one_line.txt files contain all the movies from letterboxd up to 06/08/2021.

Anyway, I think the code has all the explanations one may need to understand it. Please, in case you use it remember to mention me.

**About the database**
This database contains information about:

628.956 movies.

1.076.473 actors and actresses.

658.430 crew members (directors, writers, composers, producers, sound, make-up...).

109.996 studios.

181 languages.

246 countries.

19 different genres.

You can find the database as well as all the txt files here: [https://archive.org/details/tpmdb_2021](https://archive.org/details/tpmdb_2021)

Here you have a graph with all the average movie rating ordered by country:

![alt text](https://i.imgur.com/rEoaKhV.png)

Note: this graph was created with an smaller dataset, 250.000 movies, instead of the full dataset, 620.000.

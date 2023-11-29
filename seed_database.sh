#!/bin/bash

rm db.sqlite3
rm -rf ./rareapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations rareapi
python3 manage.py migrate rareapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata rareusers
python3 manage.py loaddata categories
python3 manage.py loaddata tags
python3 manage.py loaddata posts
python3 manage.py loaddata comments
python3 manage.py loaddata reactions
<<<<<<< HEAD
python3 manage.py loaddata post_reactions
python3 manage.py loaddata post_tags
=======
python3 manage.py loaddata subscriptions
python3 manage.py loaddata demotion_queue
>>>>>>> zd-models-fixtures

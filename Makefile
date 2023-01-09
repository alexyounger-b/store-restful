clean:
	black .; isort .;

run:
	./manage.py runserver

db:
	./manage.py migrate

test:
	./manage.py test .

coverage:
	coverage run manage.py test .
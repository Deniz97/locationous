
dev:
	python manage.py runserver 

dev_celery:
	celery -A locationous worker --loglevel=info

dev_tcp:
	daphne -p 8000 locationous.asgi:application

migrations:
	python manage.py makemigrations 
# python manage.py makemigrations <app_name> -n <migration_name> 
# python manage.py makemigrations location -n remove_additional_data_field 

migrate:
	python manage.py migrate

# admin:admin
superuser:
	python manage.py createsuperuser 

test:
	make unittest
	make integrationtest

unittest:
	python manage.py test --tag=unit-test 

integrationtest:
	python manage.py test --tag=integration-test 


deps:
	pip install -r requirements.txt

run_postgre:
	docker stop postgres-instance-evreka || true
	docker rm postgres-instance-evreka || true
	docker run --name postgres-instance-evreka \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=test_database \
  -p 5432:5432 \
  -d postgres

run_redis:
	docker stop redis-instance-evreka || true
	docker rm redis-instance-evreka || true
	docker run --name redis-instance-evreka -p 6379:6379 -d redis
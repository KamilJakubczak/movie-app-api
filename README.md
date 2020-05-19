# movie-app-api
a basic movie database interacting with external API

https://movies-api11.herokuapp.com/api/movies/

# Docker-compose steps to run 
docker-compose build
docker-compose run --service-ports app sh -c 'python manage.py runserver 0.0.0.0:8000'

# External packages
Django>=3.0.6,<3.1.0
djangorestframework>=3.11.0,<3.12.0
psycopg2>=2.8.5,<2.9.0 for posgreSQL
flake8>=3.8.1,<3.9.0
requests>=2.23.0,<2.24.0 for connecting external API


# Available API endpoints
​POST /api/movies/:
    - params
        - title - required - movie title
    -response
        - 200 - movie object

GET /api/movies/:
    - params
        - none
    - response 
        - 200 - ok movies object list

GET /api/comments/:
    - params
        - none
    - response
        - 200 - ok comments object list

GET /api/comments/{movie_id}/:
    - params
        - movie_id
    - response
        - 200 - ok comment object for provided movie id

GET /api/top/:
   - params
        - date_from
        - date_to
    - response
        - 200 - returns moie ranking for provided time range
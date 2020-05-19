# movie-app-api
a basic movie database interacting with external API

https://movies-api11.herokuapp.com/api/movies/

# Docker-compose steps to run 
docker-compose build <br>
docker-compose run --service-ports app sh -c 'python manage.py runserver 0.0.0.0:8000'

# External packages
Django>=3.0.6,<3.1.0 <br>
djangorestframework>=3.11.0,<3.12.0 <br>
psycopg2>=2.8.5,<2.9.0 for posgreSQL <br>
flake8>=3.8.1,<3.9.0 <br>
requests>=2.23.0,<2.24.0 for connecting external API <br>


# Available API endpoints
POST /api/movies/: <br>
   - params <br>
       - title - required - movie title <br>
   -response <br>
       - 200 - movie object <br>

GET /api/movies/: <br>
   - params <br>
       - none <br>
   - response <br>
       - 200 - ok movies object list <br>

GET /api/comments/: <br>
   - params <br>
       - none <br>
   - response <br>
       - 200 - ok comments object list <br>

GET /api/comments/{movie_id}/: <br>
   - params <br>
        - movie_id <br>
   - response <br>
        - 200 - ok comment object for provided movie id <br>

GET /api/top/: <br>
   - params <br>
       - date_from <br>
       - date_to <br>
   - response <br>
        - 200 - returns moie ranking for provided time range <br>

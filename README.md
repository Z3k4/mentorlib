## Introduction
This application python project come from https://github.com/DUT-Info-Montreuil/Mentorlib-SME and https://github.com/DUT-Info-Montreuil/Mentorlib-SApp

Orginally the backend was writted with flask and the frontend with sveltekit. Because is more simple to maintain only one project and use SSR
I decided to rewrite in Django (also I prefer Django ORM instead of Sqlalchemy :))

This application use tailwind & flowbite for components

## Installation
```shell
git clone https://github.com/Z3k4/mentorlib.git
cd mentorlib
```

## Configuration

- Rename .env.example to .env
- Edit variables

To edit footbar, update config.json

Load fixtures
```
python manage.py loaddata $(find mentorlib/fixtures -type f -name '*.json')
```

## Running 
```
docker-compose up -d
```

## Debug

If you want to close all connections (for example to use reset_db)
```
select pg_terminate_backend(pid) from pg_stat_activity where datname = 'mentorlib';
```

## Features
* Admin
    * Create resources, departments, semesters
* Courses
    * List all courses
    * Filter courses
    * Comments
    * Uploading documents
    * Previzualising pdf
* Mentor
    * Accept course
    * Create course
    * Add notes on student
* API


# BlueWhale

*BlueWhale* is site of *datawhale* organization.

# Local Development

## Initialize Database

Install [MariaDB](https://mariadb.org/) and init root password. Create user and database:

```sql
CREATE USER bluewhale@'%' IDENTIFIED BY 'bluewhale';
CREATE USER bluewhale@'localhost' IDENTIFIED BY 'bluewhale';
CREATE DATABASE bluewhale CHARACTER SET UTF8MB4 COLLATE UTF8MB4_GENERAL_CI;
GRANT ALL PRIVILEGES ON bluewhale.* TO 'bluewhale'@'%';
GRANT ALL PRIVILEGES ON bluewhale.* TO 'bluewhale'@'localhost';
FLUSH PRIVILEGES;
```

## Install Dependencies

### Backend

Backend uses Python [Django](https://www.djangoproject.com/).

 * Install Python3.8
 * Install [pipenv](https://pypi.org/project/pipenv/): `pip install pipenv`
 * Change folder: `cd bluewhale`
 * Install python dependencies: `pipenv sync`
 * Activate virtualenv: `pipenv shell`
 * Init database tables: `python manage.py migrate`
 * Create superuser: `python manage.py createsuperuser`
 * Run local server: `python manage.py runserver`
 * When you what to testing mailing: `docker run -p 25:25 --env RELAY_NETWORKS=:0.0.0.0/0 -d namshi/smtp`

### API & Mocking

Use [OpenAPI 3.0.3](https://swagger.io/specification/) for API specification.

Use [Prism](https://github.com/stoplightio/prism) for mocking.

Refer to [openapi.yaml](openapi.yaml) for API documentation.

 * To edit API specification: `docker run -d -p 1080:8080 swaggerapi/swagger-editor`
 * After API specification changed, copy to [openapi.yaml](openapi.yaml)
 * To start mock server: `cd client && npm run mock`

### Frontend

Frontend uses [Vue](https://vuejs.org/).

 * Install Node.js version 12 (you can use [nvm](https://github.com/creationix/nvm)
 to manage multiple released Node.js)
 * Change folder: `cd client`
 * Install nodejs dependencies: `npm install`
 * Run local server: `npm run serve`
 * Run local server against mock server: `API_PORT=4010 npm run serve`

# System dependencies

## Python

Python 3.6+ is required.

> Ubuntu 18.04 comes with Python 3.6.5 pre-installed.

### pip

pip is required to setup the environment and install the dependencies:

```
sudo apt-get install python-pip
pip install --upgrade pip
```

### virtualenv

Install with pip:

```
pip install virtualenv
```

Create the environment:

```
virtualenv -p python3 ~/.virtualenvs/dgtt/
```

Activate the environment:

```
source ~/.virtualenvs/dgtt/bin/activate
```

Deactivate the environment:

```
deactivate
```

## PostgreSQL

PostgreSQL 9.5+ is required:

```
sudo apt-get install postgresql postgresql-contrib
```

### PostGIS

PostGIS extension is required.

Installation:

```
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt-get update
sudo apt-get install postgis
```

Open configuration file:

```
sudo nano /etc/postgresql/9.5/main/postgresql.conf
```

and adjust the following settings:

```
shared_buffers = 200MB
work_mem = 16MB
maintenance_work_mem = 128MB
random_page_cost = 2.0
```

Restart PostgreSQL to apply changes:

```
sudo service postgresql restart
```

# Project dependencies

Install with pip:

```
pip install -r requirements/dev.txt
```

# Database

Create a database and a dedicated user. Then grant all privileges to this user for created database. Install `postgis`
extension.

```
sudo -i -u postgres
createdb dgtt
psql -s dgtt
create user dgtt password 'dgtt';
GRANT ALL PRIVILEGES ON DATABASE dgtt TO dgtt;
CREATE EXTENSION postgis;
```

Apply migrations:

```
python manage.py migrate
```

## Fixtures

Seeding database:

```
python manage.py seed
```

# Local settings

There is a template called `local_settings_example.py` in `dgtt` directory. Copy and rename it as `local_settings.py` and adjust if needed.

# Serving the site

Run the server:

```
python manage.py runserver
```

# API

Examples:

- Organizations by building: http://127.0.0.1:8000/organizations/by-building/1/.
- Organizations by category: http://127.0.0.1:8000/organizations/by-category/1/
- Organizations by point with radius: http://127.0.0.1:8000/organizations/by-radius/54.873950,69.152105/10/. Radius must be specified in kilometers.
- Organizations by rectangle: http://127.0.0.1:8000/organizations/by-rectangle/54.873950,69.152105/54.973950,69.052105/. The first parameter is a north west point, the second one is a south east point.

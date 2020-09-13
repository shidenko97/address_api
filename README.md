# Address API

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Just a free simple address API. You can upload your own data and use it for you web-forms. In future you will can add streets and homes through the API.

## Installing
- Clone repo
- Create virtual env
- Install requirements `pip install -r requirements.txt` or `make install-requirements`
- Set environment variable `DB_URL` - url to postgres database
- Apply migrations by the command `python db/migrations/ upgrade head` or `make upgrade-all`
- Run it by command `python main.py` or `make run`

## Api Documentation
Swagger UI Api Documentation is available by the url `/documentation`

## Make file
It has a Make file to simplify work with it. You can see all Make commands by executing `Make help` in root directory.

## Uploading data
At the moment it has only one data source - Ukrposhta free database.

For uploading you can use following commands: `python upload --source={SOURCE}` or `make upload SOURCE={SOURCE}`, where `{SOURCE}` is a datasource class name.
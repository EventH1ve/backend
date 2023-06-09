# EventHive Backend
This project is built using Python and FastAPI.

## Prerequisites
- Install Python 3.8
- Install Pip
- Install Pipenv for virtual environments

## Installation Instructions
While in the root folder, create a virtual environment by running the following command: 
```bash
pipenv shell
```
Install dependencies by running the following:
```bash
pipenv install -r requirements.txt
```
In order to run the project, the terminal's path must be in the app folder:
```bash
cd app
```
Database migrations must then be run using (make sure to have a database by the name `eventhive` already created in postgres before running this):
```bash
alembic upgrade head
```
Note: during development, changes to the database must be reflected in the register.py file within the models folder and then the following command must be run to commit the changes:
```bash
alembic revision --autogenerate -m "Commit Message"
```
The project can then be launched using uvicorn:
```bash
uvicorn main:app --reload
```

## Important Notes
The project will not run properly without the `.env` file with proper environment variables setup.\
The `.env` file must be located inside the `app` folder, and must contain values for the following variables:
- PROJECT_ENV (Currently set to `dev`)
- DATABASE_URL
- JWT_SECRET
- JWT_ALGORITHM (Set it to HS256)
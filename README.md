# Component Management System

## Project Description:
The Component Management System is a utility application designed to manage FreeCAD models from different online repositories. It provides features to seamlessly browse, download, and organize individual models while avoiding the need to download the entire library. The system is built using Flask, SQLite, and SQLAlchemy, and it serves as the backend API for the **Component Library Plugin**.

## Features:

1. Browsable online repository of FreeCAD components.
2. Individual component download with preview and metadata.
3. Integration with the Component Library Plugin frontend.
4. Structured online repository storage system.
5. RESTful API endpoints for component management.

## Setup
1. Clone the repository: `git clone [repository URL]`
2. Navigate to the project directory: `cd Component_Management_System`
3. Install dependencies using Poetry: `poetry install`
4. Run API: `flask run`

## Dependencies
1. python = "^3.10"
2. flask-sqlalchemy = "^3.0.3"
3. flask-marshmallow = {version = "0.14.0", extras = ["sqlalchemy"]}
4. connexion = {extras = ["swagger-ui"], version = "^2.14.2"}
5. flask = "2.2.2"
6. elasticsearch = "^8.8.0"
7. python-dotenv = "^1.0.0"
8. pygithub = "^1.59.0"

## Prerequisites
1. Setup elastic search
2. Add environment variables to .env file of directly
- FLASK_APP=component_management_system
- FLASK_SECRET_KEY
- FLASK_DEBUG
- ELASTICSEARCH_USERNAME
- ELASTICSEARCH_PASSWORD
- ACCESS_TOKEN (github)

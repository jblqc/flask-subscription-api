# Subscription API Activity
A simple Flask-based RESTful API to manage **Users**, **Products**, **Subscription Plans**, **Subscriptions**,  **Payments**, and **Access Continuity**.
## Features
- User and Product Management
- Subscription and Plan Handling
- Payment Simulation
- Auto-generated Swagger UI at `/swagger/`

---
## Setup Instructions
### 1. Clone the Repository
```bash
git clone https://github.com/jblqc/flask-subscription-api.git
cd flask_restx_tutorial
```
### 2. Create & Activate Virtual Environment
```bash
# Create
python -m venv .venv

# Activate
# On Windows
.venv\Scripts\activate

```
### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask App
```bash
#Make sure you have a .flaskenv file in the root directory with the following content:
#FLASK_APP=app:create_app
#FLASK_DEBUG=True

flask run

```
---

## Access the API Documentation

Once the server is running, visit:

```
http://localhost:5000/swagger/
```

You’ll find the Swagger UI with all available endpoints.

---

## Database

SQLite is used as the default database. The database file will be created automatically on first run:

```text
instance/db.sqlite3
```

To inspect or manage the database:

```bash
sqlite3 instance/db.sqlite3
.tables
```

---
##   Flask Shell Commands used

```bash
flask shell
>>> from app.models import *
>>> db.create_all()
>>> exit()
```

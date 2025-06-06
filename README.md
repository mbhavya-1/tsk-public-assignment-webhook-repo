# TechStaX : Dev Assessment - Webhook Receiver

This project listens to GitHub webhook events (Push, Pull Request, Merge), stores them in a MongoDB database, and serves the data to a frontend that displays the latest repository activity in real-time.

******

## Setup : For using this Repositry

* Repositories Overview

action-repo: A GitHub repo where actions like Push, PR, and Merge occur. Webhooks are configured here.
tsk-public-assignment-webhook-repo: This Flask app receives GitHub webhook payloads, processes them, and stores relevant data in MongoDB.

* Tech Stack

Backend: Flask (Python)
Database: MongoDB (MongoDB Atlas)
Frontend: React.js (periodically fetches and displays events)
Others: Ngrok (for exposing localhost to GitHub), Axios, Flask-CORS

* Initial Setup
  Clone the repo.
  Create a .env file with your MongoDB URI.
  
* Activate the virtual env

```bash
.\venv\Scripts\activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```
*Run Ngork:
```bash
.\venv\Scripts\ngrok.exe http 5000
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

![Webhook UI](screenshots/ui.png)

**↑ GitHub Webhook Frontend showing real-time updates**

## Note

* GitHub Webhook should be configured to send:
  push
  pull_request
  pull_request with merged status

* Use Ngrok to expose Flask locally and register it as GitHub Webhook URL.

Action Repo used for this Project: https://github.com/mbhavya-1/action-repo

* Author: Bhavya Mehta

*******************

# TechStaX : Dev Assessment - Webhook Receiver

This project listens to GitHub webhook events (Push, Pull Request, Merge), stores them in a MongoDB database, and serves the data to a frontend that displays the latest repository activity in real-time.

******

## Setup : For using this Repositry

* Activate the virtual env

```bash
source venv/bin/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

You need to use this as the base and setup the flask app. Integrate this with MongoDB (commented at `app/extensions.py`)

*******************
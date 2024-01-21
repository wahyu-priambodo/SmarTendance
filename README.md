# SmarTendance V2

## Setup & Installation

```python
pip install -r requirements.txt
flask run
# or you can create your own venv inside our project by using this command:
python -m venv .venv
# or by virtualenv command
virtualenv .venv 
```

## Usage

Coming soon.

## Libraries

- setuptools
- gunicorn
- python-dotenv
- Flask
- Flask-SQLAlchemy
- PyMySQL Flask-Migrate
- Flask-SocketIO
- Flask-MQTT
- Flask-WTF
- email-validator
- Flask-Argon2

## Notes

If you cannot rename or remove database in phpMyAdmin, you can try to repair the spesific table that may have  problem.

- In the left sidebar, click the name of the database that you want to check,
- In the navbar (at the top), go to the `Operations`,
- Scroll down until you find `Table Maintenance` section,
- And finally, you can click the `Repair` or `Optimize` table.

TODO:

- [ ] Add self-signed SSL certificate (ON PRODUCTION)
- [X] Remove trailing slash for each routes / endpoints (DONE)
- [X] Add pop-up confirmation while user want to delete or logout (DONE)
- [X] Add pop-up notification after admin complete form registration (DONE)
- [ ] Fetch data from flask over websocket (realtime).

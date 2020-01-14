# currency_converter_app
A flask and redis currency converter prototype

# How to run (tested on Ubuntu 18.04)
Install dependencies
`sudo apt-get install redis-server python3-venv pip`

cd into `scripts` folder and run `. create_venv.sh`

cd into `app` folder and run `python parser.py`

When the script is completed, setup and run flask:
```
FLASK_APP=app.py
flask run
```

Once the flask server is up and running use the endpoint like in the following example:
`http://127.0.0.1:5000/convert?amount=50&src_currency=EUR&dest_currency=USD&reference_date=2019-11-05`

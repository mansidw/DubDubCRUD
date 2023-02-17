## STEPS TO RUN
Python 3.10.5

Create a virtual environment

```sh
python -m venv env
```
Install the required dependencies and packages from requirements.txt

```sh
python3 -m pip install -r requirements.txt
```

Open terminal inside the opened folder and start python shell (perform only once after installation)
This step is required beacuse I am using the inbuilt file based sqllite database and its initialization is required. So basically every time we delete the database file these commands will have to be run.
```sh
python
>>>from app import app
>>>from app import db
>>>db.create_all()
>>>exit()
```

Start the server
```sh
flask run
```


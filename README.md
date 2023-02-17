## STEPS TO RUN
Python 3.10.5

* For this assignment I used the class based approach provided by Flask RESTful which gives the object-oriented design pattern to our APIs. Though I am well aware with the function based approach also.

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

Run using DOCKER if installed

```sh
docker pull mansidw/dubdub:latest
```
```sh
docker run -it --init -p 5000:5000 mansidw/dubdub
```
## Try Spotify

[View Application](https://try-spotify.herokuapp.com/login)

An application to show some spotify playlist and save the user play song data

## Technology Stack

- Backend: Python, Flask, PostgreSQL, SQLAlchemy
- Frontend: JavaScript, AJAX, HTML, CSS, Bootstrap

## Run Locally

In order to run the app locally, you will need to run following steps

1. Clone repository:

```
$ git clone website name
```

2. Navigate into directory:

```
$ cd try-spotify
```

3. Create python virtual environment (I use windows):

```
$ python -m venv venv
```

4. Activate virtual environment:

```
$ source venv/Scripts/activate
```

5. Install python packages:

```
(venv) $ pip install -r requirements.txt
```

6. Run seed.py file to create database tables:

```
(venv) $ python seed.py
```

7. Run application:

```
(venv) $ flask run
```

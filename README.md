# Todo Web App

A simple Todo web application built with Flask.

## Features

- Add todo
- List todos
- Toggle todo status
- Delete todo
- SQLite persistence

## Tech Stack

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite

## Environment Variables

Create a `.env` file based on `.env.example` if needed.

```env
FLASK_DEBUG=false
PORT=5000
SECRET_KEY=change-me
```

## How to Run

**Development Run**

```bash
pip install -r requirements.txt
python app.py
```
**Production Run**

```bash
pip install -r requirements.txt
gunicorn app:app
```

**The SQLite database file `todo.db` will be created automatically when the app starts.**

Open:

```text
http://127.0.0.1:5000
```

## Project Structure

```text
todo_app/
├── app.py
├── db.py
├── requirements.txt
├── README.md
└── templates/
    └── index.html
```

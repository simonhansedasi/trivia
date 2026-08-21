# trivia

Dark-themed multiple-choice trivia game — pulls questions live from the Open Trivia Database API.

## What it does

Fetches random questions from opentdb.com with category and difficulty filters. Dark UI, readable in a car. Built as an alternative to using ChatGPT for road trip trivia.

## Tech

Python, Flask, HTML/CSS/JS

## Run locally

```bash
python app.py   # http://localhost:5014
```

## Deploy

```bash
./deploy_do.sh  # rsync to DO, restarts trivia.service
```

## Live

https://trivia.simonhansedasi.com

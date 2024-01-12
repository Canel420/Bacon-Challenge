# Bacon Challenge

## Overview
The Bacon Challenge is a simple web application that fetches paragraphs from the [Bacon Ipsum API](https://baconipsum.com/json-api/), performs word analysis, and returns a PDF to the user. The analysis includes frequently occurring words, distribution of word lengths, trigrams, and bigrams. The results, along with the original paragraphs, are presented in a visually appealing format.

## Built With
- [Flask](https://flask.palletsprojects.com/): A lightweight WSGI web application framework.

## Features
- Dynamically fetches paragraphs from the Bacon Ipsum API.
- Performs word analysis on the fetched paragraphs.
- Generates a PDF with the paragraphs, analysis, and data visualizations.

## Getting Started
To get a local copy up and running, follow these steps:

1. Clone the repo
   ```bash
   git clone https://github.com/your_username_/Project-Name.git

2. Navigate to the project directory
   ```bash
   cd Project-Name

3. Create a virtual environment
   ```bash
   python3 -m venv env

4. Activate the virtual environment
   On Unix or MacOS, run:
   ```bash
   source env/bin/activate
   
5. Install the requirements
   ```bash
   pip install -r requirements.txt

6. Run the app
   ```bash
   python app.py
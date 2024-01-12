# Bacon Challenge

## Overview
The Bacon Challenge is a simple web application that fetches paragraphs from the [Bacon Ipsum API](https://baconipsum.com/json-api/), performs word analysis, and returns a PDF to the user. The analysis includes frequently occurring words, distribution of word lengths, trigrams, and bigrams. The results, along with the original paragraphs, are presented in a visually appealing format.

## Built With
- [Flask](https://flask.palletsprojects.com/): A lightweight WSGI web application framework.

## Methodology

This simple web application is built with a scalable and maintainable architecture in mind. The project is structured into three main components:

1. **Routes**: This folder contains all the API routes. Each route corresponds to a specific functionality of the application, making it easy to understand and manage the different endpoints of the application.

2. **Controllers**: This folder contains the logic for handling requests and responses. Each function in this folder corresponds to a route and contains the logic for processing the request and generating the response.

3. **Models**: This folder contains the definitions for the database tables. Each file in this folder corresponds to a table in the database, and defines the structure of the table.

This structure ensures that different aspects of the application are separated and can be developed and maintained independently. It also makes it easy to scale the application, as new routes, controllers, and models can be added as needed without affecting the existing code.

## Features
- Dynamically fetches paragraphs from the Bacon Ipsum API.
- Performs word analysis on the fetched paragraphs.
- Generates a PDF with the paragraphs, analysis, and data visualizations.

## Getting Started
To get a local copy up and running, follow these steps:

1. Clone the repo
   ```bash
   git clone https://github.com/Canel420/Bacon-Challenge.git bacon

2. Navigate to the project directory
   ```bash
   cd bacon

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

## Finance Tracker CLI

  A simple command-line interface (CLI) application for tracking financial expenses and managing user transactions.

## Table of Contents
 - Overview
 - Features
 - Technologies Used
 - Installation
 - Usage
 - Available Commands
 - Database Schema
 - Contributing
 - License

## Overview
The Finance Tracker CLI is a Python-based command-line application that allows users to manage their expenses efficiently. Users can add, edit, delete, and view transactions while also generating financial reports based on different filters such as date and category. The application uses SQLAlchemy ORM to interact with an SQLite database.

## Features
✔️ Register and manage users
✔️ Record financial transactions (expenses)
✔️ View expenses with optional filters (category, date range)
✔️ Edit or delete expenses
✔️ Generate reports on total spending

## Technologies Used
   - Python (CLI application)
   - Click (Command-line interface framework)
   - SQLAlchemy (ORM for database management)
   - SQLite (Lightweight database)

## Installation
- Prerequisites
     - Ensure you have Python installed (version 3.8).

- Setup Steps
     1. Clone the Repository

                  '''git clone https://github.com/your-username/finance-tracker.git
                     cd finance-tracker'''
 
     2. Set Up Virtual Environment
        - pipenv install && pipenv shell

     3. Install Dependencies
        - pipenv requirements > requirements.txt
## Usage
  - Run the CLI application using:
       - python main.py [COMMAND]

  - For help with commands:
       - python main.py --help


  - Available Commands
  
  ## User Management

- Create a new user
    - python main.py create-user
 
- Register a user:
    - python main.py add-user

  ## Expense Management

- Add an expense:

    - python main.py add-expense

- View expenses:

    - python main.py view-expenses

- Edit an expense:

    - python main.py edit-expense

- Delete an expense:

    - python main.py delete-expense

## Reports
- Generate spending report:

## Database Schema
The application uses an SQLite database with the following tables:

## Users Table (`users`)

| Column  | Type                 | Description                |
|---------|----------------------|----------------------------|
| `id`    | Integer (Primary Key) | Unique identifier         |
| `name`  | String               | User's full name          |
| `email` | String               | Unique email address      |

## Transactions Table (`transactions`)

| Column       | Type                  | Description                        |
|-------------|-----------------------|------------------------------------|
| `id`        | Integer (Primary Key)  | Unique transaction ID             |
| `user_id`   | Integer (Foreign Key)  | Links to user                     |
| `amount`    | Float                  | Transaction amount                 |
| `category`  | String                 | Expense category                   |
| `description` | String               | Short description of the transaction |
| `date`      | Date                   | Transaction date                   |

## Contributing
- Contributions are welcome! To contribute:

  - Fork the repository
  - Create a new branch (feature-branch)
  - Commit your changes
  - Push to your branch and create a pull request

## License

- This project is licensed under the MIT License.












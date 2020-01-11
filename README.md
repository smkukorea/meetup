# CSC210 Final Group Project: Scheduling App

## How to Use

#### Setting up the Development Environment
1. To create your virtual python environment, navigate to the `schedule-app` directory and run `python -m venv venv`
2. Activate your virtual environment by running `venv\Scripts\activate` on Windows, or
`source venv/bin/activate` on macOS or Linux
3. Install dependencies by running `pip install -r requirements.txt`

#### Running the Application
From within the virtual environment (*venv*), run `flask run`

#### Adding new dependencies
If you add new dependencies (pip packages), you will need to update the `requirements.txt` file by running `pip freeze > requirements.txt`

If somebody else adds a new dependency, you will need to download that dependency to your own virtualenv by running `pip install -r requirements.txt`

#### Upgrading the Database
1. `flask db migrate`
2. `flask db upgrade`

Use these two commands to migrate the existing database to one with updated models. These are from the `flask-migrate` package.

## To-Do List

* Forgot Password Link (sends an email with reset code)
* Build Application UI
* Build Application Back-End
* Send invitation

## Known Problems

* 'Remember Me' does nothing
* Attempting to signup with non-unique email leads to raw flask error page


**Jamie Huber**, Database Engineer

**Mitchell Jones**, Front-End

**Seungmin Kuk**, User Authentication

**Denis Lomakin**, UX/UI

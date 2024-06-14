# InstaBook
## Author: @Roshan-Baghwar
- InstaBook is a social media web application developed using Python and Django.
- For web-page templates; JavaScript, HTML and CSS is used.
## Initial Set-up (installing libraries & dependencies)
- Install Python
```
https://docs.python.org/3/installing/index.html
```
- Install pip
```
https://pip.pypa.io/en/stable/installation/
```
- Install Django
```
pip install django
```
## Ensure you're in the base-directory
- Use `dir` (in Windows) and `ls` (in MacOS or Linux) to check current directory
- Navigate to `~\InstaBook\InstaBook>` directory and check for `manage.py`, `db.sqlite3`, `UserService.py` files (This is the base-directory).
## Run following commands for initial database setup
```
python manage.py makemigrations
```
```
python manage.py migrate
```
## Run the Application
- From base directory run the following command to run the application.
```
python manage.py runserver
```
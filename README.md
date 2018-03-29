# SAC Room Booking Portal

This portal allows independent bodies of IIT Bombay to book rooms in SAC.

## Installation Instructions
```
git clone https://github.com/rohitrp/SAC-Room-Booking-Portal.git
cd SAC-Room-Booking-Portal
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py makemigrations authentication rooms bookings
python manage.py migrate
python manage.py runserver
```

Create a .env in the cloned directory and add the following. Replace the values with appropriate email server settings:
```
EMAIL_HOST=smtp-auth.iitb.ac.in
EMAIL_PORT=25
EMAIL_HOST_USER=xyz@iitb.ac.in
EMAIL_HOST_PASSWORD=password
EMAIL_USE_TLS=True
```

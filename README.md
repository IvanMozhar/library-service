# Library service API
The Library service API is designed to offer an API service for library management.
It provides functionalities such as book borrowing, returning book, registration, payment for borrowings.
This API aims to streamline library operations by facilitating easy access to book information,
managing user payments and ensuring efficient loan system.
## Before installing
- create stripe account (use test data) to get stripe public and secret key
- use telegram bot @BotFather to create your bot and get chat id and chat token
## Installing using GitHub

```
git clone https://github.com/IvanMozhar/library-service.git
cd library-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set DJANGO_SECRET_KEY=<yoursecretkey>
set TELEGRAM_BOT_TOKEN=<your telegram bot token>
set TELEGRAM_CHAT_ID=<your telegram chat id>
set STRIPE_PUBLIC_KEY=<your stripe public key>
set STRIPE_SECRET_KEY=<your stripe private key>
python manage.py migrate
python manage.py runserver
```
## To get access
- create user via /api/user/register/
- get access token via /api/user/token/

# Project features
- JWT authentication
- daily-based function is implemented using Django-q
- payment service is implemented using Stripe
- documentation is available by api/doc/swagger/
- get list of books api/see-books/books/
- get detail book info api/see-books/books/<int:pk>/
- see your borrowings (for non-admin users) api/borrow-book/borrowings/
- get detail borrowing api/borrow-book/borrowings/<int:pk>/
- return your borrowing api/borrow-book/borrowings/<int:pk>/return/
- see all payment session (for admins) api/payment-session/payments/
- for user only their payment sessions will be displayed
- by clicking on session url, user will be able to pay for borrowing
- each time user makes a borrowing, telegram bot will send notification
- using admin panel schedule task "check_overdue_borrows" that will send notification to telegram bot if overdue borrows are found

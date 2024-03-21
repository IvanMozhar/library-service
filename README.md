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
- use test cards provided by stripe to get succesful or canceled payment (for ex. card number 4242 4242 4242 4242, any CVC, any valid expiration date)
- if the borrowings has missed deadline, user will pay fine
- each time user makes a borrowing, telegram bot will send notification
- using admin panel schedule task "check_overdue_borrows" that will send notification to telegram bot if overdue borrows are found

# Project pages
## Borrowings list
![image](https://github.com/IvanMozhar/library-service/assets/147508342/f2b43096-072f-4d70-818c-40498ce306cd)
## Create borrowing
![image](https://github.com/IvanMozhar/library-service/assets/147508342/ec529c7c-bfc4-480a-8699-04d3874a4652)
## Get detailed borrowing info
![image](https://github.com/IvanMozhar/library-service/assets/147508342/c06f8f89-9757-4f80-a176-7c64e1e5ac02)
## Return borrowing
![image](https://github.com/IvanMozhar/library-service/assets/147508342/ea23b6fa-b8a2-4432-958d-418fe74da18f)
## Get list of payments
![image](https://github.com/IvanMozhar/library-service/assets/147508342/d09efacd-c013-4c13-b32a-d789a9621feb)
## Get detailed payment info
![image](https://github.com/IvanMozhar/library-service/assets/147508342/4d26c2e1-e356-42a9-ab88-6b582507a160)
## Success payment (return payment info)
![image](https://github.com/IvanMozhar/library-service/assets/147508342/5744cd9c-903b-4ee4-ba4d-9ef80382530e)
## Canceled payment
![image](https://github.com/IvanMozhar/library-service/assets/147508342/d59fc814-4125-4f92-a33e-0c4a64229ae1)
## Get list of books
![image](https://github.com/IvanMozhar/library-service/assets/147508342/43652ce0-3fdd-4ee3-b8f9-1538d2a5106a)
## Create book (for admins only)
![image](https://github.com/IvanMozhar/library-service/assets/147508342/ab532ce4-8e93-439b-9358-1b79606c6eea)
## Get detailed book info
![image](https://github.com/IvanMozhar/library-service/assets/147508342/417877c7-67ce-4019-ad11-105842189a5e)
## Stripe payment
![image](https://github.com/IvanMozhar/library-service/assets/147508342/c867fcb3-2a28-4ed1-90dc-9692f709d0f9)

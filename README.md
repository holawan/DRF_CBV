# DRF for beginners

### What we shall cover

- Environment setup 
- Models and Custom user model 
- User Registration
- JWT authentication
- User Login
- Sending email
- User email verification
- Unittesting
- Viewsets and urls 
- Generic API Views 
- CORS and REST 
- Django templates and static setup 
- Pagination support 
- API documentation
- Postman documentation integration
- Project documentation views 
- Admin and models 
- Test coverage reporting 
- Github + Travis ci integration
- Deployment 

### Prerequisites

- Basic python concept

- OOP principles 

## Project Setup and Apps 

1. Python version 3 이상 설치

2. 가상환경 생성

    ```
    python -m venv venv 
    source venv/Scripts/activate
    ```

3. Django 설치

    ```
    pip install django==3.1.7 djangorestframework
    ```

4. app에 rest_framework 추가 

5. 앱 만들기 

    ```
    python manage.py startapp todos
    python manage.py startapp authentications
    ```

6. git ignore 생성

    https://www.toptal.com/developers/gitignore/

## Create a Tracking Model


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

- Django는 모델을 생성할 때마다 약간의 지식이 필요하다

- 장고 모델의 객체가 생성되거나 업데이트 될 때 검색 방법을 통해 대부분의 항목이 어플리케이션에 공통적으로 적용된다.

- 장고는 생성된 각 모델에서 생성된 것과 같은 필드를 제공하지 않으므로 우리는 모델 헬퍼를 생성하여, 모델을 생성할 때 세부정보를 한 번에 빠르게 추가할 수 있는 helper를 생성한다

#### 생성방법

- helpers라는 폴더를 생성하고 models.py 파일을 만든다

```python
class TrackingModel(models.Model) :
    # 객체가 생성된 시간에 맞게 생성됨 
    created_at = models.DateTimeField(auto_now_add=True)
    # 객체가 수정될 때 마다 시간이 갱신됨 
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta :
        abstract=True
        # 생성 시간을 역정렬해서 정렬함 
        ordering=('-created_at',)
```

- abstract=True 옵션
    - 부모 모델은 실제로 존재하지 않는 가상의 클래스가 된다.
    - 자식 모델은 부모 필드의 속성과 함수를 물려받는 실체가 있는 DB 테이블이 된다. 
    - abstract를 사용한다는 것은 자식 모델들이 부모 없이 각각 독립적인 DB 테이블로서 존재하며, 자식과 부모의 상속관계는 실제로 없는 것이다. 공통된 필드가 많이 있는 모델 클래스들이 있을 때 코드를 효율적으로 사용하기에 편리한 기능이다.
- ordering
    - 객체를 조건 내의 순서로 정렬할 수 있다.

## Django Custom User Model

- email을 username 대신 인증 수단으로 사용한다. 

- 이를 위해 BaseUser에서 필요한 기능들을 가져온다.

    - django.contrib.auth.models에서 AbstractUser을 복사한다.
    - email을 blank=False, unique=True로 설정한다

- usermanager

    - 객체가 생성되거나 검색되는 방식을 지정하는 클래스

    - 객체 생성 방식을 변경할 때마다 사용자 지정 관리자를 정의하고 메서드가 작동하는 방식을 변경해야 하므로 중요하게 이용될 수 있다.

```python
from datetime import timezone
from django.db import models

from helpers.models import TrackingModel
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser,UserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# Create your models here.


# add new prooperites access_token, is_email_verified
# Use email and password instead of username/password

class MyUserManager(UserManager) : 
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        # username 미입력시 
        if not username:
            raise ValueError('The given username must be set')
        #email 미입력시 
        if not email:
            raise ValueError('The given email must be set')
        
        # email 유효성 검사 
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

   

class User(AbstractBaseUser, PermissionsMixin,TrackingModel) :
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    
    # username에 대한 유효성 검사 
    username_validator = UnicodeUsernameValidator()

    # username은 char field 
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(_('email address'), blank=False,unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email_verified = models.BooleanField(
        _('email_verified'),
        default=False,
        help_text=_(
            'Designates whether this user email is verified  '
        ),
    )
    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    @property
    def token(self) :
        return ''
        
```



## User Model Test

### Coverage

- coverage라는 패키지를 이용하면, 각 Django의 모델들을 모두 테스트하고 로그를 편안하게 볼 수 있다.

```
pip install coverage
```

```
coverage run manage.py test && coverage report && coverage html 
```

- test 
    - test코드를 진행한다
- report
    - test 결과를 표시한다
- html
    - html로 테스트 된 코드의 여부를 확인할 수 있다.

#### testcode

```python
from rest_framework.test import APITestCase
from authentication.models import User 

class TestModel(APITestCase) :
    
    def test_creates_user(self) :
        
        user=User.objects.create_user('test','test@gmail.com','password123!@#')
        
        self.assertIsInstance(user,User) 
        self.assertFalse(user.is_staff) 
        self.assertEqual(user.email,'test@gmail.com') 
    
    
    def test_creates_super_user(self) :
        
        user=User.objects.create_superuser('test','test@gmail.com','password123!@#')
        
        self.assertIsInstance(user,User) 
        self.assertTrue(user.is_staff) 
        self.assertEqual(user.email,'test@gmail.com') 
```

#### HTML 표시 화면 

![coverage](README.assets/coverage.GIF)

#### 최종 테스트 

```python
from rest_framework.test import APITestCase
from authentication.models import User 

class TestModel(APITestCase) :
    
    # 기본 유저 생성 
    def test_creates_user(self) :
        
        # 기본 유저 생성 
        user=User.objects.create_user('test','test@gmail.com','password123!@#')
        
        self.assertIsInstance(user,User) 
        # 기본 user가 staff가 아닌가? 
        self.assertFalse(user.is_staff)
        # 생성된 user의 email과 생성시 입력한 email이 일치하는가 
        self.assertEqual(user.email,'test@gmail.com') 
    
    # 슈퍼 유저 생성 
    def test_creates_super_user(self) :
        
        # 슈퍼 유저 생성 
        user=User.objects.create_superuser('test','test@gmail.com','password123!@#')
        
        # 생성된 이메일이 User model의 instance인가. 
        self.assertIsInstance(user,User) 
        # 생성된 객체가 staff가 맞는가 ? 
        self.assertTrue(user.is_staff) 
        # 생성된 user의 email과 생성시 입력한 email이 일치하는가 
        self.assertEqual(user.email,'test@gmail.com') 

    #username 미입력 오류 테스트 
    def test_raises_error_when_no_username_is_supplied(self) :
        self.assertRaises(ValueError,User.objects.create_superuser, username="",email='test@gmail.com',password='password123!@#')
        self.assertRaisesMessage(ValueError,'The given username must be set')
    
    
    def test_raises_error_with_message_when_no_username_is_supplied(self) :
        with self.assertRaisesMessage(ValueError,'The given username must be set') :
            User.objects.create_superuser(username='',email='test@gmail.com',password='password123!@#')
        
        
    
    def test_raises_error_when_no_email_is_supplied(self) :
        self.assertRaises(ValueError,User.objects.create_superuser, username="test",email='',password='password123!@#')
        
    def test_raises_error_with_message_when_no_email_is_supplied(self) :
        with self.assertRaisesMessage(ValueError,'The given email must be set') :
            User.objects.create_superuser(username='test',email='',password='password123!@#')
    
    
    def test_creates_super_user_with_staff_status(self) : 
        with self.assertRaisesMessage(ValueError,'Superuser must have is_staff=True.') :
            User.objects.create_superuser(username='test',email='test@naver.com',password='password123!@#',is_staff=False)
        
    
    def test_creates_super_user_with_super_user_status(self) : 
        with self.assertRaisesMessage(ValueError,'Superuser must have is_superuser=True.') :
            User.objects.create_superuser(username='test',email='test@naver.com',password='password123!@#',is_superuser=False)

```

#### coverage 결과

authentication\admin.py        3      0   100%
authentication\apps.py         3      3     0%
authentication\models.py      47      1    98%
authentication\views.py        1      1     0%
todos\admin.py                 1      0   100%
todos\apps.py                  3      3     0%
todos\models.py                1      0   100%
todos\tests.py                 1      0   100%
todos\views.py                 1      1     0%

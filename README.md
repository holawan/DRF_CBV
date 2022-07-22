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
    #username 필드를 email로 선언하면 email을 기본 로그인 수단으로 이용할 수 있다.!! 
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



## User Registration (Email/Password)

### Class Based View

- 클래스 기반으로 View 함수를 작성하는 것

#### 왜 CBV를 사용하는가?

- Django의 많은 기능을 상속할 수 있기 때문

### GenericAPIView

- DRF에서는 GenericAPIView에 CreateModelMixin,ListModelMixin 등 다양한 클래스를 결합해 APIView를 구현한다.
- GenericAPIView는 CRUD에서 공통적으로 사용되는 다양한 속성을 제공하고, Mixin은 CRUD에서 특정 기능을 수행하는 메소드를 제공한다.
- DRF에서는 GenericAPIView와 Mixin으로 대부분 API View를 구성하지만, 상황과 모델, 요청에 따라 메소드를 Override 해서 커스텀을 진행한다. 

### Register

```python
class RegisterAPIView(GenericAPIView) :
    
    
    serializer_class=RegisterSerializer 
    
    
    def post(self,request) :
        serializers = self.serializer_class(data=request.data)  
        
        if serializers.is_valid() :
            serializers.save()
            return response.Response(serializers.data,status=status.HTTP_201_CREATED)
        return response.Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
```

- serializer_class 
    - 요청을 받은 값에 대해 직렬화를 진행하며, 유효성 평가를 할 수 있는 클래스를 지정한다.
    - serializer는 보통 개발자의 의도에 따라 Model에 맞추어 등록하고, 요청을 받을 Model을 대상으로 직렬화 class를 만든다. 

### Serializer

- 사용자가 우리 프로그램에  json 데이터를 보낼 때 이를 파이썬 네이티브 객체로 바꾸는 역할을 한다.

- 왜냐하면 사용자가 JSON 데이터를 보낼 때 모델 객체처럼 매핑을 해야하기 때문 

- 이것을 연결하는데 도움을 주는 것이 serializer이다. 

- 또한 이를 python 객체를 json으로 변환하여 유저에게 제공한다.  

```python
class RegisterSerializer(serializers.ModelSerializer) :
    
    password = serializers.CharField(max_length=128,min_length=6,write_only=True)
	#password를 write_only로 설정하여, API 결과로는 보이지 않게 할 수 있다 .    
    class Meta() :
        model=User
        fields = ('username','email','password',)
        
    
    def create(create,validated_data) :
        
        return User.objects.create_user(**validated_data)
```

## Authenticate a user. Get JWT Access Token. 

#### Views.py

```python

#토큰으로 인증된 유저 정보 가져오기 
class AuthUserAPIView(GenericAPIView) :
    
    permission_classes=(permissions.IsAuthenticated,)
    def get(self,request) :
        # print(request.user)

        user = request.user
        serializers=RegisterSerializer(user)
        
        return response.Response({'user':serializers.data})
    
class LoginAPIView(GenericAPIView) :
    authentication_classes=[]
    serializer_class = LoginSerializer
    def post(self,request) :
        email = request.data.get('email',None)
        password = request.data.get('password',None)
        
        user = authenticate(username=email,password=password)
        
        if user :
            
            serializer =  self.serializer_class(user)
            
            return response.Response(serializer.data,status=status.HTTP_200_OK)
        return response.Response({'message':"Invaild credentials,try again"},status=status.HTTP_401_UNAUTHORIZED)
```



### JWT

```python
from rest_framework.authentication import get_authorization_header,BaseAuthentication
from rest_framework import exceptions
import jwt
from django.conf import settings

from authentication.models import User

class JWTAuthentications(BaseAuthentication) :
    
    def authenticate(self, request):
        print(request.data)
        #요청에서 header를 가져온다. 
        auth_header = get_authorization_header(request)
        print(auth_header)
        #받은 header를 utf-8로 디코딩한다. 
        auth_data = auth_header.decode('utf-8')
        print(auth_data)
        #token 형식이 Bearer + Token 이므로, ' '로 나눈다. 
        auth_token = auth_data.split(' ')
        print(auth_token)
        
        #토큰이 있는 리스트 길이가 2여야 하는데, 그렇지 않으면 유효하지 않은 토큰 
        if len(auth_token)!=2 :
            raise exceptions.AuthenticationFailed('Token not valid')
        
        #토큰만 취한다. 
        token=auth_token[1]
        
        try:
            #토큰과 SECRET_KEY, 발급시 사용한 알고리즘을 이용해서 디코딩한다. 
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')
            print(payload)
            #디코딩 결과로 얻은 username으로 유저 정보를 가져온다. 
            username=payload['username']
            
            
            user=User.objects.get(username=username)
            
            return (user,token)
            
        #만료된 토큰일경우 예외처리 
        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed('Token is expired, login again')
        
        #디코딩 에러일 경우 예외처리 
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed('Token is invalid')
        
        #토큰 정보로 가져온 User가 존재하지 않을 경우 예외처리 
        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed(
                'No Search user'
            )
        
        
        return super().authenticate(request)
```



## List/Create API View

- APIView를 상속받아 간단히, 게시글을 작성하고 조회할 수 있다.

### Model

```python
class Todo(TrackingModel) :
    
    title = models.CharField(max_length=255)
    desc = models.TextField()
    is_complete = models.BooleanField(default=False)
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    
    def __str__(self) :
        return self.title
```

- is_complete는 Todo를 만들 때 기본적으로 False로 설정해, Todo를 생성 시 기본적으로 끝나지 않은 상태로 등록한다.
- Todo의 주인은 Todo를 생성한 User를 참조해서 등록한다. 

### Serializer

```python
class TodoSerializer(ModelSerializer) :
    
    class Meta:
        model=Todo
        
        fields = ('title','desc','is_complete',)
```

- is_complete 는 default 값이 있기 때문에, title과 desc를 입력받게 하고, 직렬화 필드를 거치면, 해당 3가지 필드를 serializer에 담아서 응답을 보낸다. 

### Create

```python
class CreateTodoAPIView(CreateAPIView) :
    
    serializer_class =TodoSerializer
    permission_classes=(IsAuthenticated,)
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
```

- CreateAPIView는 mixins.CreateModelMixin과 GenericAPIView를 상속받는다.

```python
# CreateAPIView
class CreateAPIView(mixins.CreateModelMixin,
                    GenericAPIView):
    """
    Concrete view for creating a model instance.
    """
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
#mixins.CreateModelMixin
class CreateModelMixin:
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
```

- 데이터가 POST 요청으로 들어오면, serializer 필드에 요청된 데이터를 넣고, 모델에 새로운 Instance를 추가한다. 
- post 요청을 받으면, 넘어온 데이터로 create를 진행한다.
- create는 CreateModelMixin class에서 상속받는데, serializer_classs에서 선언한 직렬화기로, 직렬화를 진행한다.
- 유효성 검사를 끝내면 perform_create 함수에 직렬화가 끝낸 정보를 넣어주는데, 이를 custom 하여, 요청한 user를 owner로 선언해준다. 

### List

```python
class TodoListAPIView(ListAPIView) :
    
    serializer_class = TodoSerializer
    permission_classes=(IsAuthenticated,)
    
    
    queryset=Todo.objects.all()
    
    
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)
```

- List API View는 get 요청에 대해 queryset 형태로 데이터를 리턴하는 클래스이다.

- 해당 클래스에는 필수적으로 queryset을 정의해야 하며, 이를 정의하면 다른 override 없이 queryset을 리턴한다.

    - ```python
        class TodoListAPIView(ListAPIView) :
         
            serializer_class = TodoSerializer
            queryset=Todo.objects.all()
        ```

- 하지만 queryset에 대해서 custom하여 request에 담긴 data를 가지고 오고 싶은 경우 get_queryset 함수를 재정의 하여 해결할 수 있다.

    - ```python
        class TodoListAPIView(ListAPIView) :
            
            serializer_class = TodoSerializer
            def get_queryset(self):
                return Todo.objects.filter(owner=self.request.user)
        ```

- 해당 TodoListAPIView의 경우 get_queryset을 재정의 했기 때문에, queryset을 요청하지 않아도 되며, queryset 요청에 대해 요청한 유저가 작성한 유저인 경우에만 불러온다. 

- 일반적으로 queryset을 사용하여 보다 깔끔히 표시하지만, **request에서 data를 가져와야 할 경우에는 필수적으로 get_queryset을 사용**해야한다.

#### Stackoverflow 참고 글 

https://stackoverflow.com/questions/19707237/use-get-queryset-method-or-set-queryset-variable

- `queryset`서버를 시작할 때 쿼리 세트가 한 번만 생성되며, 반면 `get_queryset`에 모든 요청에 대해 메서드가 호출된다.

    - 유용한 또 다른 예 `get_queryset`는 콜러블을 기반으로 필터링하려는 경우입니다. 예를 들어 오늘의 투표를 반환합니다.

        ```python
        class IndexView(generic.ListView):
            def get_queryset(self):
                """Returns Polls that were created today"""
                return Poll.active.filter(pub_date=date.today())
        ```

        queryset를 설정하여 동일한 작업을 시도 하면 뷰가 로드될 때 `queryset`의 `date.today()`가 한 번만 호출되고 잠시 후 뷰가 잘못된 결과를 표시합니다.

        ```haskell
        class IndexView(generic.ListView):
            # don't do this!
            queryset = Poll.active.filter(pub_date=date.today())
        ```

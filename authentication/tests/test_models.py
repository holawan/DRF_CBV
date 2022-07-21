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
        
    
        
    
        
    
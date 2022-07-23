
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from todos.models import Todo

class TodosAPITestCase(APITestCase) :
    #todo 생성하기 
    def create_todo(self) :
        #title과 desc를 입력
        sample_todo={'title':"Hello","desc":"Test"}
        #todo를 생성하기 
        response = self.client.post(reverse('todos'),sample_todo)
        #생성후 반환받은 값을 response로 return 하기 
        return response
        
    #인증 
    def authenticate(self) :
        #회원가입 
        self.client.post(reverse("register"),{'username':"username",'password':'password','email':'email@gmail.com'})
        #login 후 받은 toekn을 response에 저장 
        response=self.client.post(reverse('login'),{'username':"username",'password':'password','email':'email@gmail.com'})
        #token을 이용한 인증 진행하기 
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")

class TestListCreateTodos(TodosAPITestCase) :
    # def create_todo(self) :
    #     sample_todo={'title':"Hello","desc":"Test"}
    #     response = self.client.post(reverse('todos'),sample_todo)
        
    #     return response
        
    # def authenticate(self) :
    #     self.client.post(reverse("register"),{'username':"username",'password':'password','email':'email@gmail.com'})
        
    #     response=self.client.post(reverse('login'),{'username':"username",'password':'password','email':'email@gmail.com'})
        
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")
    
    #인증되지 않은 사용자의 todo 작성 
    def test_should_not_creates_todo_with_no_auth(self) :
        response = self.create_todo()
        # 인증되지 않았기 때문에 403 에러를 반환
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    
    #
    def test_should_create_todo(self) :
        #현재 데이터베이스의 Todo 객체의 개수 가져오기 
        previous_todo_count = Todo.objects.all().count()
        #인증하기 
        self.authenticate()
        #todo 만들고 return을 response에 저장하기 
        # sample_todo={'title':"Hello","desc":"Test"}
        response = self.create_todo()
        
        # 게시글이 생성되었으면, previous_todo_count에서 1을 더한 값과 일치할 것이다. 
        self.assertEqual(Todo.objects.all().count(),previous_todo_count+1)
        #HTTP 응답은 201을 반환할 것이다. 
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        #title은 우리가 test한 'Hello'일 것이다. 
        self.assertEqual(response.data['title'],'Hello')
        #desc는 우리가 test한 'Test일' 것이다. 
        self.assertEqual(response.data['desc'],'Test')
        
        
    #todo 데이터 가져오기 
    def test_retrieves_all_todos(self) :
        #인증 
        self.authenticate()
        #모든 tood 데이터 가져오기 
        response= self.client.get(reverse('todos'))
        #HTTP응답은 인증 후 올바르게 코드를 넣었으면 200을 반환할 것이다. 
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        #전달받은 instance는 list일 것이다. 
        self.assertIsInstance(response.data['results'],list)

        #새로운 데이터 생성하기 
        self.create_todo()
        #모든 todo 데이터 가져오기 
        res=self.client.get(reverse('todos'))
        #pagination 기능을 사용했기 때문에, reutnr의 count 값이 있을 것이며 이는 integer일 것이다. 
        self.assertIsInstance(res.data['count'],int)
        #해당 값은 1일 것이다. 
        self.assertEqual(res.data['count'],1)
        
    
    
class TestTodoDetailAPIView(TodosAPITestCase) :
    #단일 객체 조회하기 
    def test_retrives_one_item(self) :
        
        #인증하기 
        self.authenticate()
        
        #todo 생성하기 
        response=self.create_todo()
        
        #생성한 todo의 id 값으로 조회하기 
        res = self.client.get(
                reverse('todo',kwargs={'id':response.data['id']}))
        #조회가 잘되면 200  반환 
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        
        #생성한 id 값으로 todo 객체 가져오기 
        todo = Todo.objects.get(id=response.data['id'])
        
        #가져온 객체의 title이 조회한 todo의 title과 같은지 확인하기 
        self.assertEqual(todo.title,res.data['title'])
        
    #todo 수정 
    def test_updates_one_item(self) :
        #인증하기 
        self.authenticate()
        
        #todo 생성하기 
        response=self.create_todo()
        # print(response.data)
        
        #생성한 todo를 수정하기 
        res =self.client.patch(reverse('todo',
                                       kwargs={'id':response.data['id']}),
                                        {"title":"New one",'is_complete':True})
        
        #수정이 잘 되면 200 반환 
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        #수정한 todo를 가져오기 
        updated_todo = Todo.objects.get(id=response.data['id'])
        # print(updated_todo.title)
        #수정결과와 일치하는지 확인하기 
        self.assertEqual(updated_todo.is_complete,True)
        self.assertEqual(updated_todo.title,"New one")
    
    #todo 삭제 
    def test_deletes_one_item(self) :
        #이
        self.authenticate()
        #todo 만들기 
        res =  self.create_todo()
        
        #현재 todo 개수 세기 (1개 )
        prev_db_count=Todo.objects.all().count()
        
        #현재 todo개수가, 0보다 큰가?
        self.assertGreater(prev_db_count,0)
        #현재 todo개수가 1개인가? 
        self.assertEqual(prev_db_count,1)
        
        #삭제요청 보내기 
        response = self.client.delete(
            reverse("todo",kwargs={'id':res.data['id']})
        )
        
        #삭제가 되었으면 204 반환 
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        #현재 todo개수가 0개인가?
        self.assertEqual(Todo.objects.all().count(),0)
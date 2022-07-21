from django.db import models

class TrackingModel(models.Model) :
    # 객체가 생성된 시간에 맞게 생성됨 
    created_at = models.DateTimeField(auto_now_add=True)
    # 객체가 수정될 때 마다 시간이 갱신됨 
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta :
        abstract=True
        # 생성 시간을 역정렬해서 정렬함 
        ordering=('-created_at',)
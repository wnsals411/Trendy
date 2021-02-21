from django.db import models

# Create your models here.

class TimeStamedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    
    class Meta:
        abstract = True

class Notice(TimeStamedModel):  # 공지사항용 모델 / admin사이트를 통해 관리
    title = models.CharField(max_length = 50) # 글 제목
    content = models.CharField(max_length = 500) # 내용
    image = models.ImageField(blank = True) # 이미지(사진)
    hits = models.IntegerField(default = 0) # 조회수

    def __str__(self):
        return self.title

class Qna(TimeStamedModel):
    title = models.CharField(max_length = 50) # 글 제목
    author = models.CharField(max_length = 15) # 작성자
    content = models.CharField(max_length = 500) # 내용
    image = models.ImageField(blank = True) # 이미지(사진)
    hits = models.IntegerField(default = 0) # 조회수
    password = models.CharField(max_length = 20) # 글 삭제시 필요한 비밀번호

    def __str__(self):
        return self.title
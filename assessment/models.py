from django.db import models
from django.contrib.auth.models import User
import uuid

from django.db.models.fields import related
# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Option(models.Model):
    option = models.CharField(max_length=200)

    def __str__(self):
        return self.option

class Question(models.Model):
    user =  models.ForeignKey(User , on_delete=models.CASCADE , default='')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.ForeignKey(Option , on_delete=models.CASCADE , related_name='answer')
    option = models.ManyToManyField(Option)
    # option_one = models.CharField(max_length=200)
    # option_two = models.CharField(max_length=200)
    # option_three = models.CharField(max_length=200 , blank=True)
    # option_four = models.CharField(max_length=200 , blank=True)

    def __str__(self):
        return f"{self.subject}-{self.question}"

class QuestionPaper(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject , on_delete=models.CASCADE , default='')
    question_paper_id = models.CharField(max_length=12)
    question_ids = models.CharField(max_length=1000)
    marks_per_question = models.FloatField(default=1)

    # def QPID(self):
    #     code = str(uuid.uuid4()).replace("-" , "")[:12]
    #     self.question_paper_id = code
    #     self.save()
    # question_paper_id = property(QPID)

    def __str__(self):
        return f"{self.question_paper_id}"


class QuizResults(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    quiz_code = models.CharField(max_length=20 , default='')
    teacher = models.ForeignKey(User , on_delete=models.CASCADE , related_name = "teacher" , default = '')
    actual_quiz_answers = models.CharField(max_length=1000)
    submitted_quiz_answers = models.CharField(max_length=1000)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.user}"
    

class Instruction(models.Model):
    inst = models.TextField(max_length=1000)

    def __str__(self):
        return self.inst[:20]



class Answer(models.Model):
    sender = models.ForeignKey(User , on_delete=models.CASCADE , related_name="sender_id")
    reciever = models.ForeignKey(User , on_delete=models.CASCADE , related_name="reciever_id")
    question = models.ForeignKey(Question , on_delete=models.CASCADE , related_name="quest")
    doubt_id = models.ForeignKey('Doubt' , on_delete=models.CASCADE , related_name="doubtquestion")
    answer = models.TextField(max_length=5000)

    def __str__(self):
        return self.answer
    
class Doubt(models.Model):
    sender = models.ForeignKey(User , on_delete=models.CASCADE , related_name="sender")
    reciever = models.ForeignKey(User , on_delete=models.CASCADE , related_name="reciever")
    question = models.ForeignKey(Question , on_delete=models.CASCADE , related_name="ques")
    qu = models.TextField(max_length=2000)
    
    def __str__(self):
        return self.qu
    

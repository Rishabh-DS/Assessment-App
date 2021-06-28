from functools import partial
from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.models import User
from . models import Instruction, QuizResults, Subject , Question , QuestionPaper , Doubt , Answer
from .serializers import DoubtSerializer, InstructionSerializer, QuestionPaperSerializer, QuestionSerializer, QuizResultsSerializer, SignupSerializer , SubjectSerializer, LoginSerializer , AnswerSerializer
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import uuid
import ast
from django.db.models import Q

from assessment import serializers


class AddSubjectViewSet(viewsets.ViewSet):
    def list(self,request):
        subject = Subject.objects.all()
        serializer = SubjectSerializer(subject , many=True)
        return Response(serializer.data)

    def create(self,request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class QuizDoneViewSet(viewsets.ViewSet):
    def list(self,request):
        return Response({"msg":"Hello World!"})

    def create(self,request):
        data = request.data
        submitted_ans = data['submitted_quiz_answers']
        quiz_code = data['quiz_code']
        quiz = QuestionPaper.objects.get(question_paper_id=quiz_code)
        marks_per_question = quiz.marks_per_question
        ques_id_list = ast.literal_eval(quiz.question_ids)
        actual_ans = []
        for i in ques_id_list:
            ques = Question.objects.get(id = i)
            ans = ques.answer.option
            actual_ans.append(ans)
        teacher = quiz.user
        marks=0
        submitted_ans_list = submitted_ans.strip('][').split(', ')
        for i in range(len(actual_ans)):
            if actual_ans[i]==submitted_ans_list[i]:
                marks+=marks_per_question
        data['teacher'] = teacher.id
        data['marks'] = marks
        data['actual_quiz_answers'] = str(actual_ans)
        data['quiz_code'] = quiz_code
        serializer = QuizResultsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class InstructionsViewSet(viewsets.ViewSet):
    def list(self,request):
        inst = Instruction.objects.get(id=1)
        serializer = InstructionSerializer(inst)
        return Response(serializer.data)

    def create(self,request):
        data = request.data
        try:
            ques_paper = QuestionPaper.objects.get(question_paper_id = data['code'])
            serializer = QuestionPaperSerializer(ques_paper)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class CreateQuestionPaperViewSet(viewsets.ViewSet):
    def list(self,request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions , many=True)
        return Response(serializer.data)

    def create(self,request):
        code = str(uuid.uuid4()).replace("-" , "")[:12]
        data = request.data
        data['question_paper_id'] = code
        serializer = QuestionPaperSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class YourQuestionPaperViewSet(viewsets.ViewSet):
    def list(self,request):
        user = request.user
        quespaper = QuestionPaper.objects.filter(user=user)
        serializer = QuestionPaperSerializer(quespaper , many=True)
        return Response(serializer.data)

    def update(self,request , pk):
        code = pk
        quiz = QuestionPaper.objects.get(question_paper_id=code)
        serializer = QuestionPaperSerializer(quiz , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Updated' , 'data':serializer.data} , status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self,request,pk):
        code = pk
        quiz = QuestionPaper.objects.get(question_paper_id=code)
        serializer = QuestionPaperSerializer(quiz , data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Updated' , 'data':serializer.data} , status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class ViewQuestionPaperViewSet(viewsets.ViewSet):
    def list(self,request):
        return Response({"msg":"Hello"})

    def retrieve(self,request , pk=None):
        id = pk
        if id is not None:
            questions = QuestionPaper.objects.get(question_paper_id=pk)
            quesids = questions.question_ids
            queslist = ast.literal_eval(quesids)
            a = []
            for q in queslist:
                ques= Question.objects.get(id=q)
                a.append(ques)
            serializer = QuestionSerializer(a , many=True)
            return Response(serializer.data)


class AddQuestionsViewSet(viewsets.ViewSet):
    def list(self,request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions , many=True) 
        return Response(serializer.data)

    def retrieve(self,request,pk):
        question = Question.objects.get(id=pk)
        serializer = QuestionSerializer(question) 
        return Response(serializer.data)

    def create(self,request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def update(self,request , pk):
        id = pk
        ques = Question.objects.get(id=id)
        serializer = QuestionSerializer(ques , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Question Updated" , "data":serializer.data} , status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self,request,pk):
        id = pk
        ques = Question.objects.get(id=id)
        serializer = QuestionSerializer(ques , data = request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Question Updated" , "data":serializer.data} , status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk):
        id=pk
        stu = Question.objects.get(id=id)
        stu.delete()
        return Response({'msg':'Question deleted'})

class DoubtViewSet(viewsets.ViewSet):
    def list(self , request):
        answers = Answer.objects.filter(reciever = request.user)
        serializer = AnswerSerializer(answers , many=True)
        return Response(serializer.data)
    def create(self,request):
        data = request.data
        ques = Question.objects.get(id = data['question'])
        data['sender'] = request.user.id
        data['reciever'] = ques.user.id
        serializer = DoubtSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class AnswerViewSet(viewsets.ViewSet):
    def list(self,request):
        doubts = Doubt.objects.filter(reciever = request.user)
        serializer = DoubtSerializer(doubts , many=True)
        return Response(serializer.data)

    def create(self,request):
        data = request.data
        data['sender'] = request.user.id
        # data['reciever'] = data['doubt_id'].sender
        # data['question'] = data['doubt_id'].question
        doubt_id = data['doubt_id']
        doubt = Doubt.objects.get(id=doubt_id)
        data['reciever'] = doubt.sender.id
        data['question'] = doubt.question.id
        serializer = AnswerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ViewSet):
    def list(self,request):
        return Response({"Massage":"Enter your credentials Here"})

    def create(self,request):
        data = request.data
        username = data['username']
        password = data['password']
        loginusername = username
        loginpassword = password
        user = authenticate(username = loginusername , password = loginpassword)
        if user is not None:
            login(request , user)
            serializer = LoginSerializer(user)
            return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"msg":"Invalid credentials, Please try again."})


class LogoutViewSet(viewsets.ViewSet):
    def list(self,request):
        logout(request)
        return Response({"msg":"Successfully Logged out"} , status=status.HTTP_401_UNAUTHORIZED)


class SignupViewSet(viewsets.ViewSet):
    def list(self,request):
        return Response({"msg":"Please enter your details here to signup."})
    
    def create(self,request):
        data = request.data
        email = data['email']
        username = data['username']
        pass1 = data['password1']
        pass2 = data['password2']
        check_user = User.objects.filter(email=email).first()
        if check_user:
            return Response({"message":"User Already exists"})
        if pass1!=pass2:
            return Response({"message":"Passwords do not match"})
        if not username.isalnum():
            return Response({"message":"Username must have only alphanumeric characters"})
        newuser = User.objects.create_user(username , email , pass1)
        userdata = {}
        userdata['first_name'] = data['first_name']
        userdata['last_name'] = data['last_name']
        serializer = SignupSerializer(newuser , data = userdata , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


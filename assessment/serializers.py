from django.db.models import fields
from rest_framework import serializers
from .models import Answer, Doubt, Instruction, Option, Subject , Question , QuestionPaper , QuizResults
from django.contrib.auth.models import User

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['option']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id' , 'user','subject' , 'question' , 'answer' , 'option']


class QuestionPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionPaper
        fields = ['user' , 'subject' , 'question_paper_id' , 'question_ids' , 'marks_per_question']


class QuizResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResults
        fields = ['user' , 'quiz_code' , 'teacher' , 'actual_quiz_answers' , 'submitted_quiz_answers' , 'marks']


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ['inst']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'email']


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'email' , 'first_name' , 'last_name' , 'password']

class DoubtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doubt
        fields = ['sender' , 'reciever' , 'question' , 'qu']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['sender' , 'reciever' , 'question' , 'doubt_id' , 'answer']

from django.urls import path , include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('addsub', views.AddSubjectViewSet , basename = "addsub")
router.register('quizdone', views.QuizDoneViewSet , basename = "quizdone")
router.register('instructions', views.InstructionsViewSet , basename = "Instructions")
router.register('createquespaper', views.CreateQuestionPaperViewSet , basename = "Create Question Paper")
router.register('yourquestionpaper', views.YourQuestionPaperViewSet , basename = "Your Question Paper")
router.register('viewques', views.ViewQuestionPaperViewSet , basename = "View Question Paper")
router.register('addques', views.AddQuestionsViewSet , basename = "Add Questions")
router.register('doubt', views.DoubtViewSet , basename = "Doubts")
router.register('answer', views.AnswerViewSet , basename = "Answer")
router.register('login', views.LoginViewSet , basename = "Login")
router.register('logout', views.LogoutViewSet , basename = "Logout")
router.register('signup', views.SignupViewSet , basename = "Signup")

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path

from auth.views import SignUpView, SignInView, TokenView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/token', TokenView.as_view())
]

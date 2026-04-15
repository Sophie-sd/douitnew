from django.urls import path

from .views import QuizPageView, ThankYouView, submit_footer, submit_lead, submit_modal

app_name = "leads"

urlpatterns = [
    path("submit/", submit_lead, name="submit"),
    path("submit-footer/", submit_footer, name="submit_footer"),
    path("submit-modal/", submit_modal, name="submit_modal"),
    path("dyakuyemo/", ThankYouView.as_view(), name="thank_you"),
    path("rozrahunok/", QuizPageView.as_view(), name="quiz_page"),
]

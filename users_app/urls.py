from django.urls import path
from users_app import views
from users_app.models import LogMessage

home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="users_app/users_app.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("log/", views.log_message, name="log"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("register", views.user_register, name='register'),
    path("profile", views.user_profile, name='profile')
]
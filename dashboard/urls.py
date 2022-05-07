from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path("",views.home,name='home'),
    path("notes/",views.notes,name='notes'),
    path("notes/<id>",views.notes_details,name='notes_details'),
    path("note_update/<id>",views.note_update,name='note_update'),
    path("note_delete/<id>",views.note_delete,name='note_delete'),


    path("login/",views.login_user,name='login_user'),
    path("register/",views.user_register,name='user_register'),
    path("logout/",views.logout_user,name='logout_user'),

    path("homework/",views.homework,name='homework'),
    path("homework_delete/<id>",views.homework_delete,name='homework_delete'),
    path("update_homework/<id>",views.update_homework,name='update_homework'),

    path("youtube/",views.youtube,name='youtube'),

    path("todo/",views.todolist,name='todo'),
    path("update_todo/<id>",views.update_todo,name='update_todo'),
    path("delete_todo/<id>",views.delete_todo,name='delete_todo'),

    path("books/",views.books,name='books'),

    path("dictionary/",views.dictionary,name='dictionary'),

    path("wiki/",views.wiki,name='wiki'),

    path("conversion/",views.conversion,name='conversion'),
    path("profile/",views.profile,name='profile'),

]
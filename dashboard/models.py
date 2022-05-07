
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def snipet(self):
        return self.description[0:100]

    def get_absolute_url(self):
        return reverse("dashboard:notes_details",kwargs={
            'id':self.id
        })

    def get_update_notes_url(self):
        return reverse("dashboard:note_update",kwargs={
            'id':self.id
        })

    def get_delete_note_url(self):
        return reverse("dashboard:note_delete",kwargs={
            'id':self.id
        })



class HomeWork(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.subject


    def get_delete_homework_url(self):
        return reverse("dashboard:homework_delete",kwargs={
            'id':self.id
        })

    def get_update_homework_url(self):
        return reverse("dashboard:update_homework",kwargs={
            'id':self.id
        })

class TodoList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add = True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_update_todo_url(self):
        return reverse("dashboard:update_todo",kwargs={
            'id':self.id
        })

    def get_delete_todo_url(self):
        return reverse("dashboard:delete_todo",kwargs={
            'id':self.id
        })

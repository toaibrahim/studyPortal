
from isodate import parse_duration
import requests
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from youtubesearchpython import VideosSearch
from django.conf import settings
import wikipedia


# Create your views here.

@login_required(login_url='/login')
def home(request):
    return render(request,'dashboard/home.html')



def notes(request):
    author = request.user
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.instance.user = author
            form.save()
            messages.success(request,'Note have been added successfully')
            return redirect("/notes")
    else:
        form = NoteForm()
    notes = Notes.objects.filter(user = request.user)
    context = {
        'notes':notes,
        'form' : form
    }
    return render(request,'dashboard/notes.html',context)


def note_update(request,id):
    title = 'Update'
    note = get_object_or_404(Notes, id=id)
    form = NoteForm(
        request.POST or None,
        request.FILES or None,
        instance=note)
    author = request.user
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = author
            form.save()
            messages.success(request,'Your note Have been updated')
            return redirect("/notes")
    context = {
        'title': title,
        'form': form
    }
    return render(request, "dashboard/notes.html", context)


def note_delete(request,id):
    note = get_object_or_404(Notes,id =id)
    note.delete()
    messages.success(request,'Your note have been deleted')
    return redirect('/notes')




def notes_details(request,id):
    note = Notes.objects.filter(user=request.user,id=id)
    context={
        'note':note
    }
    return render(request,'dashboard/notes_detail.html',context)




def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have been loggedin successfully!")
            return redirect("/")
        else:
            messages.error(request,"Something went wrong please try again")
            return redirect("/login")
    return render(request,'dashboard/login.html')


def user_register(request):
    if request.method == "POST":
         form = RegisterForm(request.POST)
         if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request,username=username,password=password)
            login(request,user)
            messages.success(request,"You have been registered successfully!")
            return redirect("/")
    else:
        form = RegisterForm() 
        

    context = {
        'form':form
    }
    return render(request,"dashboard/register.html",context)

@login_required(login_url = "/login")
def logout_user(request):
    logout(request)
    return redirect("/login")




def homework(request):
    homework = HomeWork.objects.filter(user=request.user)
    author = request.user
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            form.instance.user = author
            form.save()
            messages.success(request,"Homework added successfully!")
            return redirect('/homework')
    else:
        form = HomeworkForm()

    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    context = {
        'homework':homework,
        'homework_done':homework_done,
        'form':form
    }
    return render(request,'dashboard/homework.html',context)



def homework_delete(request,id):
    homework = get_object_or_404(HomeWork,id=id)
    homework.delete()
    return redirect("/homework")


def update_homework(request,id):
    homework = get_object_or_404(HomeWork,id=id)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished=True

    homework.save()
    return redirect("/homework")


def youtube(request):
    videos = []
    if request.method == "POST":
        query = request.POST['text']
        form = DashForm(request.POST)
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': query,
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults':10,
            'type': 'video'
        }
        video_ids = []
        r = requests.get(search_url,params = search_params)
        results = r.json()['items']
        for result in results:
            video_ids.append(result['id']['videoId'])

        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet,contentDetails',
            'id': ','.join(video_ids),
            'maxResults':10,
        }
        r = requests.get(video_url,params=video_params)
        results = r.json()['items']
        
        for result in results:
            video_date = {
                'link': f'https://www.youtube.com/watch?v={ result["id"] }',
                'title': result['snippet']['title'],
                'description': result['snippet']['description'][:100],
                #'channel': result['snippet']['channel'],
                'id': result['id'],
                'duration': parse_duration(result['contentDetails']['duration']),
                'thumbnail': result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_date)

        context = {
            'videos': videos,
            
        }
    else:
        form = DashForm()
        context = {
            'form':form
        }
    return render(request,"dashboard/youtube.html",context)


def todolist(request):
    alltodo = TodoList.objects.filter(user=request.user)
    author = request.user
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.instance.user = author
            form.save()
            messages.success(request,"Todo added successfully")
    else:
        form = TodoForm()
    context = {
        'form':form,
        'alltodo':alltodo
    }
    return render(request,"dashboard/todo.html",context)


def update_todo(request,id):
    gettodo = get_object_or_404(TodoList,id = id)

    if gettodo.is_completed == True:
        gettodo.is_completed = False
    else:
        gettodo.is_completed = True
    gettodo.save()
    messages.success(request,"Todo list is updated")
    return redirect("/todo")

def delete_todo(request,id):
    gettodo = get_object_or_404(TodoList,id = id)

    gettodo.delete()
    messages.success(request,"Your todo is deleted")
    return redirect("/todo")


def books(request):
    if request.method == "POST":
        form = DashForm(request.POST)
        query = request.POST['text']
        url = 'https://www.googleapis.com/books/v1/volumes?q='+query

        r = requests.get(url)
        results = r.json()
        result_list = [] 
        
        for i in range(10):
            result_dict = {
                'title':results['items'][i]['volumeInfo']['title'],
                'subtitle':results['items'][i]['volumeInfo'].get('subtitle'),
                'description':results['items'][i]['volumeInfo'].get('description')[0:300],
                'count':results['items'][i]['volumeInfo'].get('pageCount'),
                'categories':results['items'][i]['volumeInfo'].get('categories'),
                'rating':results['items'][i]['volumeInfo'].get('pageCount'),
                'thumbnail':results['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':results['items'][i]['volumeInfo'].get('previewLink'),

            }

            result_list.append(result_dict)

        context = {
            'result_list': result_list,
            
        }
        return render(request,"dashboard/books.html",context)

    else:
        form = DashForm()
        context = {
            'form':form
        }
    return render(request,"dashboard/books.html",context)


def dictionary(request):
    if request.method == "POST":
        form = DashForm(request.POST)
        query = request.POST['text']
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/'+query

        r = requests.get(url)
        results = r.json()
        try:
            phonetics = results[0]['phonetics'][0]['text']
            audio = results[0]['phonetics'][0]['audio']
            definition = results[0]['meanings'][0]['definitions'][0]['definition'],
            example = results[0]['meanings'][0]['definitions'][0]['example'],
            synonyms = results[0]['meanings'][0]['definitions'][0]['synonyms'],

            context = {
                'form':form,
                'input':query,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context = {
                'form':form,
                'input':'',
            }
        return render(request,"dashboard/dictionary.html",context)
    else:
        form = DashForm()
        context = {
            'form':form
        }
    return render(request,"dashboard/dictionary.html",context)


def wiki(request):
    
    if request.method == "POST":
        query = request.POST['text']
        form = DashForm(request.POST)
        search = wikipedia.page(query)
       
        context ={
            'form':form,
            'query':query,
            'title' : search.title,
            'link' :search.url,
            'details' : search.summary
        }
       

        return render(request,"dashboard/wiki.html",context)
    else:
       form = DashForm()
       context = {
          'form':form
       }
    return render(request,"dashboard/wiki.html",context)


def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == "length":
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input}yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                    context = {
                        'form':form,
                        'm_form':measurement_form,
                        'input':True,
                        'answer':answer
                    }
        if request.POST['measurement'] == "mass":
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.2062} pound'
                    context = {
                        'form':form,
                        'm_form':measurement_form,
                        'input':True,
                        'answer':answer
                    }
    else:
        form = ConversionForm()
        context = {
            'form':form
        }
    return render(request,'dashboard/conversion.html',context)


def profile(request):
    homework = HomeWork.objects.filter(is_finished=False,user = request.user)
    todos = TodoList.objects.filter(is_completed=False,user = request.user)
    context = {
        'homework':homework,
        'todos':todos
    }
    return render(request,"dashboard/profile.html",context)


def error_404_view(request,exception):
    return render(request,'dashboard/404.html')


    
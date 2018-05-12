from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.tokens import default_token_generator

# Django transaction system so we can use @transaction.atomic
from django.db import transaction
from django.template.loader import render_to_string

from django.http import Http404, HttpResponse
# Imports the Item class
from hypermap.models import *

# import time
import datetime

# import forms
from hypermap.forms import *

# used to send email with Django
from django.core.mail import send_mail

from django.views.decorators.csrf import ensure_csrf_cookie

from django.db.models import Q
# Create your views here.

@login_required
@ensure_csrf_cookie  # Gives CSRF token for later requests.
def home(request):
    context = {}
    context['form'] = PostForm()
    # News.objects.all().delete()
    # context['items'] = News.objects.all()
    return render(request, 'hypermap/global_page.html', context)

@transaction.atomic
def registration(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = Registration()
        return render(request, 'hypermap/registration_page.html', context)

    # Create form for post method
    form = Registration(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'hypermap/registration_page.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'])
    new_profile = Profile(user = new_user)
    new_user.save()
    new_profile.save()

#     # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    

    # print(1)
    token = default_token_generator.make_token(new_user)
    email_body = """
    Welcome to the Hypermap. Please click the link below to verify your email address:
    http://%s%s
    """%(request.get_host(),
         reverse('confirmation', args=(new_user.id, token)))
    send_mail(subject="Verify your email address",
            message = email_body,
            from_email="xianlal@andrew.cmu.edu",
            recipient_list=[new_user.email])
    # print(2)
    return redirect('global')

@transaction.atomic
@login_required
def confirm_registration(request, id, token):
    # check user and token
    try:
        # print(id)
        # print(token)
        user = User.objects.get(id=id)

    except ObjectDoesNotExist:
        # print('user does not exist.')
        raise Http404

    if not default_token_generator.check_token(user, token):
        # print('dont match')
        raise Http404

    user.profile.confirmed = True
    # print(user.profile.confirmed)
    user.save()
    user.profile.save()
    # profile.save()
    login(request, user)
    info = "Your registration has been confirmed. Let's GET HIGH!!"
    return render(request, "hypermap/show_info.html", {"info":info})

@login_required
def add_event(request):
    try:
        user = request.user
    except ObjectDoesNotExist:
        return Http404
    context = {}
    context["fullName"] = "%s %s" % (request.user.first_name, 
                                    request.user.last_name)

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = PostForm()
        return render(request, 'hypermap/global_page.html', context)

    # Create form for post method
    form = PostForm(request.POST, request.FILES)
    context['form'] = form
    # print("adding event")
    if form.is_valid():
        # print(form.cleaned_data)
        # print form.cleaned_data['post_type']

        if form.cleaned_data['post_type'] == "1":
            # print "News is created"
            new_event = News(user = request.user,
                    share_to = form.cleaned_data['share_to'],
                    lat = form.cleaned_data['lat'],
                    lng = form.cleaned_data['lng'],
                    title = form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    # file=form.cleaned_data['image'],
                    contact_info = request.user.email,
                    post_time = datetime.datetime.now(),
                    flag = 1)
        elif form.cleaned_data['post_type'] == "3":
            new_event = Help(user = request.user,
                            share_to = form.cleaned_data['share_to'],
                            lat = form.cleaned_data['lat'],
                            lng = form.cleaned_data['lng'],
                            title = form.cleaned_data['title'],
                            description=form.cleaned_data['description'],
                            # file=form.cleaned_data['image'],
                            contact_info = request.user.email,
                            start_time = form.cleaned_data['start_date'],
                            end_time = form.cleaned_data['end_date'],
                            post_time = datetime.datetime.now(),
                            flag = 3)
        else:
            # print form.cleaned_data['post_type']
            new_event = Event(user = request.user,
                            share_to = form.cleaned_data['share_to'],
                            lat = form.cleaned_data['lat'],
                            lng = form.cleaned_data['lng'],
                            title = form.cleaned_data['title'],
                            description=form.cleaned_data['description'],
                            # file=form.cleaned_data['image'],
                            contact_info = request.user.email,
                            start_time = form.cleaned_data['start_date'],
                            end_time = form.cleaned_data['end_date'],
                            register_required =form.cleaned_data['register_required'],
                            post_time = datetime.datetime.now(),
                            flag = 2)
        if form.cleaned_data['image'] != None:
            new_event.image = form.cleaned_data['image']
        new_event.save()
    return redirect('global')

@login_required
def get_items(request, time="1970-01-01T00:00+00:00"):
    items = News.objects.all()
    context = {"items":items}
    return render(request, 'hypermap/items.json', context, 
        content_type='application/json')

@login_required
def get_ce(request, id): #corresponding events
    # print (request.GET['id'])
    # lat, lng = request.GET['lat'], request.GET['lng']
    item = News.objects.get(id=id)
    like = item.liked_by.count()
    liked = True if request.user.profile.like.filter(id = id).count() > 0 else False
    html = render_to_string("hypermap/event.html",\
                                {"item":item, "like": like, "liked": liked},
                                request = request)
    # print(html)
    context = {"html":html}
    return render(request, 'hypermap/event.json', context,
         content_type='application/json')

@login_required
def profile1(request, id = -1):
    context = {}
    try:
        if id == -1: 
            other_user = request.user
        else:
            other_user = User.objects.get(id = id)
    except ObjectDoesNotExist:
        return Http404
    context['user'] = other_user
    # flag 0 for me, 1 for friends, 2 for not friends, 3 for sent
    if other_user == request.user: 
        context['flag'] = 0 
    elif request.user.profile in other_user.profile.friends.all():
        context['flag'] = 1
    elif request.user.profile in other_user.profile.friend_request.all():
        context['flag'] = 3
    else: 
        context['flag'] = 2
    context['items'] = other_user.profile.like.all().order_by("-post_time")
    # context['liked_items'] = user.profile.like.all().order_by("-post_time")
    return render(request, 'hypermap/profile_page.html', context)

# @login_required
# def profile1(request, id):
#     return 42
@login_required
def trending(request):
    context = {}
    context['items'] = News.objects.all().order_by("-click")
    return render(request, 'hypermap/trending_page.html', context)

@login_required
def like(request, id):
    user = request.user
    try:
        item = News.objects.get(id = id)
    except ObjectDoesNotExist:
        raise Http404

    #if this user already liked this news/event/request
    if user.profile.like.filter(id = id).count() > 0:
        user.profile.like.remove(item)
        item.click = item.click-1
    else:
        user.profile.like.add(item)
        item.click = item.click+1
        create_like_note(item, request.user)

    user.profile.save()
    user.save()
    item.save()

    liked = 1 if request.user.profile.like.filter(id = id).count() > 0 else 0
    item = News.objects.get(id=id)
    count = item.liked_by.count()
    # html = render_to_string("hypermap/event.html",\
    #                             {"item":item, "like": like, "liked": liked},
    #                             request = request)
    # print(html)
    # context = {"html":html}
    # print (item)
    return render(request, 'hypermap/like.json', {"liked": liked, "count": count},
         content_type='application/json')

def create_like_note(item, user):
    owner = item.user
    time = datetime.datetime.now()
    if item.flag == 1: 
        s = "%s %s liked your News %s" % (user.first_name, user.last_name,
                                                item.title)
    elif item.flag == 2:
        s = "%s %s liked your Event %s" % (user.first_name, 
                                                user.last_name,
                                                item.title)
    else:
        s = "%s %s liked your Help request %s" % (user.first_name, 
                                                        user.last_name,
                                                        item.title)
    note = Notification(user = owner, sender = user, 
                        content = s, date = time)
    note.save()
    # return note

@login_required
def search_page(request):
    form = SearchForm()
    return render(request, 'hypermap/search_page.html', {"form": form})

@login_required
def search_page(request):
    context = {}
    try:
        user = request.user
    except ObjectDoesNotExist:
        return Http404

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = SearchForm()
        return render(request, 'hypermap/search_page.html', context)
    form = SearchForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'hypermap/search_page.html', context)

    # do search
    key = form.cleaned_data['key_word']
    # print(key)
    ## found related events
    items1 = News.objects.filter(Q(title__icontains=key) | Q(description__icontains=key))
    # print("%d items found in 1" % len(items1))

    ## find related events from user
    users = User.objects.filter(Q(first_name__icontains=key) | Q(first_name__icontains=key) 
                                    | Q(email__icontains=key))
    items2 = News.objects.filter(user__in=users)
    # print("%d items found in 2" % len(items2))

    ## ordered 
    items = (items1 | items2).distinct().order_by("-post_time")

    for item in items:
        count = item.liked_by.count()
        item.html = render_to_string("hypermap/search_event.html",\
                                {"item":item, "like": count},
                                request = request)
        # print(item.html)
    context['items'] = items
    # return results
    # print("%d items found" % len(context["items"]))
    return render(request, 'hypermap/search_items.json', context, 
        content_type='application/json')

@login_required
def add_friend(request, id, flag):
    try:
        user = request.user
        other_user = User.objects.get(id = id)
        # url = request.META['HTTP_REFERER']
    except ObjectDoesNotExist:
        return Http404

    # if already friends -> remove
    if user.profile in other_user.profile.friends.all():
        other_user.profile.friends.remove(user.profile)
        print("1")
    # if request sent -> recall
    elif user.profile in other_user.profile.friend_request.all():
        other_user.profile.friend_request.remove(user.profile)
        print("2")
    elif other_user.profile in user.profile.friend_request.all():
        user.profile.friend_request.remove(other_user.profile)
        user.profile.friends.add(other_user.profile)
        user.profile.save()
    else:
        other_user.profile.friend_request.add(user.profile)
        add_friend_note(user, other_user)
    other_user.profile.save()
    return redirect('profile', id = id)

def add_friend_note(user, other_user):
    owner, sender = other_user, user
    time = datetime.datetime.now()
    s = "Hi %s: %s %s(%s) would like to add you as friend." % (owner.first_name,
                                                           sender.first_name,
                                                           sender.last_name,
                                                           sender.email)
    note = Notification(user = owner, sender = sender, 
                        content = s, date = time)
    note.save()

def accept_friend(request, id, note_id):
    # check if it is in the request_list
    try:
        user = request.user
        other_user = User.objects.get(id = id)
        note = Notification.objects.get(id = note_id)
    except ObjectDoesNotExist:
        return Http404
    note.read = True
    note.save()
    if other_user.profile in user.profile.friend_request.all():
        user.profile.friend_request.remove(other_user.profile)
        user.profile.friends.add(other_user.profile)
        user.profile.save()
        create_friend_note(user, other_user, True)
        m = "The request has been accepted. You and %s are friends now" % \
                                                        other_user.first_name
    else: # other user has recall the request
        m = "The request is expired."

    return render(request, "hypermap/show_info.html", {"info":m})

def create_friend_note(user, other_user, accept):
    sender, owner = user, other_user
    time = datetime.datetime.now()
    if accept:
        s = "Hi %s: %s %s(%s) has accept your friend request. You are \
            friends now." % (owner.first_name, sender.first_name,
                            sender.last_name, sender.email)
    else:
        s = "Hi %s: We are sorry that %s %s(%s) did not accept your friend \
            request but life if still beautiful." % (owner.first_name, 
                                                    sender.first_name,
                                                    sender.last_name, 
                                                    sender.email)
    note = Notification(user = owner, sender = sender, 
                        content = s, date = time)
    note.save()

def ignore_friend(request, id, note_id):
    # check if it is in the request_list
    # check if it is in the request_list
    try:
        user = request.user
        other_user = User.objects.get(id = id)
        note = Notification.objects.get(id = note_id)
    except ObjectDoesNotExist:
        return Http404
    note.read = True
    note.save()
    if other_user.profile in user.profile.friend_request.all():
        user.profile.friend_request.remove(other_user.profile)
        user.profile.save()
        create_friend_note(user, other_user, False)
    else: # other user has recall the request
        m = "The request is expired."

    return redirect('profile', id = request.user.id)

@login_required
def show_notes(request):
    context = {}
    try:
        context['user'] = user = request.user
        context['notes'] = notes = user.my_notes.all()
    except ObjectDoesNotExist:
        return Http404

    return render(request, "hypermap/notes_page.html", context)

@login_required
def get_notes_num(request):
    try:
        user = request.user
    except ObjectDoesNotExist:
        return Http404
    count = Notification.objects.filter(user = 
                                        user).filter(read = False).count()
    return render(request, 'hypermap/notes_num.json', {"count": count}, 
        content_type='application/json')

@login_required
def get_notes(request):
    try:
        user = request.user
    except ObjectDoesNotExist:
        return Http404
    notes = Notification.objects.filter(user = user).order_by("-date")
    for note in notes:
        if (("would like to add you as friend" in note.content) and \
            (note.sender.profile in user.profile.friend_request.all())):
            addF = 1
        elif (("would like to add you as friend" in note.content) and \
            (note.sender.profile not in user.profile.friend_request.all())):
            addF = 2
        else:
            addF = 0
        # print(not_dealt, addF)
        note.html = render_to_string("hypermap/notes.html",\
                                {"note":note, "addF": addF},
                                request = request)
    return render(request, "hypermap/notes.json", {"notes": notes}, 
                content_type='application/json')

@login_required
def read_notes(request, id):
    try:
        note = Notification.objects.get(id = id)
    except ObjectDoesNotExist:
        return Http404
    note.read = True if not note.read else False
    note.save()
    note.html = render_to_string("hypermap/note_content.html",\
                                {"note":note,},
                                request = request)
    # print(note.html)
    return render(request, "hypermap/note.json", {"note": note}, 
                content_type='application/json')


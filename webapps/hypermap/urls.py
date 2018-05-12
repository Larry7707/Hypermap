"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from hypermap import views 
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^login$', auth_views.login, {'template_name': 'hypermap/login_page.html'}, 
        name = "login"),
    url(r'^logout$', auth_views.logout_then_login, name = "logout"),
    url(r'^register$', views.registration, name = 'registration'),
    # show pages
    url(r'^global', views.home, name = 'global'),
    url(r'^my-profile', views.profile1, name = 'profile'),
    url(r'^profile/(?P<id>\d+)$', views.profile1, name = "profile"),
    url(r'^search', views.search_page, name = "search"),
    url(r'^trending', views.trending, name = "trending"),
    # hypermap functions
    url(r'^add-event', views.add_event, name='addevent'),

    # add friend
    url(r'^add-friend/(?P<id>\d+)/(?P<flag>\d+)$', views.add_friend, 
        name="addfriend"),
    url(r'^accept-friend/(?P<id>\d+)/(?P<note_id>\d+)$', views.accept_friend, 
        name="accept-friend"),
    url(r'^ignore-friend/(?P<id>\d+)/(?P<note_id>\d+)$', views.ignore_friend, 
        name="ignore-friend"),
    # notification 
    url(r'^notifications', views.show_notes, name="note"),
    url(r'^get-notes-num', views.get_notes_num, name="notesnum"),
    url(r'^get-notes', views.get_notes, name="get-notes"),
    url(r'^read-notes/(?P<id>\d+)', views.read_notes, name="read-notes"),


    # confirmation
    url(r'^confirmation/(?P<id>\d+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.confirm_registration, name='confirmation'),

    #JS 
    url(r'^get_items/?$', views.get_items),
    url(r'^get_items/(?P<time>.+)$', views.get_items),
    url(r'^get-ce/(?P<id>\d+)$', views.get_ce),
    url(r'^like/(?P<id>\d+)$', views.like, name = "like"),
]

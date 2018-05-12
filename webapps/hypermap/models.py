from django.db import models

# Create your models here.
from django.contrib.auth.models import User
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    confirmed = models.BooleanField(default = False)
    friends = models.ManyToManyField("Profile", symmetrical = True)
    friend_request = models.ManyToManyField("Profile", symmetrical = False)
    like = models.ManyToManyField("News", symmetrical = True, related_name="liked_by")

    def __unicode__(self):
        return self.user.username

    def get_user(self):
        return self.user

    # @staticmethod
    # def get_likes(self):
    #     return self.like.object.all().order_by(-)
        
class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_to = models.CharField(max_length=2, 
                                choices=(("PR", "private"),
                                         ("FR","friends"),
                                         ("GL","global")),
                                default="PR")
    click = models.IntegerField(default = 0)
    post_time = models.DateTimeField()
    # location = models.CharField(max_length=42)
    lat = models.DecimalField(max_digits=10, decimal_places=5)
    lng = models.DecimalField(max_digits=10, decimal_places=5)
    # loc_des = models.CharField(max_length=42)
    title = models.CharField(max_length=42)
    description = models.CharField(max_length=420)
    image = models.ImageField(max_length=500,
                            upload_to="hypermap/static/hypermap/media",
                            default="hypermap/static/hypermap/media/default_event.jpg")
    flag = models.IntegerField(default=0) # 1 for new, 2 for event, 3 for help
    contact_info = models.EmailField()

    
    def to_class_name(self):
        return "News"

    def __unicode__(self):
        return "%s %s" % (self.title, self.description)

    def __str__(self):
        return "%s %s" % (self.title, self.description)

    def get_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, content):
        self.__html = content
        # return self.html

class Help(News):
    start_time = models.DateField()
    end_time = models.DateField()
    solved = models.BooleanField(default=False)
    helper = models.ForeignKey(User, null = True, on_delete=models.CASCADE)

    def to_class_name(self):
        return "Help"

class Event(News):
    """docstring for Event"""
    start_time = models.DateField()
    end_time = models.DateField()
    register_required = models.BooleanField(default=False)
    registered = models.ManyToManyField(Profile, 
                                        related_name="registered_event")
    def to_class_name(self):
        return "Event"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(News, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    content = models.CharField(max_length=420)

    def __unicode__(self):
        return self.content

class Notification(models.Model):
    """docstring for Notification"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                            related_name = "my_notes")
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="sender")
    read = models.BooleanField(default=False)
    content = models.CharField(max_length = 420, default = "")
    date = models.DateTimeField(default = datetime.datetime.now())
    last_changed = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.content

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, content):
        self.__html = content
        # return self.html


        




        
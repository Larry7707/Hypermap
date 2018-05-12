from django import forms
import datetime
from django.contrib.auth.models import User
# from datetimewidget.widgets import DateTimeWidget

class Registration(forms.Form):
    email = forms.EmailField(max_length = 200,
                            required = True,
                            label = "Email",
                            widget = forms.TextInput(
                                attrs={'placeholder': 'Email',
                                'class': 'form-control', "type": "Email"}))
    first_name = forms.CharField(max_length = 200, 
                                label='First Name',
                                required = True,
                                widget = forms.TextInput(
                                attrs={'placeholder': 'First NaME',
                                'class': 'form-control', "type": "First Name"}))
    last_name = forms.CharField(max_length = 200, 
                                label='Last Name',
                                required = True,
                                widget = forms.TextInput(
                                attrs={'placeholder': 'Last NamE',
                                'class': 'form-control', "type": "Last Name"}))
    username = forms.CharField(max_length = 200, 
                                label= "Username",
                                required = True,
                                widget = forms.TextInput(
                                attrs={'placeholder': 'UserName',
                                'class': 'form-control', "type": "Username"}))
    password1 = forms.CharField(max_length = 200,
                                label = "Password",
                                required = True,
                                widget = forms.PasswordInput(
                                attrs={'placeholder': 'Password',
                                'class': 'form-control', "type": "Password"})
                                )
    password2 = forms.CharField(max_length = 200,
                                label = "Confirm Password",
                                required = True,
                                widget = forms.PasswordInput(
                                attrs={'placeholder': 'Confirm Password',
                                'class': 'form-control', "type": "Password"}))

    # Customizes form validation for the username field.
    def clean(self):
        # Confirms that the username is not already present in the
        # User model database.
        cleaned_data = super(Registration, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    def clean_email(self):
        # confirm email does not exist in the user data

        # clearned_data = super(Registraion, self).clean()
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already taken.") 
        return email

    def clean_username(self):
    # confirm email does not exist in the user data

    # clearned_data = super(Registraion, self).clean()
        username = self.cleaned_data.get("username")
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.") 

        return username


POST_CHOICES= [
    (1, 'News'),
    (2, 'Event'),
    (3, 'Ask for help'),
    ]
class PostForm(forms.Form):
    # content = forms.CharField(max_length = 42, 
    #                             label='Post',
    #                             required = True,
    #                             widget = forms.TextInput(
    #                             attrs={'placeholder': " What's Happening?",
    #                             'class': 'post', "type": "text", 
    #                             "aria-label":"Post"}))
    post_type = forms.ChoiceField(POST_CHOICES, 
                                label="Type",
                                widget=forms.Select(attrs={'class':'post-event',
                                                            "id": "event-type"}))
    # date_time = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3))
    # start_time=forms.TimeField()
    start_date=forms.DateField(widget=forms.SelectDateWidget(
                empty_label=("Choose Year", "Choose Month", "Choose Day"),
                attrs={"class":"post-event"}))
    end_date=forms.DateField(widget=forms.SelectDateWidget(
                empty_label=("Choose Year", "Choose Month", "Choose Day"),
                attrs={"class":"post-event"}))
    # location=forms.CharField(max_length=42, 
    #                         label="Location",
    #                         widget = forms.TextInput(
    #                             attrs={'placeholder': " Not working now",
    #                             'class': 'post-event', "type": "text", 
    #                             "aria-label":"Post"}))
    loc = forms.CharField(disabled = True,
                          required = False,
                          label="Location",
                          widget = forms.TextInput(
                          attrs={'placeholder': "Current location or Search on the map",
                                'class': 'post-event-loc', "id":"loc-input"
                                }))
    lat = forms.DecimalField(
                             # disabled = True,
                             label="Lat",
                             widget = forms.NumberInput(
                                attrs={'class': 'post-event-loc', "type": "hidden",
                                 "name":"lat", "id":"lat-input",
                                }))
    lng = forms.DecimalField(
                             # disabled = True,
                             label="Lng",
                             widget = forms.NumberInput(
                                attrs={"type": "hidden", 
                                "name":"lng", "id":"lng-input",
                                }))
    title=forms.CharField(max_length=42, 
                          label="Title",
                          widget = forms.TextInput(
                                attrs={'placeholder': " What's up?",
                                'class': 'post-event-des', "type": "text", 
                                "aria-label":"Post"}))
    description=forms.CharField(max_length=400, 
                          label="Description",
                          widget = forms.TextInput(
                                attrs={'placeholder': " Umm...Detailed location&time",
                                'class': 'post-event-des', "type": "text", 
                                "aria-label":"Post"}))
    image = forms.ImageField(max_length=500, label="Image", required=False,
                            widget = forms.FileInput(
                            attrs={'class': 'post-event', 'multiple': True}))
    share_to = forms.ChoiceField(choices=(("PR", "Only me"),
                                         ("FR","All of my friends"),
                                         ("GL","Global")),
                                label="Share To",
                                widget=forms.Select(attrs={'class':'post-event'}),
                                )
    register_required = forms.ChoiceField(choices=((True, "Yes"),
                                         (False,"No")),
                                        label="Register Required",
                                        widget=forms.Select(attrs={'class':'post-event'}),
                                )

    # end_datetime=forms.SplitDateTimeField(input_time_formats=['%I:%M %p'],
    #             widget=forms.SplitDateTimeWidget())
    # Customizes form validation for the username field.
    # def clean(self):
    #     cleaned_data = super(PostForm, self).clean()

    #     cleaned_data["start_date"]=datetime.date(year=cleaned_data['start_date_year'],
    #                                                  month=cleaned_data['start_date_month'],
    #                                                  day=cleaned_data['start_date_day'])
    #         # print()
    #         # raise forms.ValidationError("Start Date is not valid.")

    #     return cleaned_data

class SearchForm(forms.Form):
    key_word = forms.CharField(required = True)

    

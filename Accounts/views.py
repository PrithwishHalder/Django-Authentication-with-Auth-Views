from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Sum, Count
import csv
import io
import uuid
from Accounts.models import *
from Accounts.forms import SignUpForm
from Task3.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages

User = get_user_model()


@ login_required(login_url='/login')
def home(request):
  context = {}
  # Getting total male and female Athletes in the Olympics, No. of countries participating, No of Countries received medals
  context.update(SportsGender.objects.aggregate(Sum('male')))
  context.update(SportsGender.objects.aggregate(Sum('female')))
  context.update(total=context['male__sum'] + context['female__sum'])
  context.update(countries=Country.objects.all().count())
  context.update(medalholder=Medals.objects.all().count())
  # Top 10 list of medal holder ranking
  rank_10 = {}
  rank_10['data'] = []
  rank_10['data'].append(
      list(Medals.objects.values_list('gold', flat=True))[:10])
  rank_10['data'].append(list(
      Medals.objects.values_list('silver', flat=True))[:10])
  rank_10['data'].append(list(
      Medals.objects.values_list('bronze', flat=True))[:10])
  rank_10.update(label=list(
      Medals.objects.values_list('country__country', flat=True))[:10])
  context['rank'] = rank_10
  # Number of events held for each event.
  team_types = {}
  team_types['event'] = []
  team_types['count'] = []
  data = Teams.objects.values('event').order_by(
      'event').annotate(count=Count('event'))
  for record in data:
    for key, value in record.items():
      team_types[key].append(value)
  team_types['label'], team_types['data'] = team_types['event'], team_types['count']
  del team_types['count'], team_types['event']
  context['team_types'] = team_types
  # Top 10 Rank based on No. of medals and Medals points
  context['medals'] = Medals.objects.all().order_by('rank')[:10]
  context['medalsrank'] = Medals.objects.all().order_by('total_medal_rank')[
      :10]
  # Each Gender participation in Events
  gender_participation = {}
  gender_participation['data'] = []
  gender_participation.update(label=list(SportsGender.objects.values_list(
      'sports_type', flat=True)))
  gender_participation['data'].append(
      list(SportsGender.objects.values_list('male', flat=True)))
  gender_participation['data'].append(
      list(SportsGender.objects.values_list('female', flat=True)))
  context['gender_participation'] = gender_participation
  # User Info
  context['user'] = request.user

  return render(request, "homepage.html", context)


@ login_required(login_url='/login')
def upload(request):
  context = {}
  context['user'] = None

  if request.method == "POST":
    filepath = io.TextIOWrapper(request.FILES['file'].file)
    records = csv.DictReader(filepath)
    list_of_records = list(records)

    try:
      if request.POST['type'] == "Country":
        country = Country.objects.values_list('country', flat=True)
        objs, items = [], []
        for row in list_of_records:
          if row['NOC'] not in country and row['NOC'] not in items:
            items.append(row['NOC'])
            objs.append(Country(country=row['NOC']))
        upload = Country.objects.bulk_create(objs)

      elif request.POST['type'] == "Athletes":
        objs = [Athletes(name=row['Name'], country=Country.objects.only('id').get(
            country=row['NOC']), sports=row['Discipline']) for row in list_of_records]
        upload = Athletes.objects.bulk_create(objs)

      elif request.POST['type'] == "Medals":
        objs = [Medals(rank=row['Rank'], country=Country.objects.only('id').get(country=row['NOC']), gold=row['Gold'], silver=row['Silver'],
                       bronze=row['Bronze'], total_medal=row['Total'], total_medal_rank=row['Rank by Total']) for row in list_of_records]
        upload = Medals.objects.bulk_create(objs)

      elif request.POST['type'] == "Teams":
        objs = [Teams(team_name=row['Name'], country=Country.objects.only('id').get(country=row['NOC']),
                      sports_type=row['Discipline'], event=row['Event']) for row in list_of_records]
        upload = Teams.objects.bulk_create(objs)

      elif request.POST['type'] == "Gender":
        objs = [SportsGender(sports_type=row['Discipline'], male=row['Male'],
                             female=row['Female'], total=row['Total']) for row in list_of_records]
        upload = SportsGender.objects.bulk_create(objs)

      if upload:
        context['alert'] = request.POST['type'] + " created in bulk!"

    except Exception as e:
      print("Error"+e)
      context['alert'] = "File Error!"

  return render(request, "upload.html")


def signup(request):
  context = {}
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      email = form.cleaned_data.get('email')
      auth_token = str(uuid.uuid4())
      user = User.objects.get(email=email)
      user.token = auth_token
      user.save()
      print(user)
      template = render_to_string(
          'token.html', {'user': user, 'token': auth_token})
      # send_mail("Account Verification!", template, EMAIL_HOST_USER,
      #           [email], html_message=template)
      return redirect('Homepage')
  else:
    form = SignUpForm()

  context['form'] = form
  context['form_name'] = "Sign Up"
  context['user'] = None
  return render(request, 'signup.html', context)


def verify(request, token):
  try:
    user = User.objects.filter(token=token).first()
    user.is_active = True
    user.save()
    messages.success(request, "Your account is now verified!")
  except Exception:
    messages.success(request, "Your account verification failed!")

  return redirect('Login')

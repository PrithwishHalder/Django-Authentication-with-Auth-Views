from django.db import models
from django.contrib.auth.models import AbstractUser
from Accounts.manager import UserManager


class User(AbstractUser):
  username = None
  email = models.EmailField(help_text="E-mail", unique=True)
  is_active = models.BooleanField(
      default=True, help_text="Is Account Verified")
  token = models.CharField(
      help_text="Valid User Token for Verification", max_length=100, null=True, blank=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects = UserManager()


class Country(models.Model):
  country = models.CharField(
      help_text="Country Name", unique=True, max_length=255)

  def __str__(self):
    return self.country

  class Meta:
    db_table = "country"


class Athletes(models.Model):
  name = models.CharField(help_text="Athlete Name", max_length=255)
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  sports = models.CharField(help_text="Sport Type", max_length=255)

  def __str__(self):
    return self.name

  class Meta:
    db_table = "athletes"


class Medals(models.Model):
  rank = models.IntegerField(help_text="Ranking")
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  gold = models.IntegerField(help_text="No. of Gold Medals")
  silver = models.IntegerField(help_text="No. of Silver Medals")
  bronze = models.IntegerField(help_text="No. of Bronze Medals")
  total_medal = models.IntegerField(help_text="Total number of Medals")
  total_medal_rank = models.IntegerField(
      help_text="Ranking based on No. of Medals received")

  def __str__(self):
    return self.name

  class Meta:
    db_table = "medals"


class Teams(models.Model):
  team_name = models.CharField(help_text="Team Name", max_length=255)
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  sports_type = models.CharField(help_text="Sport Type", max_length=255)
  event = models.CharField(help_text="Event type", max_length=255)

  def __str__(self):
    return self.team_name

  class Meta:
    db_table = "teams"

class SportsGender(models.Model):
  sports_type = models.CharField(help_text="Sport Type", max_length=255)
  male = models.IntegerField(help_text="No. of Males")
  female = models.IntegerField(help_text="No. of Females")
  total = models.IntegerField(help_text="Total")

  def __str__(self):
    return self.sports_type + " " + self.total

  class Meta:
    db_table = "sportsgender"

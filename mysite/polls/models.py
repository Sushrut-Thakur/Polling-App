import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=264)
    pub_date = models.DateTimeField(verbose_name="date_published")

    def __str__(self):
        return self.question
    
    def was_published_recently(self):
        """
        CHeck if question was published less than a day ago
        """
        now = timezone.now()
        return now >= self.pub_date >= (now - datetime.timedelta(days=1))

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice = models.CharField(max_length=264)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice

from django.db import models
from accounts.models import ProfileModel


class concertModel(models.Model):
    
    # class Meta:
    #     verbose_name = "کنسرت"
    #     verbose_name_plural = "کنسرت"
    
    Name = models.CharField(max_length=100)
    SingerName = models.CharField(max_length=100)
    lenght = models.IntegerField()
    Poster = models.ImageField(upload_to="concertImages/", null=True)
    
    def __str__(self):
        return self.SingerName
    
class locationModel(models.Model):
    IdNumber = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=100)
    Address = models.CharField(max_length=500, default="تهران-برج میلاد")
    Phone = models.CharField(max_length=11, null=True)
    capacity = models.IntegerField()
    
    def __str__(self):
        return self.Name
    
class timeModel(models.Model):
    concertModel = models.ForeignKey("concertModel", on_delete=models.PROTECT)  #first delete the time then the concert
    locationModel = models.ForeignKey("locationModel", on_delete=models.PROTECT)
    StartDateTime = models.DateTimeField()
    Seats = models.IntegerField()
    
    Start = 1
    End = 2
    Cancle = 3
    Sales = 4
    status_choices = ((Start,"فروش بلیط شروع شده است"),
                      (End,"فروش بلیط تمام شده است"),
                      (Cancle,"این سانس کنسل شده است"),
                      (Sales,"در حال فروش بلیط"))
    
    Status = models.IntegerField(choices=status_choices)
    
    def __str__(self):
        return "Time: {} ConcertName: {} Location: {}".format(self.StartDateTime, self.concertModel.Name, self.locationModel.Name)
    
     
class ticketModel(models.Model):
    ProfileModel = models.ForeignKey(ProfileModel, on_delete=models.PROTECT)
    timeModel = models.ForeignKey("timeModel", on_delete=models.PROTECT)
    ticketImage = models.ImageField(upload_to="ticketImages/")
    
    Name = models.CharField(max_length=100)
    Price = models.IntegerField()
    
    def __str__(self):
        return "TicketInfo: Profile:{} ConcertInfo:{} ".format(self.ProfileModel.__str__(), self.timeModel.__str__())

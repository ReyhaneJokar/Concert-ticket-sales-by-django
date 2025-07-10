from rest_framework import serializers
from .models import concertModel, locationModel, timeModel, ticketModel
from accounts.serializers import ProfileSerializer


class ConcertSerializer(serializers.ModelSerializer):
    class Meta:
        model = concertModel
        fields = ['id', 'Name', 'SingerName', 'lenght']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = locationModel
        fields = ['IdNumber', 'Name', 'Address', 'Phone', 'capacity']

class TimeSerializer(serializers.ModelSerializer):
    concert = ConcertSerializer(source='concertModel', read_only=True)
    location = LocationSerializer(source='locationModel', read_only=True)

    class Meta:
        model = timeModel
        fields = ['id', 'concert', 'location', 'StartDateTime', 'Seats', 'Status']

class TicketSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(source='ProfileModel')
    time = TimeSerializer(source='timeModel')
    
    class Meta:
        model = ticketModel
        fields = ['id', 'profile', 'time', 'Name', 'Price']

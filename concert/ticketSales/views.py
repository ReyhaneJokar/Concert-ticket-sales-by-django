from django.shortcuts import render
from django.http import HttpResponseRedirect
from ticketSales.models import concertModel, locationModel, timeModel
import ticketSales
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from ticketSales.forms import SearchForm, ConcertForm
import ticketSales.views
from .serializers import ConcertSerializer, LocationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from .permissions import IsSuperUserOrReadOnly


#----------- api views ----------

class location_list(ListCreateAPIView):
    queryset = locationModel.objects.all()
    serializer_class = LocationSerializer
    permission_classes = ((IsSuperUserOrReadOnly,))
    
class location_update(RetrieveUpdateAPIView):
    queryset = locationModel.objects.all()
    serializer_class = LocationSerializer
    permission_classes = ((IsAdminUser,))

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def concert_list(request):
    concerts = concertModel.objects.all()
    concerts_serialize = ConcertSerializer(concerts, many=True)
    return Response(concerts_serialize.data)

@api_view(["GET"])
def concert_details(request, pk):
    concert = concertModel.objects.get(id=pk)
    concert_serialize = ConcertSerializer(concert, many=False)
    return Response(concert_serialize.data)

@api_view(["POST"])
def concert_save(request):
    concert =ConcertSerializer(data=request.data)
    if concert.is_valid():
        concert.save()

    return Response(concert.data)

@api_view(["POST"])
def concert_update(request, pk):
    instance = concertModel.objects.get(id=pk)
    concert = ConcertSerializer(instance=instance,data=request.data)
    if concert.is_valid():
        concert.save()

    return Response(concert.data)

@api_view(["DELETE"])
def concert_delete(request, pk):
    instance = concertModel.objects.get(id=pk)
    instance.delete()

    return Response("concert deleted!")


#----------- ui views ----------

def concertListView(request):
    searchForm = SearchForm(request.GET)
    if searchForm.is_valid():
        SearchText = searchForm.cleaned_data["SearchText"]
        concerts = concertModel.objects.filter(Name__contains=SearchText)
    else:
        concerts = concertModel.objects.all()
    
    context = {
        "concertlist": concerts,
        "concertcount": concerts.count(),
        "searchForm": searchForm
    }
    
    return render(request, "ticketSales/concertlist.html", context)

@login_required
def locationListView(request):
    locations = locationModel.objects.all()
    context = {
        "locationlist": locations,
    }
    
    return render(request, "ticketSales/locationlist.html", context)

def concertDetailsView(request, concert_id):
    concert = concertModel.objects.get(pk=concert_id)
    
    context = {
        "concertdetails": concert
    }
    
    return render(request, "ticketSales/concertDetails.html", context)

@login_required
def timeView(request):
    # if request.user.is_authenticated and request.user.is_active:
        times = timeModel.objects.all()
        context = {
            "timelist": times,
        }
        
        return render(request, "ticketSales/timeList.html", context)
    # else:
    #     return HttpResponseRedirect(reverse(accounts.views.loginView))

def concertEditView(request, concert_id):
    concert = concertModel.objects.get(pk=concert_id)

    if request.method == "POST":
        concertForm = ConcertForm(request.POST, request.FILES, instance=concert)
        if concertForm.is_valid:
            concertForm.save()
            return HttpResponseRedirect(reverse(ticketSales.views.concertListView))
    else:
            concertForm = ConcertForm(instance=concert)
            
    context = {
            "concertForm": concertForm,
            "PosterImage": concert.Poster
        }
        
    return render(request, "ticketSales/concertEdit.html", context)

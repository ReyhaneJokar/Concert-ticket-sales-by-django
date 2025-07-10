from django.urls import path
from ticketSales import views

urlpatterns = [
    path('concert/list', views.concertListView),
    path('location/list', views.locationListView),
    path('concert/<int:concert_id>', views.concertDetailsView),
    path('time/list', views.timeView),
    path('concertEdit/<int:concert_id>', views.concertEditView),
    path('concert_list', views.concert_list),
    path('concert_details/<pk>', views.concert_details),
    path('concert_save', views.concert_save),
    path('concert_update/<pk>', views.concert_update),
    path('concert_delete/<pk>', views.concert_delete),
    path('location_list', views.location_list.as_view()),
    path('location_update/<pk>', views.location_update.as_view()),

]
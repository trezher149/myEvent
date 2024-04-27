from django.http import HttpResponse

def event_create(request):
    return HttpResponse("Add")

def event_nearest(request):
    return HttpResponse("nerest")

def event_details(request):
    return HttpResponse("details")

def add_participant(request):
    return HttpResponse("details")

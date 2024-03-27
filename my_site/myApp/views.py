from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Authors, Stories
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import datetime as dt
import json
# Create your views here.
@csrf_exempt
def login(request):
    if request.method != "POST":
        return HttpResponse("We only accept POST requests")
    authors = Authors.objects.all().values()
    logged_in = False
    for i in authors:
        if request.POST["username"] == i["username"]:
            if request.POST["password"] == i["password"]:
                logged_in = True
                author = i["author"]
                break
            else:
                return HttpResponse("Wrong password", status=401)
    if logged_in == False:
        return HttpResponse("User does not exist", status=400)
    request.session['author'] = author
    return HttpResponse("Welcome", status=200)

@csrf_exempt
def logout(request):
    if request.method != "POST":
        return HttpResponse("We only accept POST requests")
    request.session.flush()
    return HttpResponse("goodbye", status=200)

@csrf_exempt
def stories(request):
    if request.method == "POST":
        if not request.session.keys():
            return HttpResponse("Unauthenticated User", status=503)
        try:
            json_data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=503)
        required_fields = ["headline", "category", "region", "details"]
        for field in required_fields:
            if field not in json_data:
                return HttpResponse("Missing field", status=503)
        valid_categories = ["pol", "art", "tech", "trivia"]
        valid_regions  = ["uk", "eu", "w"]
        if json_data["category"] not in valid_categories:
            return HttpResponse("Invalid category", status=503)
        if json_data["region"] not in valid_regions:
            return HttpResponse("Invalid region", status=503)
        try:
            story = Stories.objects.create(headline = json_data["headline"], category = json_data["category"],
                        region = json_data["region"], author_id = Authors.objects.filter(author = request.session["author"]).values()[0]["id"],
                        date = datetime.date.today(), details = json_data["details"])
        except:
            return HttpResponse("Failed to create story", status=503)
        return HttpResponse("CREATED", status=201)
    
    elif request.method == "GET":
        stories = Stories.objects.all()
        try:
            if request.GET.get("story_cat") != "*":
                stories = stories.filter(category = request.GET.get("story_cat"))
            if request.GET.get("story_region") != "*":
                stories = stories.filter(region = request.GET.get("story_region"))
            if request.GET.get("story_date") != "*":
                date_boject = dt.strptime(request.GET.get("story_date"), '%d/%m/%Y')
                story_date = date_boject.strftime('%Y-%m-%d')
                stories = stories.filter(date__gte = story_date)
        except:
            return HttpResponse("Invalid Parameters", status=404)
        payload = []
        try:
            for story in stories:
                record = {
                    "key": story.id,
                    "headline": story.headline,
                    "story_cat": story.category,
                    "story_region": story.region,
                    "author": Authors.objects.filter(id = story.author_id).values()[0]["author"],
                    "story_date": story.date,
                    "story_details": story.details
                }
                payload.append(record)
        except:
            return HttpResponse("payload failed to be created", status=404)
        return JsonResponse({"stories": payload}, status=200)

@csrf_exempt
def delete_story(request, key):
    if request.method == "DELETE":
        if not request.session.keys():
            return HttpResponse("Unauthenticated User", status=503)
        try:
            story = Stories.objects.get(id = key)
            story.delete()
            return HttpResponse("record delete", status=200)
        except:
            return HttpResponse("Failed to delete record", status=503)


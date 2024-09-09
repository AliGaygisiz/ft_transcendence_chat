from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatUser

UsersList = []


def is_username_taken(username):
    for user in UsersList:
        if user.username == username:
            return True
    return False


def index(request):
    return render(
        request, "chat/index.html"
    )  # Render the main page with the login form


# Create your views here.
def lobby(request):
    if request.method == "POST":
        username = request.POST.get("username")
        if username:
            request.session["username"] = username  # Store username in session
            return JsonResponse({"success": True, "username": username})  # Return JSON
        return JsonResponse({"success": False, "message": "Username required"})
    return JsonResponse({"success": False, "message": "Invalid request"})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        if username and not is_username_taken(username):
            # Save the username in the session
            new_user = ChatUser()
            new_user.username = username
            new_user.id = len(UsersList) + 1
            UsersList.append(new_user)  # Add user to the list

            # print all users with ids
            for user in UsersList:
                print(user.id, user.username)
            request.session["username"] = username

            # Render partial HTML for the chat interface
            chat_html = render(
                request, "chat/chat_partial.html", {"username": username}
            ).content.decode("utf-8")

            # Return the rendered chat HTML in JSON
            return JsonResponse({"success": True, "html": chat_html})

        return JsonResponse({"success": False, "message": "Username taken"})

    return JsonResponse({"success": False, "message": "Invalid request method"})

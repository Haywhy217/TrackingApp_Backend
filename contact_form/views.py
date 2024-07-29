from django.shortcuts import render
from django.http import JsonResponse
from .forms import ContactMessageForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def contact_message(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Message sent successfully"})
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    return JsonResponse({"message": "Invalid method"}, status=405)

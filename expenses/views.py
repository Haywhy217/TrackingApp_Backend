import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Expense
from utils.utils import decode_jwt_token

@csrf_exempt
def get_expenses(request):
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split('Bearer ')[1]
            is_valid = decode_jwt_token(token)

            if is_valid == "Invalid Token" or is_valid == "Token Expired":
                return JsonResponse({"error": "Invalid token"}, status=401)

       
        title = request.GET.get('title')
        expense_type = request.GET.get('type')
        date = request.GET.get('date')

       
        expenses = Expense.objects.all()

        
        if title:
            expenses = expenses.filter(title__icontains=title)
        if expense_type:
            expenses = expenses.filter(type__icontains=expense_type)
        if date:
            expenses = expenses.filter(date=date)

       
        expense_list = list(expenses.values())
        return JsonResponse({"data": expense_list}, status=200)

    else:
        return JsonResponse({"error": "GET method required"}, status=400)

@csrf_exempt
def add_expense(request):
    if request.method == "POST":
        json_data = request.body.decode("utf-8")
        data_dict = json.loads(json_data)
        
        
        title = data_dict.get("title")
        description = data_dict.get("description", "")
        amount = data_dict.get("amount")
        date = data_dict.get("date")
        expense_type = data_dict.get("type")
        
        
        existing_expense = Expense.objects.filter(title=title, date=date).first()
        if existing_expense:
            return JsonResponse({"message": "Expense with these details already exists"}, status=400)
        
       
        Expense.objects.create(
            title=title,
            description=description,
            amount=amount,
            date=date,
            type=expense_type
        )
        return JsonResponse({"message": "Expense added successfully"}, status=201)

    else:
        return JsonResponse({"message": "Invalid method"}, status=405)

@csrf_exempt
def update_expense(request):
    if request.method == 'PUT':
        expense_data = json.loads(request.body)
        expense = Expense.objects.get(id=expense_data['id'])
        expense.title = expense_data['title']
        expense.description = expense_data['description']
        expense.amount = expense_data['amount']
        expense.date = expense_data['date']
        expense.type = expense_data['type']
        expense.save()
        return JsonResponse({'message': 'Expense updated successfully'})
    else:
        return JsonResponse({'message': 'Invalid method'})

@csrf_exempt
def delete_expense(request):
    if request.method == 'DELETE':
        expense_data = json.loads(request.body)
        expense_id = expense_data['id']
        try:
            expense = Expense.objects.get(id=expense_id)
            expense.delete()
            return JsonResponse({'message': 'Expense deleted successfully'})
        except Expense.DoesNotExist:
            return JsonResponse({'message': 'Expense not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid method'})
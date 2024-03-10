# from django import forms
# from ..models import Reporter
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# class ReportForm(forms.ModelForm):
#     class Meta:
#         model = Reporter
#         fields = ['reporter','spammer','reported_to','message']


# # @csrf_exempt        
# def save_report(request):
#     if request.method == 'POST':
#         form = ReportForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'message': 'Report saved successfully'}, status=201)
#         else:
#             return JsonResponse({'error': 'Invalid data'}, status=400)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405) 
    
           


    
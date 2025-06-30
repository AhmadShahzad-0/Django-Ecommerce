from django.shortcuts import render

# Create your views here.
def payment_success(request):
    # View to render the payment success page.
    return render(request, 'payment/payment_success.html', {})

def test(request):
    # Test view to check if the payment app is working.
    return render(request, 'payment/test.html', {})
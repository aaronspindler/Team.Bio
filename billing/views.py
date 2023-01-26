import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User
from billing.models import StripeCustomer


@login_required
def home(request):
    return render(request, 'billing/home.html')


@login_required
def success(request):
    return render(request, 'billing/success.html')


@login_required
def cancel(request):
    return render(request, 'billing/cancel.html')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=settings.BASE_URL + 'billing/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.BASE_URL + 'billing/cancel',
                payment_method_types=['card'],
                mode='setup',
                customer_email=request.user.email if request.user.is_authenticated else None,
                customer_creation='always'
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        setup_intent_id = session.get('setup_intent')

        setup_intent = stripe.SetupIntent.retrieve(setup_intent_id)
        payment_method = setup_intent.get('payment_method')

        # Get the user and create a new StripeCustomer
        user = User.objects.get(id=client_reference_id)
        StripeCustomer.objects.create(
            user=user,
            stripeCustomerId=stripe_customer_id,
            setupIntentId=setup_intent_id,
            paymentMethod=payment_method
        )

    return HttpResponse(status=200)

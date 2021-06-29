from django.shortcuts import render
from .form import createTicket
import requests
from django.conf import settings
from django.contrib import messages

ms_identity_web = settings.MS_IDENTITY_WEB

def create(request):
    context = {}
    context['form'] = createTicket()
    if request.method =="POST":
        print(request.POST)
        ms_identity_web.acquire_token_silently()
        api_url = "https://localhost:44300/_api/apt_contactstables"
        body = {}
        body['apt_name'] = request.POST.get('Name')
        body['apt_phonenumber'] = request.POST.get('Phone') 
        #body['apt_issue'] = request.POST.get('Issue')[0]
        #body = {"apt_name":"test45","apt_phonenumber":"45345557"}
        headers = {'Authorization': "Bearer "+ms_identity_web.id_data._access_token, 'x-portal-idp': "Azure AD",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            'Content-Type': 'application/json'}
        print(body)
        print(headers)
        response = requests.post(api_url, json= body, headers = headers, verify=False)
        print(response)
        if (response.status_code == 204):
            context['status'] = "Your ticket was created successfully!"
        elif (response.status_code == 401):
            context['status'] = "Unauthorized User!"
        elif (response.status_code == 403):
            context['status'] = "You do not have permissions to perform this operation!"
        else:
            context['status'] = "Something went wrong! Ticket creation failed"
    return render(request, 'form.html', context)

def populate(request):
    context = {}
    url = "https://localhost:44300/_api/apt_contactstables"
    ms_identity_web.acquire_token_silently()
    try: 
        headers = {'Authorization': "Bearer "+ ms_identity_web.id_data._access_token, 'x-portal-idp': "Azure AD",
                'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        r = requests.get(url, headers= headers,verify=False)
        print(r)
        response = r.json()
        tickets = []
        for i in range(len(response['value'])):
            tickets.append(response['value'][i])
        context['tickets'] = tickets
    except Exception as e:
        pass
    return render(request, 'table.html', context)

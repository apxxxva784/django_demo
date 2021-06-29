from django import forms

class createTicket(forms.Form):

    Name = forms.CharField(max_length=50)
    Phone = forms.CharField(max_length=10,required=True)




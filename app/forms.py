from django import forms
from.models import *
class CreateEvent(forms.ModelForm):
    class Meta:
        model=Event
        fields=['name','image','description']
        
class create_main(forms.ModelForm):    
    class Meta:
        model=MainImage
        fields=['name','image']  
    def __str__(self):
        return self.name
class create_sub(forms.ModelForm) :
    class Meta:
        model=SubImage
        fields=['image','images']       
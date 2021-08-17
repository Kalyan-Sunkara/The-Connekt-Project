from django.shortcuts import render, redirect, get_object_or_404
from firstApp.models import UserProfileInfo
def firstContext(request):
    try:
        if request.user.is_authenticated:
            profile = get_object_or_404(UserProfileInfo,user=request.user)
            return {
                'profile': profile
            }
        return {'empty': ''}
    except:
        return {'profile':'hi'}

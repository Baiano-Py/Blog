def profile_context(request):
    return {
        'profile': request.user.profile if request.user.is_authenticated else None
    }
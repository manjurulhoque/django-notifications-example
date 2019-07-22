def notifications(request):
    context = {}
    if request.user.is_authenticated:
        context['notifications'] = request.user.notifications.unread()
    return context

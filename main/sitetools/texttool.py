def description_to_HTML(text: str):
    for i in text:
        print(i, end="")
    text = text.replace("\n", "<br>")
    return text


def get_context(request, name, display_bradcam=True):
    context = {'pagename': name, 'bradcam_display': display_bradcam, 'is_login': request.user.is_authenticated}
    if request.user.is_authenticated:
        context['username'] = request.user.username
    return context

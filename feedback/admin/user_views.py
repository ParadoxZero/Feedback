from django.shortcuts import render


def index(request):
    try:
        error = request.GET['error']
        context = {'error_message': 'Some error has occured'} # TODO error message
    except KeyError:
        context = {}
    return render(request, 'feedback/admin/user_index.html', context)


from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render

from feedback.models import Forms, TextBox, MultiLine, CheckBox, MCQ, Option
from feedback.views.decorators import feedbackuser_login_required


@feedbackuser_login_required
def formfill(request, form_id):
    try:
        form = Forms.objects.get(pk=form_id)
    except KeyError:
        return HttpResponseRedirect(reverse("feedback_feedbackuser_formlist"))
    text_box_list = TextBox.objects.filter(form=form)
    multiline_lsit = MultiLine.objects.filter(form=form)
    checkbox_list = CheckBox.objects.filter(form=form)
    mcq_list = MCQ.objects.filter(form=form)
    form_item_list = []
    for item in text_box_list + multiline_lsit + checkbox_list + mcq_list:
        if type(item) is TextBox:
            code = "tb"
        elif type(item) is MultiLine:
            code = "mb"
        elif type(item) is CheckBox:
            code = "cb"
        else:  # type(item) is MCQ
            code = "mcq"
        if code != 'mcq':
            item_format = [code, item]
        else:
            item_format = [code, item, Option.objects.filter(mcq=item)[:]]
        form_item_list.append(item_format)
    quicksort(form_item_list, 0, len(form_item_list) - 1)
    context = {
        'item_list': form_item_list
    }
    return render(request, 'feedback/feedbackuser_formfil', context)


'''
=======================================================================================
            Quick sort to sort according to position (direct copy from net)
=======================================================================================
'''


def partition(list, start, end):
    pivot = list[end]  # Partition around the last value
    bottom = start - 1  # Start outside the area to be partitioned
    top = end  # Ditto

    done = 0
    while not done:  # Until all elements are partitioned...

        while not done:  # Until we find an out of place element...
            bottom += 1  # ... move the bottom up.

            if bottom == top:  # If we hit the top...
                done = 1  # ... we are done.
                break

            if list[bottom][1].position > pivot[1].position:  # Is the bottom out of place?
                list[top] = list[bottom]  # Then put it at the top...
                break  # ... and start searching from the top.

        while not done:  # Until we find an out of place element...
            top -= 1  # ... move the top down.

            if top == bottom:  # If we hit the bottom...
                done = 1  # ... we are done.
                break

            if list[top][1].postion < pivot[1].position:  # Is the top out of place?
                list[bottom] = list[top]  # Then put it at the bottom...
                break  # ...and start searching from the bottom.

    list[top] = pivot  # Put the pivot in its place.
    return top  # Return the split point


def quicksort(list, start, end):
    if start < end:  # If there are two or more elements...
        split = partition(list, start, end)  # ... partition the sublist...
        quicksort(list, start, split - 1)  # ... and sort both halves.
        quicksort(list, split + 1, end)
    else:
        return

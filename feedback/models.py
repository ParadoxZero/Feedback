from random import Random
import string
from django.db import models

# Create your models here.
from django.utils import timezone


class FeedbackUser(models.Model):
    user_name = models.CharField(max_length=200)
    date_created = models.DateField()

    @staticmethod
    def create_users(number):
        for _ in range(number):
            u = FeedbackUser()
            while True:
                try:
                    # noinspection PyArgumentList
                    u.user_name = ''.join([Random.choice(string.ascii_lowercase) for _ in range(6)])
                    u.date_created = timezone.now()
                    u.save()
                    break
                except Exception:  # TODO
                    pass

    def __str__(self):
        return self.user_name


class Survey(models.Model):
    name = models.CharField(max_length=500)
    date_created = models.DateField(primary_key=True)
    finished = models.BooleanField(default=False)


class Assessee(models.Model):
    name = models.CharField(max_length=200)
    date_created = models.DateField()

    def __str__(self):
        return self.name


class Forms(models.Model):
    user = models.ForeignKey(FeedbackUser)
    assessee = models.ForeignKey(Assessee)
    survey = models.ForeignKey(Survey)
    form_name = models.CharField(max_length=500)
    date_created = models.DateField()
    finished = models.BooleanField(default=False)

    def getInputs(self):
        text_box_list = TextBox.objects.filter(form=self)
        multiline_lsit = MultiLine.objects.filter(form=self)
        checkbox_list = CheckBox.objects.filter(form=self)
        mcq_list = MCQ.objects.filter(form=self)
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
        Forms.__quicksort(form_item_list)
        return form_item_list

    def __str__(self):
        return self.form_name

    @staticmethod
    def __partition(item_list, start, end):
        pivot = item_list[end]  # Partition around the last value
        bottom = start - 1  # Start outside the area to be partitioned
        top = end  # Ditto

        done = 0
        while not done:  # Until all elements are partitioned...

            while not done:  # Until we find an out of place element...
                bottom += 1  # ... move the bottom up.

                if bottom == top:  # If we hit the top...
                    done = 1  # ... we are done.
                    break

                if item_list[bottom][1].position > pivot[1].position:  # Is the bottom out of place?
                    item_list[top] = item_list[bottom]  # Then put it at the top...
                    break  # ... and start searching from the top.

            while not done:  # Until we find an out of place element...
                top -= 1  # ... move the top down.

                if top == bottom:  # If we hit the bottom...
                    done = 1  # ... we are done.
                    break

                if item_list[top][1].postion < pivot[1].position:  # Is the top out of place?
                    item_list[bottom] = item_list[top]  # Then put it at the bottom...
                    break  # ...and start searching from the bottom.

        item_list[top] = pivot  # Put the pivot in its place.
        return top  # Return the split point

    @staticmethod
    def __quicksort(item_list, start, end):
        if start < end:  # If there are two or more elements...
            split = Forms.__partition(item_list, start, end)  # ... partition the sublist...
            Forms.__quicksort(item_list, start, split - 1)  # ... and sort both halves.
            Forms.__quicksort(item_list, split + 1, end)
        else:
            return


class TextBox(models.Model):
    form = models.ForeignKey(Forms)
    position = models.IntegerField()
    text = models.CharField(max_length=500)
    data = models.CharField(max_length=500)

    def __str__(self):
        return self.text


class MultiLine(models.Model):
    form = models.ForeignKey(Forms)
    position = models.IntegerField()
    text = models.CharField(max_length=500)
    data = models.CharField(max_length=10000)

    def __str__(self):
        return self.text


class CheckBox(models.Model):
    form = models.ForeignKey(Forms)
    position = models.IntegerField()
    text = models.CharField(max_length=500)
    data = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class MCQ(models.Model):
    form = models.ForeignKey(Forms)
    position = models.IntegerField()
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text


class Option(models.Model):
    mcq = models.ForeignKey(MCQ)
    text = models.CharField(max_length=500)
    data = models.BooleanField(default=False)

    def __str__(self):
        return self.text


# =================================================================================
"""
    The following model is to store a form layout to make forms reusable
"""
# =================================================================================

TEXTBOX = 'tb'
# noinspection SpellCheckingInspection
MULTILINE_TEXTBOX = 'mb'
CHECKBOX = 'cb'
MULTIPLE_CHOICE = 'mcq'
OPTION = "op"


class FormLayout(models.Model):
    """
        The Form layout specifies the type of fields present in the form,
        the structure of layout is :
            ...$<Field Code>@<Field Text>$<Field Code>@<Field Text>...
        in case of MCQ a special format is used for specifying choice
            ...$mcq@<Text>@<Choice 1 text>^<Choice 2 Text>$<Field...
    """
    name = models.CharField(max_length=500)
    layout = models.CharField(max_length=5000)

    def generate_objects(self, form):
        """
            This is a generator method that will return
            already saved data fields for a new form according
            to the form layout
        :param form: The form these fields will belong to
        :return: Fields [Checkbox,Textbox,MultiLine,MCQ]
        """
        layout_string = self.layout[1:]  # To remove the '$' present at the beginning
        element_list = layout_string.split('$')
        for i, item in enumerate(element_list):
            temp = item.split('@')
            if temp[0] == TEXTBOX:
                element = TextBox(
                    text=temp[1],
                    position=i,
                    form=form
                )
                element.save()
            elif temp[0] == MULTILINE_TEXTBOX:
                element = MultiLine(
                    text=temp[1],
                    position=i,
                    form=form
                )
                element.save()
            elif temp[0] == CHECKBOX:
                element = CheckBox(
                    text=temp[1],
                    position=i,
                    form=form
                )
                element.save()
            elif temp[0] == MULTIPLE_CHOICE:
                element = MCQ(
                    text=temp[1],
                    position=i,
                    form=form
                )
                element.save()
                extra = temp[2].split('^')
                for j in extra:
                    choice = Option(
                        mcq=element,
                        text=j
                    )
                    choice.save()
            else:
                raise Exception
            yield element

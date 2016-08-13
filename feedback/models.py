from django.db import models

# Create your models here.

class FeedbackUser(models.Model):
    user_name = models.CharField(max_length=200)
    date_created = models.DateField()

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

    def __str__(self):
        return self.form_name


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

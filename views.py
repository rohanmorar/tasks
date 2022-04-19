from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse


class NewTaskForm(forms.Form):
                                #form label
    task = forms.CharField(label="New task")

    # priority = forms.IntegerField(label="Priority", min_value = 1, max_value =5)

def index(request):
    # checks if there's no list of "tasks" in the session, if not in then creates one
    if "tasks" not in request.session:

        #if user doesn't already have a list of tasks, give them an empty list of tasks
        request.session["tasks"] = []

    return render(request, "tasks/index.html", {
        # common convention, same name, on the right of is a python actual value from list above (name is on the left)
        # left is the key or variable name
        "tasks": request.session["tasks"]
    })

#way for django to build form
def add(request):
    # 1) checks if user submits some form data
    if request.method == "POST":
        # 2) figures out all the data they submitted and save it inside...
        #  ... a form variable by taking all of the request.POST data and filling it into the NewTaskForm
        form = NewTaskForm(request.POST)

        # 3) checks to see if the form itself is valid, did they provide a task / all neccesary data in the right format
        if form.is_valid():
            # 4) if so, we get the task and add it to the list of tasks
            task = form.cleaned_data["task"]
            # gives access to all data user submitted - "name" must match from class above (task variable)
            request.session["tasks"] += [task]
                                        # says figure out what the url of the index url for the tasks app is and
                                        # use that url as the one we ultimatley redirect to when we return this
            return HttpResponseRedirect(reverse("tasks:index"))


        # otherwise if form not valid, we go ahead and render the same add.html back to them but pass in the form they submitted
        # ... so they can see the errors they made and make modifications
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })
    # If request method not posted at all (user just tries to get the page rather than submit data to it)
    # ... then we just render to them an empty form
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })

from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

import markdown2
import re
from . import util
from random import choice

class EntryForm(forms.Form):
    title = forms.CharField(label = "Title")
    content = forms.CharField(label = "Content", widget = forms.Textarea)

def search(request):

    entries = util.list_entries()

    query = request.GET['q']

    search_entries = []
    for entry in entries:
        if query.lower() == entry.lower():
            return HttpResponseRedirect(f"/wiki/{entry}")
        elif re.search(query.lower(), entry.lower()) != None:
            search_entries.append(entry)
        else:
            continue

    return render(request, "encyclopedia/search.html", {
            "entries": search_entries
    })

def newPage(request):

    # Check if method is POST
    if request.method == "POST":

        exists = False
        error = ''
        # Take in the data the user submitted and save it as form
        form = EntryForm(request.POST)

        if form.is_valid():

            # Isolate the task from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = "# " + title + "\n" + form.cleaned_data["content"]

            entries = [entry.lower() for entry in util.list_entries()]

            if title.lower() not in entries:
                # Add the new entry
                util.save_entry(title, content)

            else:
                exists = True
                error = f"{title} already exists"
                return render(request, "encyclopedia/new.html", {
                    "form": EntryForm(), "error": error, "exists":exists
                })

            # Redirect user to entry page
            return HttpResponseRedirect(f"/wiki/{title}")


    # If the form is invalid, re-render the page with existing information.
    return render(request, "encyclopedia/new.html", {
        "form": EntryForm()
    })

def randomPage(request):
     page = choice(util.list_entries())
     return HttpResponseRedirect(f"{page}")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):

    fullEntry = util.get_entry(entry_name)


    if fullEntry == None:
        #Go to Page not found
        return render(request, "encyclopedia/notFound.html")
    else:
        fullEntry = markdown2.markdown(fullEntry)

        title = re.search(entry_name, fullEntry).group()

        return render(request, "encyclopedia/entry.html", {
            "title": title, "entry": fullEntry
        })

def editPage(request, entry):

    #initialise dictionary with form data
    content = util.get_entry(entry)
    content = re.sub(f"# {entry}", '', content)
    context = {"title": entry, "content": content}

    #instantiate form with dictionary as initial argument

    form = EntryForm(request.POST or None, initial = context)

    if form.is_valid():

        # Isolate the task from the 'cleaned' version of form data
        title = form.cleaned_data["title"]
        content = "# " + title + "\n" + form.cleaned_data["content"]
        util.save_entry(entry, content)

        # Redirect user to entry page
        return HttpResponseRedirect(f"/wiki/{title}")

    return render(request, "encyclopedia/edit.html", {
        "form": form, "path":entry, "content": content
    })

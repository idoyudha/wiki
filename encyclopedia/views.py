from django.shortcuts import render
from django import forms

from . import util
import markdown
import re

class ContentForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50, widget = forms.TextInput)
    content = forms.CharField(label="Content", max_length=1000, widget = forms.Textarea)
    
    title.widget.attrs.update({'class': 'form-control mb-2'})
    content.widget.attrs.update({'class': 'form-control', 'rows': '15'})

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "title": "Encyclopedia",
        "entries": entries
    })

def entry(request, title):
    data = util.get_entry(title)
    filter = markdown.markdown(data)
    context_entry = {
        "filter": filter,
        "title": title
    }
    context_none = {
        "title": title
    }
    if data == "None":
        return render(request, "encyclopedia/notexist.html", context_none)
    else:
        return render(request, "encyclopedia/entry.html", context_entry)

def search(request):
    string = request.GET.get("q")
    entries = util.list_entries()
    r = re.compile(".*{}".format(string))
    search_list = list(filter(r.match, entries))
    context = {
        "title": "Search Result",
        "val": string,
        "entries": search_list
    }
    if string in entries:
        return entry(request, string)
    else:
        return render(request, "encyclopedia/search.html", context)

def new(request):
    if request.method == "POST":
        entries = util.list_entries()
        form = ContentForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in entries:
                return render(request, "encyclopedia/same.html")
            else:
                util.save_entry(title, content)
                return entry(request, title)
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    context = {
        "form": ContentForm(),
        "title": "Create new page"
    }
    return render(request, "encyclopedia/new.html", context)

def edit(request, title):
    data = util.get_entry(title)
    content = ContentForm(initial={'content': data})
    if request.method == "POST":
        form = ContentForm(request.POST)
        content_clean = form.cleaned_data["content"]
        util.save_entry(title, content_clean)
        return render(request, "encyclopedia/entry.html")
    else:
        context = {
            "form": content,
            "title_edit": "Edit page",
            "title": title
        }
        return render(request, "encyclopedia/edit.html", context)

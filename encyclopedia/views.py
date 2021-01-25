from django.shortcuts import render

from . import util
import markdown

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):
    data = util.get_entry(title)
    filter = markdown.markdown(data)
    context_entry = {
        "filter": filter
    }
    context_none = {
        "title": title
    }
    if data == "None":
        return render(request, "encyclopedia/notexist.html", context_none)
    else:
        return render(request, "encyclopedia/entry.html", context_entry)

def search(request):
    pass
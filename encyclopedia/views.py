from re import search
from django.shortcuts import render, redirect 

from . import util
import markdown
import re


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
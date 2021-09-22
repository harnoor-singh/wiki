import markdown2
from random import randrange
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from . import util




def index(request):
    """
    returns a list of all entries in the 'entries' directory
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def displayEntry(request, title):
    """
    returns a specific entry with its content (if it exists), else a error page.
    """
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html") 
    else:
        return render(request, "encyclopedia/displayEntry.html", {
            "title": title,
            "content": markdown2.markdown(util.get_entry(title))
            })


def createNewPage(request):
    return render(request, "encyclopedia/createNewPage.html")


def saveCreatedEntry(request):
    if request.POST['title'].lower() in map(str.lower, util.list_entries()):
        return render(request, "encyclopedia/saveError.html")
    else:
        util.save_entry(request.POST['title'], request.POST['content'])
        return HttpResponseRedirect(reverse(
            'encyclopedia:displayEntry', args=(request.POST['title'],)))


def editEntry(request, title):
    return render(request, "encyclopedia/editEntry.html", {
        "title": title,
        "content": util.get_entry(title)
        })


def saveEditedEntry(request):
    util.save_entry(request.POST['title'], request.POST['content'])
    return HttpResponseRedirect(reverse(
        'encyclopedia:displayEntry', args=(request.POST['title'],)))


def randomPage(request):
    list_of_entries = util.list_entries().copy()
    randomEntry = list_of_entries[randrange(0, len(list_of_entries))]
    return HttpResponseRedirect(reverse('encyclopedia:displayEntry', args=(randomEntry,)))


def searchResults(request):
    """
        1) Redirects directly if query is same as some entry
        2) Returns required entries if the query is substring in any entry
        3) Returns a 'no results page' if query doesn't match any entry
    """
    list_of_entries = util.list_entries().copy()
    query = request.GET['q']

    """
    map(str.lower, list_of_entries) is an example of functional programming.
    found it while searching for the solution of making each entry in the list lowercase.
    """
    # redirecting to direct queries.
    if query.lower() in map(str.lower, list_of_entries):
        return HttpResponseRedirect(reverse('encyclopedia:displayEntry', args=(query,)))
        # comma after query in args is very necessary.

    # checking for substrings
    temporary_entries_list = []
    for entry in list_of_entries:
        if query.lower() in entry.lower():
            temporary_entries_list.append(entry)
    return render(request, "encyclopedia/searchResults.html", {
        "query": query,
        "results": temporary_entries_list,
        "num_of_results": len(temporary_entries_list)
        })

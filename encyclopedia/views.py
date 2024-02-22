from django.shortcuts import render, redirect, reverse
from django import forms
from . import util
import random

class newEntryForm(forms.Form):
    entryName = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder":"Entry Name",}))
    entryText = forms.CharField(label="", widget=forms.Textarea(attrs={"placeholder":"Text", 'rows':3, 'cols':5})) 

# class prefilledEntryForm(forms.Form):
#     def __init__(self, name, text):
#         super().__init__(name, text)
#         self.entryName = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder":"Entry Name", "text":name}))
#         self.entryText = forms.CharField(label="", widget=forms.Textarea(attrs={"placeholder":"Text", 'rows':3, 'cols':5, "text":text})) 


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    content = util.get_entry(entry)
    return render(request, "encyclopedia/entry.html", {
        "entryName": entry,
        "entryText": util.convertMarkdown(content)
    })

def search(request):
    if request.method == "POST":
        term = request.POST['search']
        termLower = term.lower()
        pageList = util.list_entries()
        foundPages = []
        for page in pageList:
            pageName = page.lower()
            if pageName == termLower:
                return redirect(reverse('encyclopedia:entry', kwargs={'entry':str(term)}))
            elif termLower in pageName:
                foundPages.append(page)
        return render(request, "encyclopedia/search.html", {
            "title": term,
            "entries": foundPages
    })

def editEntry(request):
    if request.method == "POST":
        form = newEntryForm(request.POST)
        if form.is_valid():
            entryName = form.cleaned_data['entryName']
            entryText = form.cleaned_data['entryText']
            util.save_entry(entryName, entryText)
            return redirect(reverse('encyclopedia:entry', kwargs={'entryName':str(entryName), 'entryText':str(entryText)}))
        else:
            return render(request, "encyclopedia/editEntry.html", {
                "form": form
            })
    elif request.method == "GET":
        entryName = request.GET.get('entryName')
        entryText = util.get_entry(entryName)
        return render(request, "encyclopedia/editEntry.html", {
            "entryName": entryName,
            "entryText": entryText
        })
    
def createEntry(request):
    if request.method == "POST":
        form = newEntryForm(request.POST)
        if form.is_valid():
            entryName = form.cleaned_data['entryName']
            entryText = form.cleaned_data['entryText']
            titleExists = util.get_entry('entryName')
            if titleExists is not None:
                return render(request, "encyclopedia/editEntry.html", {
                "form": form,
                "error": "Error: Page already exists"
                })
            else:
                util.save_entry(entryName, entryText)
                return redirect(reverse('encyclopedia:entry', kwargs={'entry':str(entryName)}))
        else:
            return render(request, "encyclopedia/editEntry.html", {
                "form": form
            })
    return render(request, "encyclopedia/editEntry.html", {
        "form": newEntryForm()
    })

def randomPage(request):
    pageList = util.list_entries()
    listLength = len(pageList)
    randPage = pageList[random.randrange(0, listLength)]
    return redirect(reverse('encyclopedia:entry', kwargs={'entry':str(randPage)}))

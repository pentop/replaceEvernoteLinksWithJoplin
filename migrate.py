import urllib.request
import json 
from sys import argv

#ToDo - create a backup before we start! https://discourse.joplinapp.org/t/best-method-to-backup-notes/1135

replacements={
    'evernote:///view/237202231/s7/82254d2d-f19d-49b6-9ab6-7c57626e6897/82254d2d-f19d-49b6-9ab6-7c57626e6897/':':/79bfb652ff4c41d89b42b6d92cc3469d', #Home Page
    'evernote:///view/926571/s7/82254d2d-f19d-49b6-9ab6-7c57626e6897/82254d2d-f19d-49b6-9ab6-7c57626e6897/':':/79bfb652ff4c41d89b42b6d92cc3469d', #Home Page
    'evernote:///view/926571/s7/b05e6cfc-dff4-46c1-bdc3-4339c3e44a25/b05e6cfc-dff4-46c1-bdc3-4339c3e44a25/':':/8bcb8b3ba6554ff6a1e7fa53a3494e7d', #Family Quotes
    'evernote:///view/926571/s7/6314702c-39a4-4860-b186-2b6123aa4c60/6314702c-39a4-4860-b186-2b6123aa4c60/':':/d52d8282440849b79e8be83187ca2021', #Thursday ToDo checklist
    'evernote:///view/926571/s7/8f862370-0b94-4da2-b4da-44f24dcbf1dd/8f862370-0b94-4da2-b4da-44f24dcbf1dd/':':/a4bc45e4043d4bb8afd6a540930bc06a', #ToDo
    'evernote:///view/926571/s7/ac937071-0dee-4ac2-b07d-f4621642a73c/ac937071-0dee-4ac2-b07d-f4621642a73c/':':/360c27581b764d9aa835783d612dd98a', #Accounts
    'evernote:///view/926571/s7/83df728f-6641-489c-aacf-c2db30943cb2/83df728f-6641-489c-aacf-c2db30943cb2/':':/85c4d82e80be4af8ba308d668ff5be44' #Wifi keys
}

def replaceTextInNote(note, textToReplace, replacement):
    noteBody = note["body"]
    noteId = note["id"]
    noteTitle = note["title"]
    opener = urllib.request.build_opener(urllib.request.HTTPHandler)
    print(f'Replacing:<{textToReplace}> with:<{replacement}> in the note with title:<{noteTitle}>')
    newNoteBody = noteBody.replace(textToReplace, replacement)
    payload = {'body': newNoteBody}
    putUrl = f'{baseUrl}notes/{noteId}?{tokenUrlPart}'
    payloadAsBytes = bytes(json.dumps(payload), encoding="utf-8")
    #ToDo - switch to using requests https://2.python-requests.org/
    request = urllib.request.Request(putUrl, data=payloadAsBytes)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'PUT'
    if commitChanges:
        opener.open(request)

def searchAndReplace(textToReplace, replacement):
    #ToDo - can I restrict this search to a single notebook for safety? Doesn't look like it: https://joplinapp.org/#searching
    searchUrl = f'{baseUrl}search?query={textToReplace}{tokenUrlPart}&fields=id,body,title'
    searchResultsJson = urllib.request.urlopen(searchUrl).read()
    searchResults = json.loads(searchResultsJson)
    print(f'Searching for :<{textToReplace}> found:<{len(searchResults)}> notes')
    for note in searchResults:
        replaceTextInNote(note, textToReplace, replacement)

def ping():
    url = f'{baseUrl}ping?{tokenUrlPart}'
    contents = urllib.request.urlopen(url).read()
    print(f'Joplin server at:<{url}> returned:<{contents}>')

def main():
    #ping()
    for key, value in replacements.items():
        old = key
        new = value
        searchAndReplace(old, new)
    print('finished!')

print (len(argv))
print (argv)


if len(argv) <= 1:
     print('Useage: migrate.py <joplinToken>')
     exit
token = argv[1]
baseUrl = 'http://localhost:41184/'
tokenUrlPart = f'&token={token}'
notesUrl = f'{baseUrl}notes?token{token}'
commitChanges = False #Set to True to commit changes to notes

ping()
# main()

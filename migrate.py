import urllib.request
import json 
from sys import argv

#ToDo
# create a backup before we start! https://discourse.joplinapp.org/t/best-method-to-backup-notes/1135
# pull out the token somewhere safe
# Log out some kind of indication of how long the script has to run

replacements={
    'evernote:///view/237202231/s7/82254d2d-f19d-49b6-9ab6-7c57626e6897/82254d2d-f19d-49b6-9ab6-7c57626e6897/':':/79bfb652ff4c41d89b42b6d92cc3469d', #Home Page
    'evernote:///view/926571/s7/82254d2d-f19d-49b6-9ab6-7c57626e6897/82254d2d-f19d-49b6-9ab6-7c57626e6897/':':/79bfb652ff4c41d89b42b6d92cc3469d', #Home Page
    'evernote:///view/926571/s7/b05e6cfc-dff4-46c1-bdc3-4339c3e44a25/b05e6cfc-dff4-46c1-bdc3-4339c3e44a25/':':/8bcb8b3ba6554ff6a1e7fa53a3494e7d', #Family Quotes
    'evernote:///view/926571/s7/6314702c-39a4-4860-b186-2b6123aa4c60/6314702c-39a4-4860-b186-2b6123aa4c60/':':/d52d8282440849b79e8be83187ca2021', #Thursday ToDo checklist
    'evernote:///view/926571/s7/8f862370-0b94-4da2-b4da-44f24dcbf1dd/8f862370-0b94-4da2-b4da-44f24dcbf1dd/':':/a4bc45e4043d4bb8afd6a540930bc06a', #ToDo
    'evernote:///view/926571/s7/ac937071-0dee-4ac2-b07d-f4621642a73c/ac937071-0dee-4ac2-b07d-f4621642a73c/':':/360c27581b764d9aa835783d612dd98a', #Accounts
    'evernote:///view/926571/s7/83df728f-6641-489c-aacf-c2db30943cb2/83df728f-6641-489c-aacf-c2db30943cb2/':':/85c4d82e80be4af8ba308d668ff5be44' #Wifi keys
}

class JoplinConnection():
    def __init__(self, joplin_token):
        self.joplin_token = joplin_token
        self.baseUrl = 'http://localhost:41184/'
        self.tokenUrlPart = f'&token={self.joplin_token}'
        self.notesUrl = f'{self.baseUrl}notes?token{self.joplin_token}'
        self.commitChanges = True #Set to True to commit changes to notes

    def ping(self):
        url = f'{self.baseUrl}ping?{self.tokenUrlPart}'
        contents = urllib.request.urlopen(url).read()
        print(f'Joplin server at:<{url}> returned:<{contents}>')

    def __replaceTextInNote(self, note, textToReplace, replacement):
        noteBody = note["body"]
        noteId = note["id"]
        noteTitle = note["title"]
        opener = urllib.request.build_opener(urllib.request.HTTPHandler)
        print(f'Replacing:<{textToReplace}> with:<{replacement}> in the note with title:<{noteTitle}>')
        newNoteBody = noteBody.replace(textToReplace, replacement)
        payload = {'body': newNoteBody}
        putUrl = f'{self.baseUrl}notes/{noteId}?{self.tokenUrlPart}'
        payloadAsBytes = bytes(json.dumps(payload), encoding="utf-8")
        #ToDo - switch to using requests https://2.python-requests.org/
        request = urllib.request.Request(putUrl, data=payloadAsBytes)
        request.add_header('Content-Type', 'application/json')
        request.get_method = lambda: 'PUT'
        if self.commitChanges:
            opener.open(request)

    def searchAndReplace(self, textToReplace, replacement):
        #ToDo - can I restrict this search to a single notebook for safety? Doesn't look like it: https://joplinapp.org/#searching
        searchUrl = f'{self.baseUrl}search?query={textToReplace}{self.tokenUrlPart}&fields=id,body,title'
        searchResultsJson = urllib.request.urlopen(searchUrl).read()
        searchResults = json.loads(searchResultsJson)
        print(f'Searching for :<{textToReplace}> found:<{len(searchResults)}> notes')
        for note in searchResults:
            self.__replaceTextInNote(note, textToReplace, replacement)        

if len(argv) <= 1:
    exit('Useage: migrate.py <joplinToken>')
joplin_token = argv[1]
joplin_connection = JoplinConnection(joplin_token)

joplin_connection.ping()
for key, value in replacements.items():
    old = key
    new = value
    joplin_connection.searchAndReplace(old, new)
print('finished!')


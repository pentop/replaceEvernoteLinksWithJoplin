import urllib.request
import json 

token = 'myJoplinToken' #replace from token from Joplin/Options/WebClipper
baseUrl = 'http://localhost:41184/'
tokenUrlPart = f'&token={token}'
commitChanges = False #Set to True to commit changes to notes
#ToDo - create a backup before we start! https://discourse.joplinapp.org/t/best-method-to-backup-notes/1135

notesUrl = f'{baseUrl}notes?token{token}'

replacements={
    'evernote:///view/guid1/antherGuid1/':':/joplinLink1', #put your evernote links & joplin links here....
    'evernote:///view/guid2/antherGuid2/':':/joplinLink2'
    #etc, etc, etc
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
    print(contents)

#ping()
for key, value in replacements.items():
    old = key
    new = value
    searchAndReplace(old, new)
print('finished!')
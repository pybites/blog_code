import zipfile

from django.http import HttpResponse

from .models import Script

README_NAME = 'README.md'
README_CONTENT = """
## PyBites Code Snippet Archive

Here is a zipfile with some useful code snippets.

Produced for blog post https://pybit.es/django-zipfiles.html

Keep calm and code in Python!
"""
ZIPFILE_NAME = 'pybites_codesnippets.zip'


def download(request):
    """Download archive zip file of code snippets"""
    response = HttpResponse(content_type='application/zip')
    zf = zipfile.ZipFile(response, 'w')

    # create the zipfile in memory using writestr
    # add a readme
    zf.writestr(README_NAME, README_CONTENT)

    # retrieve snippets from ORM and them to zipfile
    scripts = Script.objects.all()
    for snippet in scripts:
        zf.writestr(snippet.name, snippet.code)

    # return as zipfile
    response['Content-Disposition'] = f'attachment; filename={ZIPFILE_NAME}'
    return response

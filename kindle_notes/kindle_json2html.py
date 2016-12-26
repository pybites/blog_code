import json
import sys

from templates import PAGE, QUOTE

JSON_EXT = ".json"
HTML_EXT = ".html"

def load_json(json_file):
    with open(json_file) as f:
        return json.loads(f.read())

def get_highlights(highlights):
    for hl in highlights:
        yield QUOTE.safe_substitute({
            'text' : hl['text'],
            'note' : ' / note: ' + hl['note'] if hl['note'] else '',
            'url' : hl['location']['url'],
            'location': hl['location']['value'],
        })


if __name__ == "__main__": 
    if len(sys.argv) < 2:
        sys.exit("Usage: {} <book1.json book2.json ...>".format(sys.argv[0]))
    
    for json_file in sys.argv[1:]:
        if not json_file.endswith(JSON_EXT):
            print("{} is not a json file".format(json_file))
            continue

        html_out = json_file.replace(JSON_EXT, HTML_EXT)
        
        content = load_json(json_file)
        highlights = get_highlights(content['highlights'])
        with open(html_out, 'w') as f:
            f.write(PAGE.safe_substitute({
                'asin': content['asin'],
                'title': content['title'],
                'author': content['authors'],
                'content': '\n'.join(list(highlights)),
            }))
            print("{} created".format(html_out))

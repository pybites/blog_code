Uses Python3

pip install -r requirements.txt

    $ more pybites_header
    To: <email>
    Subject: Weekly PyBites digest
    Content-Type: text/html

Cronjob:

	$ cat pybites_header <(python3 /path/to/pybites_digest/digest.py) | sendmail -t

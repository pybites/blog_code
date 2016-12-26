from string import Template

PAGE = Template('''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>$title</title>
  <meta name="description" content="$title">
  <meta name="author" content="$author">
  <style>
    h1 { 
        font-size: 1em;
    }
    h2 { 
        font-size: 0.9em;
    }
    body {
        font-family: Georgia, serif;
    }
    li {
        list-style: none; 
    }
    blockquote {
        margin-top: 20px;
        padding: 10px;
        background: #f2f2f2;
        font-style: italic;
        line-height: 1.45;
        color: #383838;
    }
    #meta {
        width: 340px;
        position: fixed;
    }
    #quotes {
        width: 600px;
        margin: 20px 0 0 340px;
    }
  </style>
</head>

<body>
    <div id='meta'>
        <h1>$title</h1>
        <h2>by $author | <a href='https://amazon.com/dp/$asin'>Amazon</a></h2>
        <img src="http://images.amazon.com/images/P/$asin.jpg" alt="$title">
    </div>
    <div id='quotes'>
        $content
    </div>
</body>
</html>''')

QUOTE = Template('''
<li>
    <blockquote>$text (loc: <a href='$url'>$location</a>$note)</blockquote>
</li>''')

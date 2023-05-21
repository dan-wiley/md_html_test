"""
This file gets run after pandoc to perform some finishing touches
"""

from bs4 import BeautifulSoup

def add_class_to_tags(html_file, tag):
    """
    Add class names to specific HTML tags in a file based on the language.

    Args:
        html_file (str): Path to the HTML file.
        tag (str): HTML tag to modify.

    Returns:
        None
    """
    class_map = {
        'java': 'lang-java',
        'js': 'lang-js',
        'jsx': 'lang-jsx',
        'py': 'lang-py',
        'sql': 'lang-sql',
        'cs': 'lang-cs',
        'html': 'lang-html',
        'css': 'lang-css',
        'swift': 'lang-swift'
    }

    with open(html_file, 'r') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    tags = soup.find_all(tag)
    for tag in tags:
        classes = ['prettyprint']
        language = tag.get('class', None)
        if language and language[0] in class_map:
            classes.append(class_map[language[0]])
        tag['class'] = ' '.join(classes)

    with open(html_file, 'w') as f:
        f.write(str(soup))

if __name__ == "__main__":
    html_file = "<path-to-html-file>"
    tag = 'pre'
    add_class_to_tags(html_file, tag)

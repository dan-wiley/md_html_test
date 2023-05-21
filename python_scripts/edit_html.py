from bs4 import BeautifulSoup
import sys

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
        'python': 'lang-py',
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
        if language:
            for lang in language:
                if lang in class_map:
                    classes.append(class_map[lang])
        tag['class'] = ' '.join(classes)

    with open(html_file, 'w') as f:
        f.write(str(soup))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python modify_html.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    tag = 'pre'
    add_class_to_tags(html_file, tag)

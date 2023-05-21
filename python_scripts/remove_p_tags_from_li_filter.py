import sys
from bs4 import BeautifulSoup

def add_class_to_tags(html_file, tag, class_name):
    """
    Add a class to specific HTML tags in a file.

    Args:
        html_file (str): Path to the HTML file.
        tag (str): HTML tag to modify.
        class_name (str): Class name to add to the tag.

    Returns:
        None
    """
    with open(html_file, 'r') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    tags = soup.find_all(tag)
    for tag in tags:
        tag['class'] = class_name

    with open(html_file, 'w') as f:
        f.write(str(soup))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python modify_html.py <html_file> <tag> <class_name>")
        sys.exit(1)

    html_file = sys.argv[1]
    tag = sys.argv[2]
    class_name = sys.argv[3]

    add_class_to_tags(html_file, tag, class_name)

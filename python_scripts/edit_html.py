from bs4 import BeautifulSoup
import sys

def modify_code_tags(html_file, tag):
    """
    Wrap <code> tags in <pre> tags if the immediate parent is not <pre>.
    Adds the 

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
    code_blocks = soup.find_all(tag)
    for code_block in code_blocks:
        pre_tag = code_block.find_parent('pre')
        if pre_tag is None:
            pre_tag = soup.new_tag('pre')
            code_block.wrap(pre_tag)

        classes = ['prettyprint']
        language = code_block.get('class', None)
        if language:
            for lang in language:
                if lang in class_map:
                    classes.append(class_map[lang])
        pre_tag['class'] = ' '.join(classes)

        # Remove tags inside <code> and replace with text
        code_block.unwrap()

    with open(html_file, 'w') as f:
        f.write(str(soup))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python modify_html.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    tag = 'code'
    modify_code_tags(html_file, tag)

from bs4 import BeautifulSoup
import sys

def modify_code_tags(soup):
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
    code_blocks = soup.find_all('code')
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
        del code_block['class']

        for tag in code_block.find_all():
            tag.unwrap()
    return soup
            
def remove_p_tags_from_li(soup):
    li_tags =soup.find_all('li')
    for li in li_tags:
        p_tags =soup.find_all('p')
        for p in p_tags:
            p.unwrap()
    return soup

def blockquotes_to_aside(soup):
    for blockquote in soup.find_all('blockquote'):
        # Create a new aside tag
        aside = soup.new_tag('aside')

        # Replace the blockquote with the aside tag
        blockquote.wrap(aside)

        # Unwrap the blockquote tag without removing children
        blockquote.unwrap()
    return soup 
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python modify_html.py <html_file>")
        sys.exit(1)
        
    html_file = sys.argv[1]
    
    html_content = "<div class='lesson-content'>"
    
    with open(html_file, 'r') as f:
        html_content += f.read() + "</div>"
        
    soup = BeautifulSoup(html_content, 'html.parser')
    soup = modify_code_tags(soup)
    soup = remove_p_tags_from_li(soup)
    soup = blockquotes_to_aside(soup)
    
    with open(html_file, 'w') as f:
        f.write(str(soup))

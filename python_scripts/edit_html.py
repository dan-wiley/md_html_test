    # Create a new <div> tag
    div_tag = soup.new_tag('div', attrs={'class': 'lesson-content'})

    # Extract the contents of the soup object
    contents = soup.contents

    # Clear the existing contents of the soup object
    soup.clear()

    # Append the new <div> tag to the soup object
    soup.append(div_tag)

    # Append the extracted contents to the new <div> tag
    for content in contents:
        div_tag.append(content)

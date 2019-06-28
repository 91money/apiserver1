import base64

def encode(html):
    return base64.b64encode(html.encode()).decode()


def decode(base64_content):
    return base64.b64decode(base64_content.encode()).decode()


if __name__ == '__main__':
    html = '''
    <div class="editor-body">
        <p> 1. 我很好</p>
        <strong> 2.百度</strong>
    </div>
    '''

    content = encode(html)
    print(content)


    html = decode(content)
    print({
        'content': str(html).replace('\n', '<br>')
    })
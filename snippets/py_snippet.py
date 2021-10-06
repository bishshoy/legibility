from legibility import LaTeXPage


def main(_compile_):
    page = LaTeXPage(
        name='{{name}}',
        files_dir='{{files_dir}}',
        images_dir='{{images_dir}}'
    )

    page.text(
        '''
        
        '''
    )

    if _compile_:
        page.compile()

    return page


if __name__ == '__main__':
    main(_compile_=True)

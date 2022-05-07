from legibility import LaTeXTable


def main(_compile_):
    table = LaTeXTable(
        name='{{name}}', files_dir='{{files_dir}}', images_dir='{{images_dir}}', tables_dir='{{tables_dir}}'
    )

    table.initialize()

    if _compile_:
        table.compile()

    return table


if __name__ == '__main__':
    main(_compile_=True)

import click


def test_cli(cli_runner):

    @click.command()
    @click.argument('name')
    def hello(name):
        click.echo('Hello %s!' % name)

    result = cli_runner.invoke(hello, ['Peter'])
    assert result.exit_code == 0
    assert result.output == 'Hello Peter!\n'


def test_fixture(isolated_cli_runner):

    @click.command()
    @click.argument('f', type=click.File())
    def cat(f):
        click.echo(f.read())

    with open('hello.txt', 'w') as f:
        f.write('Hello World!')

    result = isolated_cli_runner.invoke(cat, ['hello.txt'])
    assert result.exit_code == 0
    assert result.output == 'Hello World!\n'

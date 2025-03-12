import click

@click.command()
def hello():
    """Simple CLI Test Command"""
    click.echo("Hello, your CLI is working!")

if __name__ == '__main__':
    hello()


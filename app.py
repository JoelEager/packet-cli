"""
Entry point for the packet CLI
"""

import click
import requests


@click.group()
def cli():
    pass


@cli.command()
@click.argument("id")
def packet(id):
    """
    Fetches a packet based on id
    """
    print(id)


@cli.command()
@click.argument("username")
def freshman(username):
    """
    Fetches a freshman based on username
    """
    print(username)


@cli.command()
@click.argument("term")
def search(term):
    """
    Searches for freshmen based on their names
    """
    print(term)


@cli.command()
@click.argument("sign")
def sign(username):
    """
    Signs the current packet of the freshmen with the given username
    """
    print(username)


if __name__ == '__main__':
    cli()

"""
Entry point for the packet CLI
"""

from os import environ
from sys import exit
from urllib import parse
import click
import requests

cookie_token = environ.get("PACKET_TOKEN", None)
packet_server = environ.get("PACKET_SERVER", "packet.csh.rit.edu")


@click.group()
def cli():
    """
    Top-level group of packet commands
        Handles setup work for the CLI
    """
    if cookie_token is None:
        print("ERROR: Please set the PACKET_TOKEN environment variable to your packet session cookie.")
        exit(1)


def make_request(method, path):
    """
    Helper method for making REST calls and handling errors
    :param method: The requests.<verb>() function to call
    :param path: The path portion of the URL
    :return: The parsed JSON
    """
    resp = method(parse.urljoin("http://" + packet_server, path) + "/", cookies={"session": cookie_token})

    if len(resp.history) != 0:
        # Redirect happened indicating auth failure
        print("ERROR: The server did not accept the token in the PACKET_TOKEN environment variable.")
        exit(1)
    elif resp.status_code != 200:
        print("ERROR: The API call to the server failed.")
        try:
            print(resp.json()["description"])
        except (ValueError, KeyError):
            pass
    else:
        # Everything looks good, return the parsed JSON
        return resp.json()


@cli.command()
@click.argument("id")
def packet(id):
    """
    Fetches a packet based on id
    """
    packet = make_request(requests.get, parse.urljoin("/api/packet/", id))

    print(packet["freshman_name"] + "'s packet:")

    if packet["open"]:
        print("\tOpen until " + packet["end"])
    else:
        print("\tOpen from " + packet["start"] + " to " + packet["end"])

    print()
    received = packet["signatures_received"]
    required = packet["signatures_required"]
    print("\tUpperclassmen score: {:0.2f}%".format(received["member_total"] / required["member_total"] * 100))
    print("\tTotal score: {:0.2f}%".format(received["total"] / required["total"] * 100))
    print("\tEboard: {}/{}".format(received["eboard"], required["eboard"]))
    print("\tUpperclassmen: {}/{}".format(received["upper"], required["upper"]))
    print("\tFreshmen: {}/{}".format(received["fresh"], required["fresh"]))
    print("\tMiscellaneous: {}/{}".format(received["misc"], required["misc"]))
    print("\tTotal missed:", required["total"] - received["total"])


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

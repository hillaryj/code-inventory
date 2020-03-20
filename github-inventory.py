#!/usr/bin/env python
"""Retrieve and format a list of github repos with details.

[description]
"""

# Python library imports
import logging
from github import Github


__author__ = "Hillary Jeffrey"
__copyright__ = "Copyright 2020"
__credits__ = ["Hillary Jeffrey"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Hillary Jeffrey"
__status__ = "Development"


# Globals
# Debug settings
LOG_LEVEL = logging.INFO

# Output fields
outfields = []


# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=LOG_LEVEL, format="%(levelname)s - %(message)s")


def get_repos(user_token):
    """Get and return a list of repos."""
    g = Github(user_token)

    return g.get_user().get_repos()


def list_repos(gh_repo_list, print_to_screen=True):
    """Given a Github Paginated List, returns a dictionary."""
    repos = {}
    for repo in gh_repo_list:
        org = repo.organization
        reponame = repo.name

        if not org:
            orgname = repo.owner.login
        else:
            orgname = org.name
        if orgname not in repos:
            repos[orgname] = {}

        namestr = "{}\\{}".format(orgname, reponame)
        if print_to_screen:
            logging.info(namestr)
        else:
            logging.debug(namestr)
        repos[orgname][namestr] = repo

    return repos


def repo_details(gh_repo_list):
    """Given a Github Paginated List, gets details and returns a JSON dict."""
    deets = {}
    return deets


def save_file(filepath, data, filetype="csv"):
    """Save data to a specified output file."""
    return


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Exports repositories and details from Github."
    )
    parser.add_argument(
        "-t",
        "--token",
        metavar="TOKEN",
        type=str,
        dest="user_token",
        help="Specifies a user token to use to access Github",
    )
    parser.add_argument(
        "-o",
        "--out",
        metavar="OUTPATH",
        type=str,
        dest="out_path",
        help="Output file path, including extension (supported: csv)",
    )
    args = parser.parse_args()

    if args.user_token is not None:
        user_token = args.user_token
    else:
        # no token specified, quit
        logging.error("No token specified, exiting.")

    if args.out_path is None:
        # No destination specified, print to screen
        logging.info("No output path specified, will print to screen")
        # outscreen = True
    outpath = args.out_path

    logging.info("Retrieving repositories:")

    repos = list_repos(get_repos(user_token))

    logging.info(
        "Operation complete!\nRetrieved {} repos in {} namespaces".format(
            sum([len(orgrepos) for orgrepos in repos]), len(repos)
        )
    )

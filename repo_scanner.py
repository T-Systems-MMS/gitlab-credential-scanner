#!/usr/bin/env python3
"""
A script to run kics scans on multiple gitlab repositories in a row.
"""

# import our used python libraries
import logging
import subprocess
import tempfile
from argparse import ArgumentParser
from gitlab import Gitlab, GitlabListError, GitlabAuthenticationError
from git import Repo
from jinja2 import Environment, FileSystemLoader

# initialize logging and set it to INFO
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%y %H:%M:%S",
)

parser = ArgumentParser()
parser.add_argument(
    "--scan-repo",
    help="scan explicit repo with this name",
    required=False,
    default=False,
    dest="scan_repo",
)
parser.add_argument(
    "--gitlab-hostname",
    help="hostname of gitlab (e.g. git.example.com)",
    required=True,
    dest="gitlab_hostname",
)
parser.add_argument(
    "--gitlab-access-token",
    help="access token for project or projects",
    required=True,
    dest="gitlab_access_token",
)
parser.add_argument(
    "--template-name",
    help="name of the template file used for the ticket description",
    required=False,
    default='default_issue_description.j2',
    dest="template_name",
)
args = parser.parse_args()

gitlab_url = f"https://{args.gitlab_hostname}"
gitlab_url_with_login = (
    f"https://scanner:{args.gitlab_access_token}@{args.gitlab_hostname}"
)

# login to gitlab with private token
gl = Gitlab(gitlab_url, private_token=args.gitlab_access_token)

# get a list of all projects
try:
    logging.info("fetch list of all projects from %s", gitlab_url)

    if args.scan_repo:
        projects = gl.projects.list(search=args.scan_repo, order_by="id", min_access_level=20)
    else:
        projects = gl.projects.list(get_all=True, order_by='id', min_access_level=20)
except GitlabListError:
    logging.error("can't fetch list from %s", gitlab_url)
except GitlabAuthenticationError:
    logging.error("cannot authenticate against %s", gitlab_url)

logging.debug(projects)

def create_description(scanner_output):
    """
    function to create the description for gitlab issue
    """
    env = Environment(
      loader = FileSystemLoader('./templates/')
    )

    template = env.get_template(f'{args.template_name}')
    description = template.render(scanner_output=scanner_output)

    return description

def create_issue(project, scanner_output):
    """
    function to create a issue in out GitLab if we found something with our scan
    """
    issue_list = project.issues.list(labels=["automated-credential-scan"])

    if len(issue_list) > 0:
        logging.debug("there is already an issue")
        issue = issue_list[0]
        if issue.state == "closed":
            issue.state_event = "reopen"
        issue.description = create_description(scanner_output=scanner_output)
        issue.save()
    else:
        project.issues.create(
            {
                "title": "Automated credential scan",
                "description": create_description(scanner_output=scanner_output),
                "labels": ["automated-credential-scan"],
            }
        )


for p in projects:
    project_id = getattr(p, "id")
    project_path = getattr(p, "path_with_namespace")
    project_url = f"{gitlab_url_with_login}/{project_path}.git"

    # skip project if there is an issue to disable scanning
    if len(p.issues.list(labels=["automated-credential-scan-disabled"])) > 0:
        logging.info(
            '%s has label "automated-credential-scan-disabled" - skipping', project_path
        )
        continue

    logging.debug(project_url)
    tmpdir = tempfile.TemporaryDirectory(prefix="kics-scan")

    logging.debug("%s: cloning", project_path)
    Repo.clone_from(url=project_url, to_path=tmpdir.name, multi_options=['--depth 1'])
    logging.debug("%s: clone done", project_path)

    logging.info("%s: starting kics scan", project_path)
    scanner = subprocess.run(
        [
            "kics",
            "scan",
            "-i",
            "a88baa34-e2ad-44ea-ad6f-8cac87bc7c71",
            "--no-color",
            "-p",
            ".",
        ],
        cwd=tmpdir.name,
        capture_output=True,
        check=False,
    )

    if scanner.returncode != 0:
        logging.info(
            "%s: returncode is %s - create a ticket", project_path, scanner.returncode
        )
        create_issue(project=p, scanner_output=scanner.stdout.decode("utf-8"))
    else:
        logging.info("kics scan successful")

    tmpdir.cleanup()

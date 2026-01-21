import os
from glob import glob

import click
import importlib_resources
from tutor import hooks

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        ("ENTERPRISE_ACCESS_ENABLED", True),
        ("ENTERPRISE_ACCESS_REPO", "https://github.com/openedx/enterprise-access.git"),
        ("ENTERPRISE_ACCESS_HOST", "enterprise-access.{{ LMS_HOST }}"),
        ("ENTERPRISE_ACCESS_PORT", 18100),

        # Database (reuse Tutor's MySQL)
        ("ENTERPRISE_ACCESS_MYSQL_DATABASE", "enterprise_access"),
        ("ENTERPRISE_ACCESS_MYSQL_USERNAME", "enterprise_access"),

        # Redis (reuse Tutor's Redis; default to its own DB index)
        ("ENTERPRISE_ACCESS_REDIS_DB", 9),

        # Docker image tag built by this plugin
        ("ENTERPRISE_ACCESS_DOCKER_IMAGE", "{{ DOCKER_REGISTRY }}enterprise-access:{{ OPENEDX_COMMON_VERSION }}"),

        # OAuth2 clients (created in LMS during init)
        ("ENTERPRISE_ACCESS_OAUTH2_KEY_DEV", "enterprise-access-dev"),
        ("ENTERPRISE_ACCESS_OAUTH2_KEY_SSO_DEV", "enterprise-access-sso-dev"),
        ("ENTERPRISE_ACCESS_OAUTH2_KEY", "enterprise-access"),
        ("ENTERPRISE_ACCESS_OAUTH2_KEY_SSO", "enterprise-access-sso"),
    ]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        ("ENTERPRISE_ACCESS_MYSQL_PASSWORD", "{{ 24|random_string }}"),
        ("ENTERPRISE_ACCESS_DJANGO_SECRET_KEY", "{{ 50|random_string }}"),
        ("ENTERPRISE_ACCESS_OAUTH2_SECRET_DEV", "{{ 32|random_string }}"),
        ("ENTERPRISE_ACCESS_OAUTH2_SECRET_SSO_DEV", "{{ 32|random_string }}"),
        ("ENTERPRISE_ACCESS_OAUTH2_SECRET", "{{ 32|random_string }}"),
        ("ENTERPRISE_ACCESS_OAUTH2_SECRET_SSO", "{{ 32|random_string }}"),
    ]
)


########################################
# INITIALIZATION TASKS
########################################

# Init tasks are executed by `tutor local do init --limit=...`
# We register them by reading the bash templates we ship.
INIT_TASKS = [
    ("mysql", ("enterprise-access", "tasks", "mysql", "init.sh")),
    ("lms", ("enterprise-access", "tasks", "lms", "init.sh")),
    ("enterprise-access", ("enterprise-access", "tasks", "enterprise-access", "init.sh")),
]

for service, template_path in INIT_TASKS:
    full_path = str(
        importlib_resources.files("tutorenterprise_access")
        / os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as f:
        hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, f.read()))

########################################
# DOCKER IMAGE MANAGEMENT
########################################

# Build an enterprise-access image from the upstream repo
hooks.Filters.IMAGES_BUILD.add_item(
    (
        "enterprise-access",
        ("plugins", "enterprise-access", "build", "enterprise-access"),
        "{{ ENTERPRISE_ACCESS_DOCKER_IMAGE }}",
        (
            "OPENEDX_IMAGE={{ DOCKER_IMAGE_OPENEDX }}",
            "ENTERPRISE_ACCESS_REPO={{ ENTERPRISE_ACCESS_REPO }}",
        ),
    )
)
hooks.Filters.IMAGES_PUSH.add_item(("enterprise-access", "{{ ENTERPRISE_ACCESS_DOCKER_IMAGE }}"))
hooks.Filters.IMAGES_PULL.add_item(("enterprise-access", "{{ ENTERPRISE_ACCESS_DOCKER_IMAGE }}"))


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        str(importlib_resources.files("tutorenterprise_access") / "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutorenterprise_access/templates/enterprise-access/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/enterprise-access/build``.
    [
        ("enterprise-access/build", "plugins"),
        ("enterprise-access/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorenterprise_access/patches,
# apply a patch based on the file's name and contents.
for path in glob(str(importlib_resources.files("tutorenterprise_access") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################

# A job is a set of tasks, each of which run inside a certain container.
# Jobs are invoked using the `do` command, for example: `tutor local do importdemocourse`.
# A few jobs are built in to Tutor, such as `init` and `createuser`.
# You can also add your own custom jobs:


# To add a custom job, define a Click command that returns a list of tasks,
# where each task is a pair in the form ("<service>", "<shell_command>").
# For example:
### @click.command()
### @click.option("-n", "--name", default="plugin developer")
### def say_hi(name: str) -> list[tuple[str, str]]:
###     """
###     An example job that just prints 'hello' from within both LMS and CMS.
###     """
###     return [
###         ("lms", f"echo 'Hello from LMS, {name}!'"),
###         ("cms", f"echo 'Hello from CMS, {name}!'"),
###     ]


# Then, add the command function to CLI_DO_COMMANDS:
## hooks.Filters.CLI_DO_COMMANDS.add_item(say_hi)

# Now, you can run your job like this:
#   $ tutor local do say-hi --name="Cannon Smith"


#######################################
# CUSTOM CLI COMMANDS
#######################################

# Your plugin can also add custom commands directly to the Tutor CLI.
# These commands are run directly on the user's host computer
# (unlike jobs, which are run in containers).

# To define a command group for your plugin, you would define a Click
# group and then add it to CLI_COMMANDS:


### @click.group()
### def enterprise-access() -> None:
###     pass


### hooks.Filters.CLI_COMMANDS.add_item(enterprise-access)


# Then, you would add subcommands directly to the Click group, for example:


### @enterprise-access.command()
### def example_command() -> None:
###     """
###     This is helptext for an example command.
###     """
###     print("You've run an example command.")


# This would allow you to run:
#   $ tutor enterprise-access example-command

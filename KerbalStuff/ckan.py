import json
import os
import re
import subprocess

from flask import url_for
from github import Github

from .config import _cfg


# TODO(Thomas): Make this modular
def send_to_ckan(mod):
    if not _cfg("netkan_repo_path"):
        return
    if not mod.ckan:
        return
    json_blob = {
        'spec_version': 'v1.4',
        'identifier': re.sub(r'\W+', '', mod.name),
        '$kref': '#/ckan/spacedock/' + str(mod.id),
        'license': mod.license.replace(' ', '-'),
        'x_via': 'Automated ' + _cfg('site-name') + ' CKAN submission'
    }
    wd = _cfg("netkan_repo_path")
    path = os.path.join(wd, 'NetKAN', json_blob['identifier'] + '.netkan')

    if os.path.exists(path):
        # If the file is already there, then chances are this mod has already been indexed
        return

    with open(path, 'w') as f:
        f.write(json.dumps(json_blob, indent=4))
    subprocess.call(['git', 'fetch', 'upstream'], cwd=wd)
    subprocess.call(['git', 'checkout', '-b', 'add-' + json_blob['identifier'], 'upstream/master'], cwd=wd)
    subprocess.call(['git', 'add', '-A'], cwd=wd)
    subprocess.call(['git', 'commit', '-m', 'Add {0} from '.format(mod.name) + _cfg('site-name') + '\n\nThis is an automated commit on behalf of {1}'\
            .format(mod.name, mod.user.username), '--author={0} <{1}>'.format(mod.user.username, mod.user.email)], cwd=wd)
    subprocess.call(['git', 'push', '-u', 'origin', 'add-' + json_blob['identifier']], cwd=wd)
    g = Github(_cfg('github_user'), _cfg('github_pass'))
    r = g.get_repo("KSP-CKAN/NetKAN")
    r.create_pull(title="Add {0} from ".format(mod.name) + _cfg('site-name'), base=r.default_branch, head=_cfg('github_user') + ":add-" + json_blob['identifier'], body=\
"""\
This pull request was automatically generated by """ + _cfg('site-name') + """ on behalf of {0}, to add [{1}]({4}{2}) to CKAN.

Please direct questions about this pull request to [{0}]({4}{3}).

Mod details:
    name = {2}
    author = {0}
    abstract = {6}
    license = {7}
    Homepage = {8}
    description =
{5}
""".format(mod.user.username, mod.name,
           url_for('mods.mod', mod_name=mod.name, id=mod.id),
           url_for("profile.view_profile", username=mod.user.username),
           _cfg("protocol") + "://" + _cfg("domain"),
           mod.description, mod.short_description,
           mod.license, mod.external_link))

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.project import rsync_project
from os.path import join

env.hosts = ['nwittstock@pi.north.lan']
REMOTE_DIR = '/var/www'
REMOTE_SETTINGS_FILE = 'app/deej/local_settings_north.py'
FAVICONS = {
    'ico': {
        'size': 32,
        'name': 'favicon.ico',
    },
    'apple-57': {
        'size': 57,
        'name': 'apple-touch-icon-precomposed.png',
    },
    'apple-72': {
        'size': 72,
        'name': 'apple-touch-icon-72x72-precomposed.png',
    },
    'apple-114': {
        'size': 114,
        'name': 'apple-touch-icon-114x114-precomposed.png',
    },
    'apple-144': {
        'size': 144,
        'name': 'apple-touch-icon-144x144-precomposed.png',
    },
    'fb': {
        'size': 300,
        'name': 'opengraph-icon.png',
    },
}

EXCLUDE_LIST = ['app/deej/local_settings.py',
                'fabfile.py',
                'venv',
                'upload/*',
                'media/*',
                '*.pyc',
                '*.pyo',
                ]


def prepare_staticfiles():
    make_favicons()
    local('rm -rf static')
    with lcd('app'):
        local('./manage.py collectstatic')


def commit(message=None):
    with settings(warn_only=True):
        result = local("git add -p")
    if result.failed and not confirm("`git add` returned some errors. Commit anyway?"):
        abort("Aborting at user request.")
    if message:
        local('git commit -m "%s"' % message)
    else:
        local('git commit')


def push():
    local("git push")


def prepare_deploy():
    commit()
    push()
    prepare_staticfiles()


def deploy():
    # verify that the directory exists on remote host, fail if not
    with settings(warn_only=True):
        result = run("test -d %s" % REMOTE_DIR)
    if result.failed and not confirm("The remote deployment doesn't exist, try to clone it?"):
        abort("Aborting at user request.")

    # make a place for our new static files and transfer, then kill the old dir
    with settings(warn_only=True):
        rsync_project(local_dir='./', remote_dir=REMOTE_DIR, delete=True, exclude=EXCLUDE_LIST, extra_opts="-O")

    with cd("%s/app/deej" % REMOTE_DIR):
        run("mv local_settings_north.py local_settings.py")

    with cd(REMOTE_DIR):
        run("sudo chown -R www-data .")

    # now reload httpd
    # run("sudo service httpd reload")


def make_favicons():
    with lcd("assets/favicons/"):
        for k, v in FAVICONS.items():
            local("convert favicon.svg -resize %s %s" % (v['size'], v['name']))


from fabconfig import *

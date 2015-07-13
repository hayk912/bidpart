from fabric.api import *
from fabric.contrib.console import confirm
from fabric.operations import prompt, local
from fabtools import require


project_dir = "/var/www/bidpart-django"
project_env = "/etc/envs/bidpart-django"
manage_file = "%s/manage.py" % project_dir
python_bin = "%s/bin/python" % project_env
uwsgi_pid = "/var/www/bidpart-django/uwsgi.pid"


@parallel
@roles("www", "cdn", "db")
def _ensure_deb_packages():
    require.deb.packages([
        'wkhtmltopdf'
    ])


@roles("db")
def _install_crontab():
    sudo("%s %s crontab add" % (python_bin, manage_file))


@parallel
@roles("www", "cdn", "db")
def _git_pull(branch):
    with cd(project_dir):
        git_status = sudo('git status')

        if not 'nothing to commit' in git_status:
            abort('There is uncommited changes on the server.')

        sudo('git fetch')
        sudo('git checkout %s' % branch)
        sudo('git pull origin %s' % branch)


@parallel
@roles("www", "cdn", "db")
def _ensure_pip_packages():
    # Make sure we own both the virtualenv and the project dir so we can install the packages safely
    sudo("chown -hR nobody:developers %s" % project_env)
    sudo("chown -hR nobody:developers %s" % project_dir)

    with cd(project_dir):
        with prefix("source %s/bin/activate" % project_env):
            run('pip install -r requirements.txt')


@roles("db")
def _migrate_db():
    with cd(project_dir):
        with prefix("source %s/bin/activate" % project_env):
            run('./manage.py syncdb --migrate')


@roles("cdn")
def _collect_static():
    with cd(project_dir):
        with prefix("source %s/bin/activate" % project_env):
            run('./manage.py collectstatic --noinput')


@parallel
@roles("cdn", "www")
def _compress_static():
    with cd(project_dir):
        sudo('rm -rf static/*')
        with prefix("source %s/bin/activate" % project_env):
            run('./manage.py compress')


@parallel
@roles("www")
def _restart_uwsgi():
    sudo("kill -HUP `cat %s`" % uwsgi_pid)


def deploy_prod(branch='master', username=None, skip_pip=False):
    env.hosts = ['stan.area59.se', 'kenny.area59.se', 'butters.area59.se', 'cartman.area59.se']
    env.roledefs = {
        'www': ['stan.area59.se', 'kenny.area59.se'],
        'cdn': ['butters.area59.se'],
        'db': ['cartman.area59.se']
    }

    if branch is None:
        branch = "master"

        if not confirm("Deploy the %s branch on server?" % branch):
            abort("Aborting.")

    if username is None:
        if not confirm("Are you %s?" % env.user):
            env.user = prompt("Username:")
    else:
        env.user = username

    if not env.user:
        abort("I dont know who you are.")

    execute(_git_pull, branch=branch)
    if not skip_pip:
        execute(_ensure_pip_packages)
    else:
        print "skipping pip"
    execute(_ensure_deb_packages)
    execute(_install_crontab)
    execute(_migrate_db)
    execute(_compress_static)
    execute(_collect_static)
    execute(_restart_uwsgi)
    print "-------------"
    print "TODO:"
    print "- Manually add APBS ads"


def deploy_stage(branch='stage', username=None, skip_pip=False):
    global project_dir
    global project_env
    global uwsgi_pid
    global manage_file
    global python_bin

    project_dir = "/var/www/bidpart-2-0"
    project_env = "/etc/envs/bidpart-2-0"
    uwsgi_pid = "/var/www/bidpart-2-0/uwsgi.pid"

    manage_file = "%s/manage.py" % project_dir
    python_bin = "%s/bin/python" % project_env

    env.hosts = ['marge.returngreat.com']
    env.roledefs = {
        'www': ['marge.returngreat.com'],
        'cdn': ['marge.returngreat.com'],
        'db': ['marge.returngreat.com']
    }

    if branch is None:
        branch = "stage"

        if not confirm("Deploy the %s branch on server?" % branch):
            abort("Aborting.")

    if username is None:
        if not confirm("Are you %s?" % env.user):
            env.user = prompt("Username:")
    else:
        env.user = username

    if not env.user:
        abort("I dont know who you are.")

    execute(_git_pull, branch=branch)
    if not skip_pip:
        execute(_ensure_pip_packages)
    else:
        print "skipping pip"

    execute(_ensure_deb_packages)
    execute(_install_crontab)
    execute(_migrate_db)
    execute(_compress_static)
    execute(_collect_static)
    execute(_restart_uwsgi)


def deploy_dev(branch='dev', username=None, skip_pip=False):
    #local('open /Applications/Safari.app http://media.tumblr.com/tumblr_maljispYL31ruql5i.gif')
    env.hosts = ['timmy.area59.se']
    env.roledefs = {
        'www': ['timmy.area59.se'],
        'cdn': ['timmy.area59.se'],
        'db': ['timmy.area59.se']
    }

    if branch is None:
        branch = "dev"

        if not confirm("Deploy the %s branch on server?" % branch):
            abort("Aborting.")

    if username is None:
        if not confirm("Are you %s?" % env.user):
            env.user = prompt("Username:")
    else:
        env.user = username

    if not env.user:
        abort("I dont know who you are.")

    execute(_git_pull, branch=branch)
    if not skip_pip:
        execute(_ensure_pip_packages)
    else:
        print "skipping pip"
    execute(_ensure_deb_packages)
    execute(_install_crontab)
    execute(_migrate_db)
    execute(_compress_static)
    execute(_collect_static)
    execute(_restart_uwsgi)


def import_old(path=None, empty_db=False):
    types = (
        'users',
        'producttypes',
        'ads',
        'uploads'
    )
    if not path:
        abort("Please specify a path.")

    db = ""
    if empty_db:
        db = "--use-empty=1"

    for type in types:
        local('./manage.py import --path=%s --type=%s %s' % (path, type, db))

"""
Role tests
"""

import re

import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


@pytest.mark.parametrize('name', [
    ('openjdk-8-jdk'),
])
def test_packages(host, name):
    """
    Test installed packages
    """

    assert host.package(name).is_installed


def test_user(host):
    """
    Test zeppelin user
    """

    app_user = host.user('zeppelin')
    assert app_user.exists
    assert app_user.home == '/var/lib/zeppelin'


def test_group(host):
    """
    Test zeppelin group
    """

    app_user = host.user('zeppelin')
    assert app_user.exists


@pytest.mark.parametrize('folder_path,user,group,mode', [
    ('/var/lib/zeppelin', 'zeppelin', 'zeppelin', 0o750),
    ('/var/log/zeppelin', 'zeppelin', 'zeppelin', 0o750),
    ('/var/run/zeppelin', 'zeppelin', 'zeppelin', 0o750),
])
def test_folders(host, folder_path, user, group, mode):
    """
    Test app paths
    """

    current_folder = host.file(folder_path)

    assert current_folder.exists
    assert current_folder.is_directory
    assert current_folder.user == user
    assert current_folder.group == group
    assert current_folder.mode == mode


@pytest.mark.parametrize('file_path,user,group,mode', [
    (
        '/var/lib/zeppelin/current/conf/zeppelin-site.xml',
        'zeppelin',
        'zeppelin',
        0o400
    ),
    (
        '/var/lib/zeppelin/current/conf/zeppelin-env.sh',
        'zeppelin',
        'zeppelin',
        0o500
    ),
    (
        '/var/lib/zeppelin/current/conf/shiro.ini',
        'zeppelin',
        'zeppelin',
        0o400
    ),
])
def test_config_files(host, file_path, user, group, mode):
    """
    Test app paths
    """

    current_file = host.file(file_path)

    assert current_file.exists
    assert current_file.is_file
    assert current_file.user == user
    assert current_file.group == group
    assert current_file.mode == mode


def test_current_link(host):
    """
    Test app paths
    """

    current_link = host.file('/var/lib/zeppelin/current')

    assert current_link.exists
    assert current_link.is_symlink
    assert re.search('zeppelin-\d+.\d+.\d+-bin-all', current_link.linked_to)


def test_service(host):
    """
    Test service
    """

    assert host.service('zeppelin').is_running
    assert host.service('zeppelin').is_enabled


def test_socket(host):
    """
    Test socket
    """

    assert host.socket('tcp://:::8080').is_listening

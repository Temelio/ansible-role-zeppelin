"""
Role tests
"""

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


@pytest.mark.parametrize('folder_path,user,group,mode', [
    (''),
])
def test_folders(host, folder_path, user, group, mode):
    """
    Test app paths
    """

    current_folder = host.file(folder_path)

    assert current_folder.exists
    assert current_folder.is_directory

"""
Role tests
"""

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_foo_a(User):
    assert User().name == 'root'


def test_foo_b(User):
    assert User().name == 'root'

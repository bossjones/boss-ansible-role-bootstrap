import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts.molecule')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644
    assert f.content_string == '127.0.1.2\tbootstrap-xenial'

@pytest.mark.parametrize('f',
                         ['python', 'python-apt', 'python-pip', 'sudo', 'lsb-release'])
def test_packages_installed(host, f):
    pkg = host.package(f)
    assert pkg.is_installed

# EXAMPLE: https://github.com/activatedio/ansible-simplestack/blob/c489220dc5c633cc5e1411c09aa34a0c77aee86c/molecule/default/tests/test_default.py
# def test_stack_setup_in_kvm_group(host):
#     u = host.user('stack')

#     assert 'kvm' in u.groups

def test_passwd_file(host):
    passwd = host.file("/etc/passwd")
    assert passwd.contains("bossjones")
    assert passwd.user == "root"
    assert passwd.group == "root"
    assert passwd.mode == 0o644

def test_sudoers_admin_file(host):
    sudoes_admins = host.file("/etc/sudoers.d/admins")
    assert sudoes_admins.contains('Defaults: %admins !requiretty')
    assert sudoes_admins.contains('Defaults: %admins env_check += "SSH_CLIENT"')
    assert sudoes_admins.contains('%admins ALL = (ALL:ALL) NOPASSWD: SETENV: ALL')

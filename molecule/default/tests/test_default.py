import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

admin_password = 'adminpassword'


def test_jenkins_service(host):
    jenkins = host.service('jenkins')

    assert jenkins.is_enabled
    assert jenkins.is_running


def test_cron(host):
    datagov_jenkins = host.file('/etc/cron.daily/datagov-jenkins')

    assert datagov_jenkins.user == 'root'
    assert datagov_jenkins.group == 'root'
    assert datagov_jenkins.mode == 0o755


def test_jenkins_credentials(host):
    credentials = host.file('/root/jenkins.txt')

    assert credentials.user == 'root'
    assert credentials.group == 'root'
    assert credentials.mode == 0o640
    assert credentials.contains('admin:%s' % admin_password)

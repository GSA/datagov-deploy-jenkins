import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_jenkins_service(host):
    jenkins = host.service('jenkins')

    assert jenkins.is_enabled
    assert jenkins.is_running

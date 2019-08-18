# datagov-deploy-jenkins

Ansible role to install Jenkins for the Data.gov platform.

This installs a production single-instance Jenkins with Nginx to terminate SSL.

The following plugins are installed. You may install additional plugins by
specifying them in the `jenkins_additional_plugins` variable.

- ansible
- ansicolor
- audit-trail
- aws-credentials
- blueocean
- docker
- github
- packer
- periodicbackup
- pipeline-utility-steps
- role-strategy
- saml
- ssh-agent
- timestamper
- workflow-aggregator
- ws-cleanup


## Usage

Install [geerlingugy.jenkins](https://github.com/geerlingguy/ansible-role-jenkins).

Example playbook.

```
---
- name: Install
  hosts: all
  roles:
    - gsa.datagov-deploy-jenkins
```


### Variables

In addition to the variables available for
[geerlingugy.jenkins](https://github.com/geerlingguy/ansible-role-jenkins),
these variables are also available.


#### `jenkins_admin_user` string (default: admin)

The admin username to create.


#### `jenkins_admin_password` string required

The admin password to assign.


#### `jenkins_additional_plugins` list of string (default: [])

Additional Jenkins plugins to install.


#### `jenkins_tls_cert` string required

File content for the TLS/SSL certificate to serve for your Jenkins instance.


#### `jenkins_tls_key` string required

File content for the TLS/SSL key to serve for your Jenkins instance.


## Development

Requirements:

- Docker v18
- pipenv

Install the dependencies.

    $ pipenv install --dev

Run the tests.

    $ pipenv run test


### Accessing Jenkins

Once converged in molecule, you can access the Jenkins image locally. First, get
the IP address of the docker container.

    $ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' jenkins-bionic

Then open your web browser to that IP on port 8080.


## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for additional information.

## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.

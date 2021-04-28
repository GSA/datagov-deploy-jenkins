[![CircleCI](https://circleci.com/gh/GSA/datagov-deploy-jenkins.svg?style=svg)](https://circleci.com/gh/GSA/datagov-deploy-jenkins)

# datagov-deploy-jenkins

Ansible role to install Jenkins for the Data.gov platform.

## Features

- Production single-instance [Jenkins](https://jenkins.io)
- SSL termination with [Nginx](https://nginx.org)
- Automatic updates for plugins


### Plugins

The following plugins are installed. You may install additional plugins by
specifying them in the `jenkins_additional_plugins` variable.

- [ansible](https://plugins.jenkins.io/ansible) allows to execute Ansible tasks
  as a job build step
- [ansicolor](https://plugins.jenkins.io/ansicolor) _(enable in pipeline)_ add
  ANSI escape sequences, including color, to Console Output
- [audit-trail](https://plugins.jenkins.io/audit-trail) _(requires
  configuraiton)_ keeps a log of who performed particular Jenkins operations, such
  as configuring jobs
- [aws-credentials](https://plugins.jenkins.io/aws-credentials) allows storing
  Amazon IAM credentials within the Jenkins Credentials API
- [configuration-as-code](https://plugins.jenkins.io/configuration-as-code/)
  an opinionated way to configure Jenkins based on human-readable declarative
  configuration files
- [blueocean](https://plugins.jenkins.io/blueocean) is a new Jenkins UI
  optimized for user experience; it reduces clutter and increases clarity for
  every member of your team
- [github](https://plugins.jenkins.io/github) integrates Jenkins with
  [GitHub](https://github.com) projects
- [github-issues](https://plugins.jenkins.io/github-issues) create GitHub issues
  on build failures
- [job-dsl](https://plugins.jenkins.io/job-dsl/) define jobs in a programmatic form
  in a human readable file
- [packer](https://plugins.jenkins.io/packer) allows [Packer](https://packer.io)
  tasks to build and publish AMI and OS images
- [periodicbackup](https://plugins.jenkins.io/periodicbackup) _(requires
  configuration)_ allows archiving and restoring your Jenkins (and Hudson) home
  directory
- [pipeline-utility-steps](https://plugins.jenkins.io/pipeline-utility-steps)
  adds small, miscellaneous, cross platform [utility
  steps](https://github.com/jenkinsci/pipeline-utility-steps-plugin/blob/master/docs/STEPS.md)
  for [Pipeline Plugin](https://plugins.jenkins.io/workflow-aggregator) jobs
- [role-strategy](https://plugins.jenkins.io/role-strategy) adds a new
  role-based strategy to manage users' permissions
- [saml](https://plugins.jenkins.io/saml) _(requires configuration)_ allows
  authentication to Jenkins via the SAML 2.0 protocol
- [ssh-agent](https://plugins.jenkins.io/ssh-agent) allows you to provide SSH
  credentials to builds via a ssh-agent in Jenkins
- [timestamper](https://plugins.jenkins.io/timestamper) _(enable in pipeline)_
  adds timestamps to the Console Output
- [workflow-aggregator](https://plugins.jenkins.io/workflow-aggregator) a.k.a.
  Pipeline, a suite of plugins that lets you orchestrate simple or complex
  automation
- [ws-cleanup](https://plugins.jenkins.io/ws-cleanup) _(requires
  configuraiton)_ declared build wrapper and post build step to delete files
  matching a pattern


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


#### `jenkins_saml_keystore_path` string

Path to the Java Key Store file containing the SAML2 key and certificate for the
SAML plugin.


#### `jenkins_tls_cert` string required

File content for the TLS/SSL certificate to serve for your Jenkins instance.


#### `jenkins_tls_key` string required

File content for the TLS/SSL key to serve for your Jenkins instance.


#### `jenkins_url` string

The public URL where Jenkins will be available.


## Configuring Jenkins

While our goal is to configure production-ready Jenkins out of the box, there
are some steps that need to be configured manually after you deploy your
instance.


### Keeping Jenkins up to date

Jenkins is pulled from the Jenkins repos for your distro (currently we only
support Ubuntu). As long as your OS is configured to update automatically,
you'll always pull in the latest version of Jenkins. For Debian/Ubuntu, install
[unattended-upgrades](https://wiki.debian.org/UnattendedUpgrades).


### SAML2 authentication

_TODO_


### Email notifications

_TODO_


### Setup a project with blue ocean

_TODO_


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

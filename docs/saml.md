# SAML authentication

For SP Id urn:gov:gsa:SAML:2.0.profiles:sp:sso:gsa:ci_jenkins_sandbox


Generate two passwords, one for the key password, the other for the store
password. These will be used in the key generation tool below as well as
entered in the UI.

    $ keystorepass=$(pwgen -s 32 1)
    $ privatekeypass=$(pwgen -s 32 1)

Run the keytool with the passwords you just generated. Here, we use the jenkins
docker image to run keytool and write the keystore to `saml-key.jks`.

```
docker pull jenkins
docker run --rm -it -v $(pwd):/app -w /app jenkins bash -c "\$JAVA_HOME/bin/keytool -genkeypair -alias saml-key -keypass $privatekeypass -keystore saml-key.jks -storepass $keystorepass -keyalg RSA -keysize 4096 -validity 3650"
```

## Login.gov configuration

https://dashboard.int.identitysandbox.gov/service_providers

Show the SAML SP certificate, copy/paste the certificate part into the Login.gov
application configuration.

    $ docker run --rm -it -v $(pwd):/app -w /app jenkins bash -c "\$JAVA_HOME/bin/keytool -list -rfc -keystore saml-key.jks -alias saml-key -storepass $keystorepass"


## Jenkins configuration

Once configured, any user of your IdP will be able to log into Jenkins so it's
important that you control authorization within Jenkins. We recommend using
the role-based authorization strategy to give read/admin access _only_ to
a specific allowed-list of users.


### Role-based authorization strategy

If you're using the role-based authorization strategy, you'll want to add your
admin users _before_ enabling SAML, otherwise you'll be able to login, but won't
be able to change settings.

```yaml
# with configuration-as-code
jenkins:
  authorizationStrategy:
    roleBased:
      roles:
        global:
        - assignments:
          - "your.email@agency.gov"
          name: "admin"
          pattern: ".*"
          permissions:
          - "Job/Move"
          - "Job/Build"
          - "Lockable Resources/View"
          - "Credentials/Delete"
          - "Credentials/ManageDomains"
          - "Lockable Resources/Unlock"
          - "View/Create"
          - "Agent/Configure"
          - "Job/Read"
          - "Credentials/Update"
          - "Agent/Create"
          - "Job/Delete"
          - "Agent/Build"
          - "View/Configure"
          - "Lockable Resources/Reserve"
          - "Agent/Provision"
          - "SCM/Tag"
          - "Job/Create"
          - "Job/Discover"
          - "Credentials/View"
          - "Agent/Connect"
          - "Agent/Delete"
          - "Run/Replay"
          - "Agent/Disconnect"
          - "Run/Delete"
          - "Job/Cancel"
          - "Overall/Read"
          - "Run/Update"
          - "Credentials/Create"
          - "Overall/Administer"
          - "View/Delete"
          - "Job/Configure"
          - "Job/Workspace"
          - "View/Read"
```


### Security Realm

As a Jenkins admin, click [Manage Jenkins -> Configure Global Security](https://ci.sandbox.datagov.us/configureSecurity/).

Under Security Realm, select SAML 2.0. Leave the defaults as is and fill out
only the fields as described below.

- IdP Metadata: Leave this blank.
- IdP Metadata URL: `https://idp.int.identitysandbox.gov/api/saml/metadata2020`
- Refresh period: `1440`

Click Validate IdP Metadata URL. You should see a "Success" message.

- Username Attribute: `email`
- Email attribute: `email`
- Username Case Conversion: `Lowercase`
- Logout URL: `https://idp.int.identitysandbox.gov/api/saml/logout2020`

Enable/select Advanced Configuration.

- SP Entity ID: `urn:gov:gsa:SAML:2.0.profiles:sp:sso:gsa:ci_jenkins_sandbox`

Enable/select Encryption Configuration:

- Keystore path is `/data/jenkins/saml-key.jks`
- Keystore passord was generated earlier (`echo $keystorepass`)
- Private key alias is `saml-key`
- Private key password was generated earlier (`echo $privatekeypass`)

Click "Test keystore". You should see a "Success" message.

Click "Save".

If your IdP requires your SP metadata, it is available at the URL
[/securityRealm/metadata](https://ci.sandbox.datagov.us/securityRealm/metadata).


## Configuration-as-code

Once this configuration is working, you'll want to move it into your
configuration-as-code plugin. It might look like this:

```yaml
jenkins:
  securityRealm:
    saml:
      advancedConfiguration:
        forceAuthn: false
        spEntityId: "urn:gov:gsa:SAML:2.0.profiles:sp:sso:gsa:ci_jenkins_sandbox"
      binding: "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
      displayNameAttributeName: "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"
      emailAttributeName: "email"
      encryptionData:
        forceSignRedirectBindingAuthnRequest: false
        keystorePassword: "{AQAAABAAAAAwsez2FyULLoLGZrjfit7QXVenlnHu0e+Vmt3J/lbYFdIal6K3jr2RCGOiHS0/5SciTZNYVjLKF6wftXabgdF7Bw==}"
        keystorePath: "/data/jenkins/saml-key.jks"
        privateKeyAlias: "saml-key"
        privateKeyPassword: "{AQAAABAAAAAwRxO8IN5TBt36+ePiJ2X5Glb8bLVMDRSLA1/a2y184h4kL7xzsOmD83/qTOhYy4pPXV2hciRp5oUhgGvcVLmeJA==}"
      groupsAttributeName: "http://schemas.xmlsoap.org/claims/Group"
      idpMetadataConfiguration:
        period: 1440
        url: "https://idp.int.identitysandbox.gov/api/saml/metadata2020"
      logoutUrl: "https://idp.int.identitysandbox.gov/api/saml/logout2020"
      maximumAuthenticationLifetime: 86400
      usernameAttributeName: "email"
      usernameCaseConversion: "lowercase"
```

Note that `keystorePassword` and `privateKeyPassword` are base64 encoded and
encrypted with the Jenkins key. If the Jenkins key is lost, the passwords
change, or the keystore cert/key changes, it's probably easier to regenerate
them all and then extract these values from Jenkins.


## Getting locked out

Once SAML2 is enabled your built-in admin user will no longer work and you might
need to tweak the configuration, but won't be able to log in. In that case it
might be easier to fall back to the local Jenkins user database and then fix the
configuration through the Jenkins UI.

```yaml
# with configuration-as-code
jenkins:
  securityRealm:
    local:
      allowsSignup: false
      enableCaptcha: false
```
# SAML authentication

Generate two passwords, one for the key password, the other for the store
password. These will be used in the key generation tool below as well as
entered in the UI.

    $ keypass=$(pwgen -s 32 1)
    $ storepass=$(pwgen -s 32 1)

Run the keytool with the passwords you just generated. Here, we use the jenkins
docker image to run keytool and write the keystore to `/tmp/saml-key.pem`.

```
docker pull jenkins
docker run --rm -it -v $(pwd):/app -w /app jenkins bash -c "\$JAVA_HOME/bin/keytool -genkeypair -alias saml-key -keypass $keypass -keystore saml-key.jks -storepass $storepass -keyalg RSA -keysize 4096 -validity 3650"
docker run --rm -it -v $(pwd):/app -w /app jenkins bash -c "\$JAVA_HOME/bin/keytool -list -rfc -keystore saml-key.jks -alias saml-key -storepass $storepass"
```

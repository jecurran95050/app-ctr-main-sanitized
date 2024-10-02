# Application Central

This repo is a sub-component for Application Central.  For more info, please visit:
SANITIZED

## Main Module Docker Container

- The main module leverages Nginx as both a web server and reverse-proxy.
- The web content is a Flask Application hosted on Port 443.
- Initial SSL certificates are self signed.  These are located in ./vault/global/ and can be swapped with production certs.  Just use the same filenames.
- Path based routing is configured via default.conf which is copied to /etc/nginx/conf.d/default.conf inside of the docker container.
- Auth credentials are confirmed via ldap.
- XXXX credentials are securely cached at ./vault/global/
- Encryption is provided by Fernet.

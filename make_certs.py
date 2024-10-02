from creds.creds import *

__author__ = 'jacurran'


if __name__ == '__main__':
    if not os.path.isdir("outside/vault"):
        os.system("mkdir outside/vault")
        os.system("chmod -R 777 outside/vault")

    if not os.path.isdir("outside/vault/global"):
        os.system("mkdir outside/vault/global")
        os.system("chmod -R 777 outside/vault/global")

    if not os.path.isdir("outside/vault/global/postgres"):
        os.system("mkdir outside/vault/global/postgres")
        os.system("chmod -R 777 outside/vault/global/postgres")

    if not os.path.isdir("outside/vault/global/pgadmin"):
        os.system("mkdir outside/vault/global/pgadmin")
        try:
            os.system("chmod -R 777 outside/vault/global/pgadmin")
        except:
            pass

    if not cert_exists():
        make_cert()

    if not dhpem_exists():
        make_dhpem()
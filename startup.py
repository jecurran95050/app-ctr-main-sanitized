import os

__author__ = 'jacurran'

####################################################################

if __name__ == '__main__':
    os.system('echo "search XXXXX.com" >> /etc/resolv.conf')
    os.system('python3 make_certs.py')
    os.system('redis-server --daemonize yes --protected-mode no')
    os.system('nginx')
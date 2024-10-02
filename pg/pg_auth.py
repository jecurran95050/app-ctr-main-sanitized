import yaml
from cryptography.fernet import Fernet
import psycopg2
import requests
from requests.packages import urllib3
import os

__author__ = 'jacurran'


settings_data = open('settings/settings.yml', 'r')
settings = yaml.full_load(settings_data)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

####################################################################################

def read_pg_pw():
    ESP_cipher_key = b'XXXXX'
    cipher_suite = Fernet(ESP_cipher_key)
    try:
        with open("outside/vault/global/pg_cache") as file:
            raw_content = file.readlines()
        encrypted_pw = [line.strip() for line in raw_content][0]
        unencrypted_pw = cipher_suite.decrypt(encrypted_pw.encode()).decode()
        return unencrypted_pw
    except:
        with open("outside/vault/global/pg_cache", "w+"):
            os.system("chmod -R 777 outside/vault/global/pg_cache")
            return "password"


def write_pg_pw(content):
    ESP_cipher_key = b'XXXXX'
    cipher_suite = Fernet(ESP_cipher_key)
    cipher = cipher_suite.encrypt(content.encode()).decode()
    with open("outside/vault/global/pg_cache", 'w+') as cache:
        os.system("chmod -R 777 outside/vault/global/pg_cache")
        cache.write(cipher)


def read_pg_hash():
    try:
        with open("outside/vault/global/pg_cache") as file:
            raw_content = file.readlines()
        encrypted_pw = [line.strip() for line in raw_content][0]
        return encrypted_pw
    except:
        return str()


def read_pg_pw_rest(url=settings["app_ctr_main"]):
    ESP_cipher_key = b'XXXXX'
    cipher_suite = Fernet(ESP_cipher_key)
    encrypted_pw = requests.get(f"https://{url}/api/pgh", verify=False).text
    unencrypted_pw = cipher_suite.decrypt(encrypted_pw.encode()).decode()
    return unencrypted_pw


def get_pg_pw():
    try:
        return read_pg_pw()
    except:
        try:
            return read_pg_pw_rest(url=settings["app_ctr_main"])
        except:
            return "password"

####################################################################################

def web_first_pg_creds():
    pg_pw = get_pg_pw()
    if pg_pw == "password":
        return True
    else:
        return False


def web_valid_pg_creds():
    pg_pw = get_pg_pw()
    return pg_auth_good(pg_pw=pg_pw)


def pg_auth_good(pg_pw=get_pg_pw(),
              db_name="postgres",
              pg_host=settings["pg_host"],
              pg_port="XXXX"):
    try:
        connection = psycopg2.connect(
            database=db_name,
            user="XXXXX",
            password=pg_pw,
            host=pg_host,
            port=pg_port,
        )
        connection.close()
    except:
        return False
    return True

####################################################################################
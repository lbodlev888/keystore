#!/usr/bin/python3
from custom_keyring import Keyring
import argparse

parser = argparse.ArgumentParser(description='Own keyring manager')
subparsers = parser.add_subparsers(dest='command', required=True)

init_keyring = subparsers.add_parser('init', help='Inits a new empty keyring')
init_keyring.add_argument('gpg_id', type=str, help='GPG id. Can be also the email')

new_credential = subparsers.add_parser('new', help='Adds a new credential')
new_credential.add_argument('--service', '-s', type=str, required=True, help='Name of the service')
new_credential.add_argument('--username', '-u', type=str, required=True, help='Username for the credential')
new_credential.add_argument('--password', '-p', type=str, required=True, help='Password of the credential. It can be anything, from private keys(pgp, ssh) and API keys to regular login passwrods')

remove_credential = subparsers.add_parser('remove', help='Removes an existing credential')
remove_credential.add_argument('--service', '-s', type=str, required=True, help='Service name of the credential provided when created')
remove_credential.add_argument('--username', '-u', type=str, required=True, help='Username of the credential provided when created')

get_credential = subparsers.add_parser('get', help='Returns the password of the credential based on service and username')
get_credential.add_argument('--service', '-s', type=str, required=True, help='Name of the service provided when credential was created')
get_credential.add_argument('--username', '-u', type=str, required=True, help='Username provided when credential was created')

update_credentual = subparsers.add_parser('update', help='Update the password for an existing credential')
update_credentual.add_argument('--service', '-s', type=str, required=True, help='Name of the service provided when credential was created')
update_credentual.add_argument('--username', '-u', type=str, required=True, help='Username provided when credential was created')
update_credentual.add_argument('--new_password', '-p', type=str, required=True, help='Username provided when credential was created')

args = parser.parse_args()
keyring = Keyring()

match args.command:
    case 'init':
        keyring.init_keyring(args.gpg_id)
    case 'new':
        keyring.save_password(args.service, args.username, args.password)
    case 'remove':
        keyring.remove_password(args.service, args.username)
        print('remove')
    case 'update':
        keyring.update_password(args.service, args.username, args.new_password)
    case 'get':
        print(keyring.get_password(args.service, args.username))

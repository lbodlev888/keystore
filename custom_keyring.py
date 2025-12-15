import subprocess
import os
import json

class CredentialMissing(Exception):
    def __init__(self, message = 'Credential doesnt exist') -> None:
        self.message = message
        super().__init__(self.message)

class KeyringMissing(Exception):
    def __init__(self, message = 'Keyring doesnt exist. Init it first') -> None:
        self.message = message
        super().__init__(self.message)

class CredentialAlreadyExists(Exception):
    def __init__(self, message = 'A credential with same service and username was found') -> None:
        self.message = message
        super().__init__(self.message)

class Keyring:
    def __init__(self, keyring_path: str | None = None) -> None:
        home_path = os.path.expanduser('~')
        self.keyring_path = keyring_path if keyring_path else os.path.join(home_path, '.custom_keyring')
        self.data_file = 'data.json'

    def save_password(self, service_name: str, username: str, password: str):
        try:
            with open(f'{self.keyring_path}/{self.data_file}', 'r') as f:
                recipient = json.load(f)['recipient']
        except FileNotFoundError:
            raise KeyringMissing()

        if self.__check_password(service_name, username):
            raise CredentialAlreadyExists()

        outfile = f'{self.keyring_path}/{service_name}_{username}.gpg'
        command = f'echo "{password}" | gpg --encrypt -r {recipient} --out {outfile}'
        subprocess.run(command, shell=True)

    def get_password(self, service_name: str, username: str) -> str | None:
        if not self.__check_password(service_name, username):
            raise CredentialMissing()

        input_file = f'{self.keyring_path}/{service_name}_{username}.gpg'
        command = f'gpg --decrypt {input_file}'
        result = subprocess.run(command, shell=True, capture_output=True)
        if result.returncode != 0:
            return None
        return result.stdout.decode().strip()

    def __check_password(self, service_name: str, username: str) -> bool:
        input_file = f'{self.keyring_path}/{service_name}_{username}.gpg'
        return os.path.exists(input_file)

    def remove_password(self, service_name: str, username: str) -> bool:
        if not self.__check_password(service_name, username):
            raise CredentialMissing()
        input_file = f'{self.keyring_path}/{service_name}_{username}.gpg'
        os.remove(input_file)
        return True

    def update_password(self, service_name: str, username: str, new_password: str) -> bool:
        if not self.__check_password(service_name, username):
            raise CredentialMissing()

        input_file = f'{self.keyring_path}/{service_name}_{username}.gpg'
        os.remove(input_file)
        self.save_password(service_name, username, new_password)
        return True

    def init_keyring(self, recipient: str) -> bool:
        try:
            data = {'recipient': recipient}
            if not os.path.isdir(self.keyring_path):
                os.mkdir(self.keyring_path)
            with open(f'{self.keyring_path}/'+self.data_file, 'w') as f:
                json.dump(data, f)
            return True
        except Exception as e:
            print('Exception occured: ', e)
            return False

    def check_keyring(self) -> bool:
        return os.path.exists(f'{self.keyring_path}/{self.data_file}')

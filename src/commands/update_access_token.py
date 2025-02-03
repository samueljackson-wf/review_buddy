import keyring
from src.commands.command import Command
from src.constants import KEYRING_SERVICE, KEYRING_ACCOUNT


class UpdateAccessToken(Command):

    def apply(self):
        token = input('GitHub personal access token (will be stored in Keychain): ').strip()

        if not token:
            print('Invalid access token')
            exit(1)

        keyring.set_password(KEYRING_SERVICE, KEYRING_ACCOUNT, token)
        return token
"""Convenience function for generating a fernet secret.

Secret is used to encrypt & decrypt data between the Route Policy Server
and the Route Server Agent.
"""

# Third Party
from cryptography.fernet import Fernet

if __name__ == "__main__":
    key = Fernet.generate_key().decode()
    sep = "-" * (63 + len(key))
    print(
        """
{sep}
48 IX Inc.

{sep}

Route Policy Server to Route Server Agent Encryption Key: {k}

{sep}
On the Server, add this to /etc/48ix-routingpolicy/config.yaml:

agent:
  key: '{k}'

{sep}
On the Agent, add this to .bashrc:

export ix_rsagent_secret='{k}'

{sep}
    """.format(
            k=key, sep=sep
        )
    )

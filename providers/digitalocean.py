import os
import pulumi
import pulumi_digitalocean
from cryptography.hazmat.primitives import serialization as crypto_serialization

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
with open(f"{CUR_DIR}/../cloud-init.yaml", "r") as f:
    cloud_init = f.read()


def digitalocean_program(
    key, size="s-2vcpu-4gb", region="sfo2", image="ubuntu-22-04-x64"
):
    def run():
        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.OpenSSH,
            crypto_serialization.NoEncryption(),
        )

        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH,
        )

        ssh_key = pulumi_digitalocean.SshKey(
            "ssh-key",
            public_key=public_key.decode("utf-8"),
        )

        # Create a droplet
        server = pulumi_digitalocean.Droplet(
            "benchmark-instance-digitalocean",
            image=image,
            region=region,
            size=size,
            ssh_keys=[ssh_key.fingerprint],
            user_data=cloud_init,
            opts=pulumi.ResourceOptions(depends_on=[ssh_key]),
        )

        # Export the IP address of the server
        pulumi.export("ip", server.ipv4_address)
        pulumi.export("ssh_key_private", private_key.decode("utf-8"))
        pulumi.export("ssh_key_public", public_key.decode("utf-8"))

    return run

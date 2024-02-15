from base64 import b64encode
import os
import pulumi
import pulumi_linode
from cryptography.hazmat.primitives import serialization as crypto_serialization

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
with open(f"{CUR_DIR}/../cloud-init.yaml", "r") as f:
    cloud_init = f.read()
cloud_init = b64encode(cloud_init.encode("utf-8")).decode("utf-8")


def linode_program(
    key, size="g6-standard-2", region="us-mia", image="linode/ubuntu22.04"
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

        # Create an instance
        server = pulumi_linode.Instance(
            "benchmark-instance-linode",
            image=image,
            region=region,
            type=size,
            private_ip=False,
            authorized_keys=[public_key.decode("utf-8").strip()],
            metadatas=[{"userData": cloud_init}],
            opts=pulumi.ResourceOptions(depends_on=[]),
        )

        # Export the IP address of the server
        pulumi.export("ip", server.ip_address)
        pulumi.export("ssh_key_private", private_key.decode("utf-8"))
        pulumi.export("ssh_key_public", public_key.decode("utf-8"))

    return run

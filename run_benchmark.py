from threading import Thread

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

from providers.digitalocean import digitalocean_program
from providers.hetzner import hetzner_program
from providers.linode import linode_program

from benchmark import setup
from plot import show_plots


def main():
    DATA = {}
    key = rsa.generate_private_key(
        backend=crypto_default_backend(), public_exponent=65537, key_size=2048
    )

    threads = [
        Thread(target=setup, args=(DATA, "digitalocean", digitalocean_program(key))),
        Thread(target=setup, args=(DATA, "hetzner", hetzner_program(key))),
        Thread(target=setup, args=(DATA, "linode", linode_program(key))),
    ]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    show_plots(DATA)


if __name__ == "__main__":
    main()

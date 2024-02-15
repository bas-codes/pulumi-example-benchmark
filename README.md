# pulumi-example-benchmark

Simple Pulumi example to benchmark VPS instances of three cloud providers using [yabs](https://yabs.sh)

- [DigitalOcean](https://bas.surf/digitalocean)
- [Linode](https://bas.surf/linode)
- [Hetzner](https://bas.surf/hetzner)

# Read more

The blog article is available at [bas.codes](https://bas.surf/pulumi-example-benchmark).

# Run it

```bash
export HCLOUD_TOKEN=xxxxxxxxxxxx
export LINODE_TOKEN=xxxxxxxxxxxx
export DIGITALOCEAN_TOKEN="dop_v1_xxxxxxxxxxxx"

export PULUMI_CONFIG_PASSPHRASE=
export PULUMI_CONFIG_PASSPHRASE_FILE=
export PULUMI_ACCESS_TOKEN=

pulumi login --local

python3 -m pip install -r requirements.txt
python3 run_benchmark.py
```
import io
import json
import time
import pulumi
import paramiko


def setup(DATA, provider, pulumi_program):
    workspace = pulumi.automation.LocalWorkspace()
    stack = pulumi.automation.create_or_select_stack(
        stack_name=f"benchmark-{provider}",
        project_name="pulumi-benchmark",
        program=pulumi_program,
    )
    stack.up()
    outputs = stack.outputs()
    ip = outputs.get("ip").value
    ssh_key_private = outputs.get("ssh_key_private").value

    print(">>>>>>>", "stack up done. ")
    time.sleep(30)

    data = None
    try:
        # Run /root/benchmark.sh via ssh
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        pkey = paramiko.RSAKey.from_private_key(io.StringIO(ssh_key_private))
        ssh.connect(ip, username="root", pkey=pkey)
        stdin, stdout, stderr = ssh.exec_command("bash /root/benchmark.sh")
        for line in stdout:
            try:
                data = json.loads(line)
            except:
                print(line.strip())
        stdin.close()
        ssh.close()
        print(">>>>>>>", "benchmark done. ")
    except Exception as e:
        print(">>>>>>>", "benchmark error. ", e)
    finally:
        stack.destroy()
        print(">>>>>>>", "stack destroy done. ")

    DATA[provider] = data
    return data

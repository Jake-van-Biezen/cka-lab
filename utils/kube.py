"""
Utilities for managing Kubernetes clusters using Kind
"""
import subprocess
import sys
import time
from pathlib import Path

import typer


def run_cmd(cmd: list[str]):
    """
    Run a command in the shell and print the output
    """
    typer.echo(f"🔧 Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def create_kind_cluster(name: str):
    """
    Create a Kind cluster with the given name
    """
    run_cmd(["kind", "create", "cluster", "--name", name])
    wait_for_cluster_ready()

def delete_kind_cluster(name: str):
    """
    Delete a Kind cluster with the given name
    """
    run_cmd(["kind", "delete", "cluster", "--name", name])

def apply_scaffold(exercise: str):
    """
    Apply the scaffold for the given exercise
    """
    path = Path("exercises") / exercise / "scaffold.yaml"
    if not path.exists():
        typer.echo(f"❌ No scaffold found for {exercise}")
        return
    run_cmd(["kubectl", "apply", "-f", str(path)])

def wait_for_cluster_ready(namespace="default", timeout=30):
    """
    Wait for the Kind cluster to be ready
    """
    print("⏳ Waiting for cluster to become ready...", end="", flush=True)
    for _ in range(timeout):
        try:
            result = subprocess.run(
                ["kubectl", "get", "sa", "default", "-n", namespace],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            if "default" in result.stdout.decode():
                print(" ✅")
                return True
        except subprocess.CalledProcessError:
            pass
        print(".", end="", flush=True)
        time.sleep(1)
    print(" ❌ Timed out waiting for cluster to be ready.")
    return False

def run_kubectl(cmd):
    """
    Run a kubectl command and return the output
    """
    try:
        result = subprocess.run(
            ["kubectl"] + cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {' '.join(cmd)}:")
        print(e.stderr.decode())
        sys.exit(1)

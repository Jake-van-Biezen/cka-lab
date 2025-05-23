"""
CLI for managing Kubernetes exercises using Kind.
"""

import importlib
import os
import re
import subprocess
from pathlib import Path

import typer

from utils.kube import apply_scaffold, create_kind_cluster, delete_kind_cluster

app = typer.Typer()


@app.command()
def run(exercise: str):
    """
    Spin up a cluster and scaffold an exercise.
    """
    typer.echo(f"🛠️ Starting exercise: {exercise}")
    cluster_name = f"cka-{re.sub('[^A-Za-z0-9]+', '', exercise)}"

    # Check if cluster already exists
    try:
        output = subprocess.check_output(["kind", "get", "clusters"], text=True)
        clusters = output.strip().splitlines()
        if cluster_name in clusters:
            typer.echo(f"⚠️ Cluster '{cluster_name}' already exists. Skipping creation.")
        else:
            create_kind_cluster(cluster_name)
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Failed to list kind clusters: {e}")
        raise typer.Exit(code=1)

    # Apply the scaffold
    apply_scaffold(exercise)

    typer.echo("✅ Cluster and resources ready!")
    info(exercise)


@app.command()
def check(exercise_path: str):
    """
    Check the exercise and tear down the cluster if successful.
    """
    typer.echo(f"✅ Checking {exercise_path}...")
    # Check if the exercise is running
    try:
        output = subprocess.check_output(["kind", "get", "clusters"], text=True)
        clusters = output.strip().splitlines()
        cluster_name = f"cka-{re.sub('[^A-Za-z0-9]+', '', exercise_path)}"
        if cluster_name in clusters:
            pass
        else:
            typer.echo(f"❌ Exercise '{exercise_path}' is not running.")
            raise typer.Exit(code=1)
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Failed to list kind clusters: {e}")
        raise typer.Exit(code=1)

    exercise_mod = exercise_path.replace("/", ".")
    try:
        check_module = importlib.import_module(f"exercises.{exercise_mod}.check")
        if hasattr(check_module, "check"):
            check_succesful = check_module.check()
            if check_succesful:
                if typer.confirm(
                    "🎉 Check successful! Do you want to tear down the cluster?"
                ):
                    cluster_name = f"cka-{re.sub('[^A-Za-z0-9]+', '', exercise_path)}"
                    typer.echo(f"🧹 Tearing down cluster '{cluster_name}'...")
                    try:
                        subprocess.run(
                            ["kind", "delete", "cluster", "--name", cluster_name],
                            check=True,
                        )
                        typer.echo("✅ Cluster deleted.")
                    except subprocess.CalledProcessError as e:
                        typer.echo(f"❌ Failed to delete cluster: {e}")
                        raise typer.Exit(code=1)
        else:
            typer.echo("❌ No 'check()' function found.")
    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def list_exercises():
    """
    List all available exercises.
    """
    base_dir = "exercises"
    if not os.path.isdir(base_dir):
        typer.echo("❌ No exercises found.")
        raise typer.Exit()

    typer.echo("📚 Available exercises:\n")

    for root, dirs, _ in os.walk(base_dir):
        for d in dirs:
            full_path = os.path.join(root, d)
            check_path = os.path.join(full_path, "check.py")
            if os.path.exists(check_path):
                relative_path = os.path.relpath(full_path, base_dir)
                typer.echo(f"• {relative_path.replace(os.sep, '/')}")


@app.command()
def info(exercise_path: str):
    """
    Show information about the given exercise.
    """
    readme_path = Path(f"exercises/{exercise_path}/README.md")
    if not readme_path.exists():
        typer.echo("No README found.")
        raise typer.Exit()
    typer.echo(readme_path.read_text(encoding="utf-8"))


@app.command()
def cleanup(exercise: str):
    """
    Teardown the cluster for the given exercise.
    """
    cluster_name = f"cka-{re.sub('[^A-Za-z0-9]+', '', exercise)}"
    delete_kind_cluster(cluster_name)
    typer.echo("🧹 Cleaned up.")


if __name__ == "__main__":
    app()

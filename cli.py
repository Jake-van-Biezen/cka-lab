import typer
from utils.kube import apply_scaffold, create_kind_cluster, delete_kind_cluster

app = typer.Typer()

@app.command()
def run(exercise: str):
    """
    Spin up a cluster and scaffold an exercise.
    """
    typer.echo(f"🛠️ Starting exercise: {exercise}")
    cluster_name = f"cka-{exercise}"

    create_kind_cluster(cluster_name)
    apply_scaffold(exercise)
    typer.echo("✅ Cluster and resources ready!")

@app.command()
def cleanup(exercise: str):
    """
    Teardown the cluster for the given exercise.
    """
    cluster_name = f"cka-{exercise}"
    delete_kind_cluster(cluster_name)
    typer.echo("🧹 Cleaned up.")

if __name__ == "__main__":
    app()

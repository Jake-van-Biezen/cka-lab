# 🧪 cka-lab

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

**cka-lab** is a CLI tool for creating and testing hands-on Kubernetes exercises, designed to help you (or your students) prepare for the [Certified Kubernetes Administrator (CKA)](https://www.cncf.io/certification/cka/) exam.

Each exercise spins up a **fresh Kubernetes cluster**, applies predefined **scaffolded resources**, and can run **automated checks** to verify correctness — all from the command line.---

## 🚀 Features

- 🌀 Launches a new Kubernetes cluster per exercise (using [KinD](https://kind.sigs.k8s.io/))
- 📦 Scaffolds pods, services, namespaces, and more
- ✅ Optional validation scripts for verifying CKA-style configurations
- 🧹 Clean teardown and repeatable learning flow
- 💻 Built with [Typer](https://typer.tiangolo.com/) for a great CLI experience

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/jake-van-biezen/cka-lab.git
cd cka-lab

# Create a virtual environment
env activate

# Install dependencies
poetry install --no-root
```

---

## 🚀 Usage

Make sure you have Docker and kind installed.

Once the CLI is installed or cloned locally, you can run the following commands:

📚 List All Available Exercises

Get a list of all available exercises, organized by domain:

```python
poetry run python cli.py list-exercises
```

🏁 Run an Exercise  
Spin up a fresh Kubernetes cluster using kind and scaffold the resources for a specific exercise:

```python
poetry run python cli.py run troubleshooting/1
```

✅ Check an Exercise

Run the check logic to verify if you've successfully completed the exercise:

```python
poetry run python cli.py check troubleshooting/1
```

If the check passes, you’ll be asked whether you want to delete the cluster.

ℹ️ View Exercise Info

Display the README for an exercise (if present):

```python
python cli.py info troubleshooting/1
```

🧹 Manually Cleanup

Tear down the cluster for a specific exercise:

```python
python cli.py cleanup troubleshooting/1
```

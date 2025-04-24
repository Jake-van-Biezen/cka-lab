# 🧪 cka-lab

**cka-lab** is a CLI tool for creating and testing hands-on Kubernetes exercises, designed to help you (or your students) prepare for the [Certified Kubernetes Administrator (CKA)](https://www.cncf.io/certification/cka/) exam.

Each exercise spins up a **fresh Kubernetes cluster**, applies predefined **scaffolded resources**, and can run **automated checks** to verify correctness — all from the command line.

---

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
git clone https://github.com/YOUR-USERNAME/cka-lab.git
cd cka-lab

# (Optional) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

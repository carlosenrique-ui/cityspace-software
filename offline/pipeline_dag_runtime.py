# ==========================================================
# IPT-CitySpace – Executable Pipeline DAG
# ==========================================================

from pathlib import Path
import subprocess


PIPELINE_DIR = Path("offline/pipeline")


def load_pipeline():

    steps = sorted(PIPELINE_DIR.glob("*.py"))

    pipeline = []

    for step in steps:

        module = step.with_suffix("").as_posix().replace("/", ".")

        pipeline.append({
            "name": step.name,
            "module": module
        })

    return pipeline


def run_pipeline():

    pipeline = load_pipeline()

    print("\n===================================")
    print(" IPT-CitySpace DAG EXECUTION ")
    print("===================================\n")

    for step in pipeline:

        print(f"\nRunning step: {step['name']}\n")

        subprocess.run(
            ["python", "-m", step["module"]],
            check=True
        )

    print("\nPipeline finished.\n")


if __name__ == "__main__":

    run_pipeline()
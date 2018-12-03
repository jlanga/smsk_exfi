# pylint: disable=syntax-error

import pandas as pd
import yaml

from snakemake.utils import min_version
min_version("5.3")

shell.prefix("set -euo pipefail;")

params = yaml.load(open("params.yml", "r"))
features = yaml.load(open("features.yml", "r"))
samples = pd.read_table("samples.tsv")

singularity: "docker://continuumio/miniconda3:4.4.10"

# Define cross-script variables
SAMPLES_PE = (
    smaples["samples"]

MAX_THREADS = params["max_threads"]

# Import ubworkflows
snakefiles = "src/snakefiles/"
include: snakefiles + "folders.py"
include: snakefiles + "clean.py"
include: snakefiles + "raw.py"
# include: snakefiles + "qc.py"
# include: snakefiles + "exfi.py"

rule all:
    """
    Execute the entire pipeline
    """
    input:
        # raw
        expand(
            RAW + "{sample}_{end}.fq.gz",
            sample = SAMPLES_PE,
            end = "1 2".split()
        )

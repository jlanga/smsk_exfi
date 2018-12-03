rule index_fasta:
    """Index a .fasta"""
    input: "{filename}"
    output: "{filename}.fai"
    conda: "generic.yml"
    shell: "samtools faidx {input}"

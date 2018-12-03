def get_reads(wildcards):
    sample = wildcards.sample
    forward, reverse = (
        samples
        [(samples["sample"] == sample)]
        [["forward", "reverse"]]
        .values
        .tolist()[0]
    )
    return forward, reverse


rule raw_link_pe_sample:
    input:
        get_reads
    output:
        forward = RAW + "{sample}_1.fq.gz",
        reverse = RAW + "{sample}_2.fq.gz"
    log:
        RAW + "link_dna_pe_{sample}.log"
    benchmark:
        RAW + "link_dna_pe_{sample}.json"
    shell:
        "ln "
            "--symbolic "
            "$(readlink --canonicalize {input[0]}) "
            "{output.forward} 2> {log}; "
        "ln "
            "--symbolic "
            "$(readlink --canonicalize {input[0]}) "
            "{output.reverse} 2>> {log}"



rule raw_link_assembly:
    input:
        fasta = features["assembly"]
    output:
        fasta = RAW + "assembly.fa"
    log:
        RAW + "link_assembly.log"
    benchmark:
        RAW + "link_assembly.json"
    shell:
        "ln "
            "--symbolic "
            "$(readlink --canonicalize {input.fasta}) "
            "{output.fasta} 2> {log}"

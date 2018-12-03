def get_adaptor(wildcards):
    sample = wildcards.sample
    adaptor = (
        samples
        [(samples["sample"] == sample)]
        ["adaptor"]
        .values
        .tolist()
        [0]
    )
    return adaptor


def get_phred(wildcards):
    sample = wildcards.sample
    phred = (
        samples
        [(samples["sample"] == sample)]
        ["phred"]
        .values
        .tolist()
        [0]
    )
    return phred


def get_trimmomatic_params(wildcards):
    # The YAML file introduces a \n
    return params["trimmomatic"]["extra"].strip()


rule qc_trimmomatic:
    """Run trimmomatic on paired end mode

    to eliminate Illumina adaptors andremove low quality regions and reads.

    Inputs _1 and _2 are piped through gzip/pigz.
    Outputs _1 and _2 are piped to gzip/pigz (level 9).
    Outputs _3 and _4 are compressed with the builtin compressor from
    Trimmomatic.

    Further on they are catted and compressed with gzip/pigz (level 1).
    Sequences will be stored permanently later on on CRAM
    """
    input:
        forward = RAW + "{sample}_1.fq.gz",
        reverse = RAW + "{sample}_2.fq.gz"
    output:
        forward = QC + "{sample}_1.fq.gz",
        reverse = QC + "{sample}_2.fq.gz",
        forward_unp = QC + "{sample}_3.fq.gz",
        reverse_unp = QC + "{sample}_4.fq.gz"
    params:
        adaptor = get_adaptor,
        phred = get_phred,
        trimmomatic_params = get_trimmomatic_params
    log:
        QC + "{sample}.trimmomatic_pe.log"
    benchmark:
        QC + "{sample}.trimmomatic_pe.json"
    threads:
        MAX_THREADS
    priority:
        50  # Do this and later the mappings
    conda:
        "qc.yml"
    shell:
        """
        trimmomatic PE \
            -threads {threads} \
            -{params.phred} \
            <(gzip --decompress --stdout {input.forward}) \
            <(gzip --decompress --stdout {input.reverse}) \
            >(pigz --best > {output.forward}) \
            >(pigz --best > {output.forward_unp}) \
            >(pigz --best > {output.reverse}) \
            >(pigz --best > {output.reverse_unp}) \
            ILLUMINACLIP:{params.adaptor}:2:30:10 \
            {params.trimmomatic_params} \
        2> {log} 1>&2
        """

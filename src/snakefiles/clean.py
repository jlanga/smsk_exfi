rule clean:
    """Delete everything"""
    shell:
        "rm -rf {RAW} {QC} {EXFI}"

import logging
import subprocess

def run(*args, **kwargs):
    """Runs a command in a shell and logs stdout and stderr"""
    result = subprocess.run(*args, **kwargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logging.info(result.stdout)
    logging.info(result.stderr)
    return result
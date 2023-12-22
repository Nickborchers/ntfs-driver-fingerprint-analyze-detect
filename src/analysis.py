import subprocess

def istat(image, filename):
    """Execute the istat command in a shell on the 'filename' file in the 'image' disk image"""
    cmd = ["ifind", image, "-n", filename]
    inode = subprocess.check_output(cmd).decode('utf-8').replace("\n", "").replace("'", "")
    return subprocess.check_output(["istat", image, inode])

def baseline_to_file(name, filename, snapshot_dir):
    """Extract metadata from a baseline disk image and write the result to a file"""
    baseline_artefact = istat(snapshot_dir + "/baseline-{name}.bin".format(name=name), filename)
    result = "baseline-{name}-istat-output.txt".format(name=name)
    write_to_file(result, baseline_artefact.decode("utf-8"))
    return result

def experiment_to_file(name, filename, snapshot_dir):
    """Extract metadata from an experiment disk image and write the result to a file"""
    experiment_artefact = istat(snapshot_dir + "/experiment-{name}.bin".format(name=name), filename)
    result = "experiment-{name}-istat-output.txt".format(name=name) 
    write_to_file(result, experiment_artefact.decode("utf-8"))
    return result

def diff(file_a, file_b):
    """Execute the 'diff' command in a shell and print stderr and stdout"""
    result = subprocess.run(["diff", file_a, file_b])
    print(result.stdout)
    print(result.stderr)

def write_to_file(name : str, content : str):
    """Helper function to open a file handle, write to it, and close it."""
    handle = open(name, "w")
    handle.write(content)
    handle.close()
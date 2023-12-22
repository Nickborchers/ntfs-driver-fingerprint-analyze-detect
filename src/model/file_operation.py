class FileOperation:
    """Domain object representing a file operation"""
    def __init__(self, action, baseline, experiment, baseline_filename, experiment_filename):
        """_summary_

        Args:
            action (_type_): the type of operation
            baseline (_type_): the command to establish the baseline
            experiment (_type_): the command that is the experiment
            baseline_filename (_type_): the filename to analyze as a result of the baseline operation
            experiment_filename (_type_): the filename to analyze as a result of the experiment operation
        """
        assert action != None
        self.action = action
        self.baseline = baseline
        self.experiment = experiment
        self.baseline_filename = baseline_filename
        self.experiment_filename = experiment_filename
import os

class Config:
    """Centralized configuration for the Specc utility."""
    def __init__(self):
        # Default file paths
        self.output_file = "system_report.json"
        self.log_file = "system_errors.log"
        
        # Execution constraints
        self.max_retries = 3
        self.sampling_interval = 1.0  # Seconds between sensor polls
import sys
sys.path.append("../")

import yaml

def load_config(config_path: str = r"C:\Users\mksgh\OneDrive - Vestas Wind Systems A S\Documents\Github\TradingBot-agentic-langchain\config\config.yaml" ) -> dict:
    """
    Loads the YAML configuration file from the specified path.

    Parameters
    ----------
    config_path : str, optional
        The path to the YAML configuration file. 

    Returns
    -------
    dict
        The loaded configuration as a dictionary.
    """
    with open(config_path, "r") as file:
        config: dict = yaml.safe_load(file)
    return config
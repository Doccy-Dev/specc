from setuptools import setup, find_packages

setup(
    name='specc',
    version='0.1.2',
    # 'packages' tells setuptools which directories to bundle.
    # We use ['src'] because our logic lives in the src/ folder.
    packages=['src'],
    
    # External dependencies required for the tool to function.
    # psutil: Cross-platform hardware/system telemetry.
    # jsonschema: For validating the generated report structure.
    install_requires=[
        'psutil>=5.9.0',
        'jsonschema>=4.1.0',
        'rich>=12.0.0' #needed for console output
    ],
    
    # Entry Points create the actual CLI command.
    # This maps the terminal command 'specc' to the main() function
    # located in src/main.py.
    entry_points={
        'console_scripts': [
            'specc = src.main:main'
        ]
    },
    
    # Metadata for the package index
    author="Zach",
    description="A lightweight system hardware and thermal profiler for Ubuntu.",
    python_requires='>=3.10', # Targeted specifically for Ubuntu 22.04 LTS
)
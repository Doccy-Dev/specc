import os
from setuptools import setup, find_packages

setup(
    name='specc',
    version='0.1.3',
    # 'packages' tells setuptools which directories to bundle.
    # We use ['src'] because our logic lives in the src/ folder.
    packages=find_packages(where='src'), # This will find all packages in the src/ directory, including subpackages.
    # 'install_requires' lists the external dependencies required for the tool to function.
    
    # External dependencies required for the tool to function.
    # psutil: Cross-platform hardware/system telemetry.
    # jsonschema: For validating the generated report structure.
    install_requires=[
        'psutil>=5.9.0',
        'jsonschema>=4.1.0',
        'rich>=12.0.0', #needed for console output
        'wmi>=1.5.1; sys_platform=="win32"', # Windows-specific dependency for hardware info
        'pywin32>=306; sys_platform=="win32"', # Windows-specific dependency for WMI support
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
    description="A lightweight cross-platform system hardware and thermal profiler.",
    long_description=open('README.md', encoding='utf-8').read() if os.path.exists('README.md') else '', # Safeguard against missing README.md but for my repo this should always be there.
    long_description_content_type='text/markdown', # This tells package indexes that our long description is in Markdown format.
    python_requires='>=3.10', # Targeted specifically for Ubuntu 22.04 LTS
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
)
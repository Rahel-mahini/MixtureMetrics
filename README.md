
# MixtureMetrics: Mixture Descriptors Calculator
This Python project calculates an additive scheme for mixture descriptors of multi-component materials. The algorithm processes input from two `.csv` files and computes various mixture descriptors.


## Overview
The algorithm requires two input files:

1. Descriptors File: Contains individual descriptors for each component.
2. Mole Fraction File: Contains mole fraction values for each component in each mixture.
The main function, mixture_descriptors_to_csv, processes these inputs and generates 12 CSV files, each corresponding to a different mixture descriptor metric. 


## Getting Started

### Prerequisites

Ensure you have Python 3.x installed. You will also need `pip` to install the package.

### Installation
You can install the package in two different ways depending on whether you want to install from the local directory or directly from PyPI:

Option 1: Install from Local Directory
   1. **Download the Package:**
      - Clone the repository or download the ZIP file from GitHub.
      - Extract the contents of the ZIP file.

   2. **Install the Package:**
      - Open a command-line interface (CLI).
      - Navigate to the directory containing the extracted package files.
      - Run the following command to install the package:

      ```bash
      pip install .
      ```
Option 2: Install from PyPI

If you prefer to install the package directly from PyPI, you can use the following command. 

   ```bash
   pip install MixtureMetrics
   ```

## Usage

After installing the package, you can use it in your Python code. Here’s a basic example of how to use the main function:


```python
from MixtureMetrics import mixture_descriptors_to_csv

# Define file paths
descriptors_file_path = 'path/to/descriptors.csv'
mole_fraction_file_path = 'path/to/mole_fraction.csv'
output_directory = 'path/to/output_directory'  # if output path string is empty or None and not provided,it defaults to use the current working directory and if the provided folder is not existed it creates a folder in the given path or in 1.1.5 working directory

# Call the function
mixture_descriptors_to_csv(descriptors_file_path, mole_fraction_file_path, output_directory)
```

## Arguments
- **descriptors_file_path**: Path to the `.csv` file containing individual descriptors for each component.
  
- **mole_fraction_file_path**: Path to the `.csv` file containing mole fraction values for each component in each mixture.
  
- **output_directory**: Directory where the 12 output `.csv` files will be saved.

### Output

The code computes and saves 12 different mixture descriptors, each in its own `.csv` file within the specified output directory.


## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.
   
## License
This project is licensed under the GNU General Public License - see the LICENSE file for details.



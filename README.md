# emo-bon-data-validation
Pydantic validators for the emo-bon sampling log-sheets

## Overview

The `emo-bon-data-validation` project is designed to validate sampling log-sheets for the EMO-BON (Ecological Marine Observatory - Biodiversity Observation Network) project. This project leverages Pydantic, a data validation and settings management library, to ensure the integrity and consistency of the data collected from various observatories.

## Features

- **Data Validation**: Validate log-sheets for water column and soft sediment sampling.
- **Error Logging**: Log validation errors for further analysis.
- **Jupyter Notebooks**: Interactive notebooks for metadata validation and data analysis.

## Project Structure

- `src/validation_classes`: Contains validation logic for different types of log-sheets.
- `validated-data/`: Directory for storing validated data files.
    - `governance/`: Governance data.
    - `logsheets/`: Validated sampling and measured logsheets (lax validation) from GoogleSheets.
    - `logsheets_github/`: Validated sampling and measured logsheets from Github after QC.
    - `logsheets_strict_semistrict`: Validated sampling and measured logsheets (strict and semi-strict validation) from GoogleSheets.
    - `observatories`: The combined validated sampling and measured sheets for each observatory.
- `notebooks/`: Jupyter Notebooks for interactive data validation and analysis.
- `logs/`: Directory for log files, including validation error logs.
- `tests/`: Unit tests for validation functions.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Poetry for dependency management

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/emo-bon-data-validation.git
    cd emo-bon-data-validation
    ```

2. Install dependencies:
    ```sh
    poetry install
    ```

### Usage

1. Explore the Jupyter Notebooks for interactive validation:
    ```sh
    poetry run jupyter notebook notebooks/
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
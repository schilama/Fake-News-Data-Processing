# Fake News Data Processing

This repo is for converting the FNC-1 dataset into a format suitable for the model implemented in https://github.com/schilama/Fake-News

1. Clone the fnc-1 dataset from https://github.com/FakeNewsChallenge/fnc-1  

2. Update path variables in `00_read_data.py` and run the script.  

3. Download the Stanford CoreNLP parser and extract it. 

4. Update paths in `01_parse_data.py` and run the script. To parallelize, pass in non overlapping start and end ranges within 0 and 2600 and run the script multiple times.  

5. Create the dataset by running `02_create_dataset.py`. Modify paths as needed.  

6. Convert data into a suitable format by running `03_format_data.py`.

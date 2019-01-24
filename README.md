# Prepare Fake News Challenge dataset for training the model described in https://github.com/schilama/Fake-News

## Step 1  
Clone the fnc-1 dataset from https://github.com/FakeNewsChallenge/fnc-1

## Step 2  
Update path variables in `00_read_data.py` and run the script.

## Step 3
Download the Stanford CoreNLP parser and extract it. 

## Step 4
Update paths in `01_parse_data.py` and run the script. Pass in non overlapping start and end ranges within 0 and 2600 to parallelize.

## Step 5
Create the dataset by running `02_create_dataset.py`. Modify paths as needed.

## Step 6
Convert data into a suitable format for the model by running `03_format_data.py`.


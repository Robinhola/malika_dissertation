# Malika dissertation

The trial RT file contains the raw data of various participants' reaction times on each experimental trial. Participants are distinguished based on their participant ID. There are 36 participants in total. For each participant we need to obtain average reaction times for the 8 conditions, varying in congruency, social-ness and block. The WhatsApp image outlines the exact nature of these 8 conditions. Only the 'correct' trials (coded as '1' in the excel) should be included in these averages. Additionally, half the participants first completed the social trials followed by the non-social trials whilst the other half did it in reverse order. This is also an important distinction. This summary data then needs to be formatted into the Block data excel, which will allow us to export the results into SPSS to run relevant analyses.

## Installation
```sh
./installation.sh
```

## How to run
```
python ./malika.py && cp a.out a.csv && open a.csv
```
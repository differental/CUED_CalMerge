# CUED_CalMerge

A small Python script that helps CUED students (IA/IB) download and combine lab and lecture calendars, removing useless information and rearranging properties, and filtering lectures according to the students' will.

## Running the script

Clone the repo / download zip & unzip

```bash
git clone https://github.com/differental/CUED_CalMerge.git
cd CUED_CalMerge
pip install -r requirements.txt
python main.py
```

## Expected output

`lecture.ics`: Optimised and filtered lecture calendar file;

if Lab Group Number is not set to 0 (skip):
    `lab.ics`: Optimised and filtered lab calendar file;
    `combined.ics`: Combination of lecture and lab calendars, optimised and filtered.

To import the generated `ics` files to your own calendar, simply open them, or go to Google Calendar / Outlook Calendar / iCloud and import them.

## Configuration

| Option           | Description                                                                                                                                     | Default Value                                  |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Academic Year    | The year of which this academic year started. E.g., 2023 for academic year 2023-24                                                              | Current academic year according to system time |
| Year Group       | The year group the student is in. `IA` or `IB`                                                                                                  | N/A                                            |
| Term             | The term the student is in. `Michaelmas`, `Lent` or `Easter`                                                                                    | N/A                                            |
| Lab Group Number | The lab group number of the student, or 0 to skip all lab events                                                                                | `0`                                            |
| Lecture Clean    | Whether to clean names of all lecture events and put locations into a separate property                                                         | `True`                                         |
| Lab Clean        | Whether to clean names and locations of all lab events                                                                                          | `True`                                         |
| Lecture Keep     | What lecture events to keep. `3` for everything, `2` for everything except coursework & workshops, `1` for all lectures that require attendance | `2`                                            |

# CUED_CalMerge

A small Python script that helps CUED students (IA/IB) download and combine lab and lecture calendars, removing useless information and rearranging properties, and filtering lectures according to the students' will.

## Installation

```bash
git clone https://github.com/differental/CUED_CalMerge.git
cd CUED_CalMerge
pip install -r requirements.txt
```

## Running the script

```
usage: main.py [-h] [-l] [-b] [-c CONFIG]

This tool helps you deal with CUED Calendars. Please refer to README.md for
configuration guides.

options:
  -h, --help            show this help message and exit
  -l, --skip-lecture    Skip Lectures (default: False)
  -b, --skip-lab        Skip Lab (default: False)
  -c CONFIG, --config CONFIG
                        Use Configuration file (default: None)
```

Examples:

- `python main.py -h`: Display the help message above
- `python main.py -l`: Skip Lectures, and enter commandline configuration
- `python main.py -c config.ini`: Use `config.ini` as configuration file and skip commandline configuration
- `python main.py -l -c config.ini`: Use `config.ini` as configuration file, skip commandline configuration, and skip lectures
- `python main.py -l -b`: Bro stop messing around please

## Expected output

- `lecture.ics`: Optimised and filtered lecture calendar file, if enabled;
- `lab.ics`: Optimised and filtered lab calendar file, if enabled;
- `combined.ics`: Combination of lecture and lab calendars, optimised and filtered, if both lecture and lab are enabled.

To import the generated `ics` files to your own calendar, simply open them, or go to Google Calendar / Outlook Calendar / iCloud and import them.

## Configuration file

You can either choose to use the configuration file with `-c /path/to/config` or use console configuration when `-c` is not specified.

See `config.ini` for a sample configuration file including comments.

## Console configuration

| Option           | Description                                                                                                                                     | Default Value                                  |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Academic Year    | The year of which this academic year started. E.g., 2023 for academic year 2023-24                                                              | Current academic year according to system time |
| Year Group       | The year group the student is in. `IA` or `IB`                                                                                                  | N/A                                            |
| Term             | The term the student is in. `Michaelmas`, `Lent` or `Easter`                                                                                    | N/A                                            |
| Lab Group Number | The lab group number of the student, or 0 to skip all lab events                                                                                | `0`                                            |
| Lecture Clean    | Whether to clean names of all lecture events and put locations into a separate property                                                         | `True`                                         |
| Lab Clean        | Whether to clean names and locations of all lab events                                                                                          | `True`                                         |
| Lecture Keep     | What lecture events to keep. `3` for everything, `2` for everything except coursework & workshops, `1` for all lectures that require attendance | `2`                                            |

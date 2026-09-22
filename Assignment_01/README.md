# Assignment 1: Student Support Rule Engine

## Program Description
This is a modular, command-line rule engine that collects student performance data (attendance, assignment averages, and missed submissions), validates the inputs, and assigns a support-priority category along with an actionable advisory message.

## Support-Priority Rules
1. **High priority**: Attendance is below 60% OR missed submissions are 4 or more.
2. **Moderate priority**: Attendance is below 75% OR assignment average is below 60% OR missed submissions are 2 or more.
3. **Routine monitoring**: Applies if no previous conditions are met.

## Included Files
* `support_engine.py`: The main Python script containing the logic for input validation, rule classification, and output formatting.
* `test_support_engine.py`: The test suite containing assertion checks to verify normal and boundary cases for the rule engine.
* `README.md`: Documentation outlining project details, execution instructions, and limitations.

## Run Commands
To run the main program from the repository root:
`uv run python Assignment_01/support_engine.py`

To run the automated tests from the repository root:
`uv run python Assignment_01/test_support_engine.py`

## Known Limitations
1. The rule conditions are hardcoded into the classification function and cannot be dynamically adjusted by the user without altering the source code.
2. The application uses a simple command-line interface with no persistent database, meaning all entered student data is lost once the program terminates.
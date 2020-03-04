# Porting Process

These scripts in `asset_generation` convert the available Excel document of GI categories into json objects, which are then converted into rules formatted for a spaCy Matcher object.

## Why are some categories incomplete?

The import script as it stands handles easy cases first: for most terms in the General Inquirer, we can match a term and POS tag to generate a matcher rule directly from the excel file. These are about 90% of the rules. The other 10 percent are multi-term idioms or more complex phrases where rules will likely have to be written manually.
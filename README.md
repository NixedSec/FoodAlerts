# FoodAlerts
Search FSA Food Alert API


Search for food recalls using the FSA API.

These are UK food product recalls from January 2018 onwards.


### How can I search?

You can:
* search for all recalls from a specific date.
* search for a specific phrase.
* combine both of these.
* search for all recalls from the previous year.
* search for all recalls from the 1st of the previous month.


#### Examples

* FoodAlerts.py -f 2022-02-10
* FoodAlerts.py -s peanuts
* FoodAlerts.py -c 2018-06-27 salmonella
* FoodAlerts.py -y
* FoodAlerts.py -m


#### What can I find?

This should tell you:
* the date of recall
* a description of why
* the reason why
* products being recalled


#### Where is this data from?
The data is from the Food Standards Agency API, the documentation to which is: https://data.food.gov.uk/food-alerts/ui/reference
The alerts provided by the API should be Allergy Alerts (AA), Product Recall Information Notices (PRIN) and Food Alerts for Action (FAFA).
This API being used is a beta release and may change.


#### Is this data accurate?
The script attempts to display information from the API. Bugs or changes to the API may lead to missed alerts. For the most accurate results: the documentation above should be consulted to look up the data directly.

NLDR Reporter

The nldr_reporter script performs a search on the repository and then reports the results in tab-delimted form. Both the search and the columns in the report are configured in a properties file.

To generate a report, execute the nldr_reporter script and include the properties file path, e.g., 
	% nldr_reporter -p my.properties

The most important properties are:
- baseUrl - the web service endpoint
- q - the query parameter (e.g., allrecords:true)
- report.file.path - the path to which the report is written as tab-delimited file. This property can be relative (to directory in which the script is executed) or absolute.
- report.columns - the columns to be displayed in the report. Each of the columns must match a pre-defined attribute of the reporter.

See sample.properties - a self-documented properties file containing all properties and an example of building a complex query.

Note: to see what columns are available to display, add a '-c' flag to the command line for nldr_reporter, e.g.,
	% nldr_reporter -p my.properties -c







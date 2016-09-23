from log_file import LogFileEntry

food = '128.117.126.140 - - [14/Sep/2011:11:14:32 -0600] "GET /scripts/pull/ed_standards.php?server=&purl[]=http%3A%2F%2Fpurl.org%2FASN%2Fresources%2FS103E246&purl[]=http%3A%2F%2Fpurl.org%2FASN%2Fresources%2FS103E24C&purl[]=http%3A%2F%2Fpurl.org%2FASN%2Fresources%2FS103E251 HTTP/1.1" 500 - "http://www.nsdldev.org/search/results?q=ocean&submitButton=Search&n=10" "Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2'
foo = '128.117.126.140 - - [14/Sep/2011:11:14:32 -0600] "GET /scripts/pull/ed_standards.php?server=&purl HTTP/1.1" 500 - "http://www.nsdldev.org/search/results?q=ocean&submitButton=Search&n=10" "Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2'
entry = LogFileEntry (food)

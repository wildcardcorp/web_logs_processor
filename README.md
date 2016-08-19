# web_logs_processor
Process CDN logs such as Cloudflare via API and output to Common Log format do some quick counts on requests and other features using Enterprise Log Share and the REST API.

Please know email address, api key and Zone from Cloudflare to pass on the command line.

Features are:
-Top Country Counts
-Process Starting X minutes ago
-process between epochs
-Top X URLs
-TOP X IP's
-TOP Results
-Lookup Rayid
-Output to Stdout of Common Log Format
-Push the results to Graylog2 GELF input endpoint

PUSH results to graylog server using epoch tracking file:
python process_logs.py -e EMAIL@ADDRESSHERE -k APIKEYHERE -z ZONEIDHERE --pushgraylog 1 --epochfile 1

Get top ip counts:
python process_logs.py -e EMAIL@ADDRESSHERE -k APIKEYHERE -z ZONEIDHERE --minsago 60 --showips 1

Get ray id json log info:
python process_logs.py -e EMAIL@ADDRESSHERE -k APIKEYHERE -z ZONEIDHERE --ray RAYIDFROMREQUESTHEADER

Just output some common_logs to STDOUT so i can process elsewhere:
python process_logs.py -e EMAIL@ADDRESSHERE -k APIKEYHERE -z ZONEIDHERE  --commonlogs 1


Contact us at info@wildcardcorp.com for futher information or access to simliar scripts that are long running, multiprocessing/multithreaded.


www.wildcardcorp.com


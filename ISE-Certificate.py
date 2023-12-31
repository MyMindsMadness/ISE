from ciscoisesdk import IdentityServicesEngineAPI
import json
from datetime import datetime
import time

currentTime = datetime.now().strftime("%Y-%m-%d")

#Credentials/login information for the DevnetSandbox ISE with Ansible
api = IdentityServicesEngineAPI(username='admin',
                                password='C1sco12345',
                                uses_api_gateway=True,
                                base_url='https://10.10.20.77',
                                version='3.1_Patch_1',
                                verify=False,
                                debug=False,
                                uses_csrf_token=False
                                )

#Blank list for node names to be appended too 
nodeList = []
#Testing data for nodes##
#testgetnode = {'response': [{'hostname': 'ise-1', 'fqdn': 'ise-1.lab.devnetsandbox.local', 'ipAddress': '10.10.20.77', 'roles': ['Standalone'], 'services': ['Profiler', 'Session'], 'nodeStatus': 'Connected'},{'hostname': 'ise-2', 'fqdn': 'ise-2.lab.devnetsandbox.local', 'ipAddress': '10.10.20.78', 'roles': ['Standalone'], 'services': ['Profiler', 'Session'], 'nodeStatus': 'Connected'}], 'version': '1.0.0'}
#for node in testgetnode["response"]:
#    nodename = node["hostname"]
#    nodeList.append(nodename)

#API call to get a list of all node Names for use in certificate call. 
getNodes= api.node_deployment.get_nodes().response
for getNode in getNodes["response"]:
    nodename = getNode["hostname"]
    nodeList.append(nodename)

##API call that gets the JSON back from ISE with all Certificate information
for node in nodeList:
    get_sysCerts = api.certificates.get_system_certificates(host_name=node).response

### Not Required, this section can write the content of the API get request in to a json file. 
### And then read from it. You can also use the Stystem Certificates.json as for testing 
##Writes API return in to a .json file
#json_object = json.dumps(get_sysCerts, indent=2)
#with open("SystemCertificates.json", "w") as outfile:
#    outfile.write(json_object)
##Reads .json file to be able to pull appropriate responses 
#with open("SystemCertificates.json", "r") as file:
#    data = json.load(file)

response = get_sysCerts['response']
for keys in response:
    #Sets interesting value Variables using Key pair name
    #This be used to grab other information also as long as you know the name
    id = keys['id']
    issuedBy = keys['issuedBy']
    friendlyName = keys['friendlyName']
    usedBy = keys['usedBy']
    expiryDate = keys['expirationDate']    
    # Formats the expiration dates
    expirationDate = datetime.strptime(expiryDate, '%a %b %d %H:%M:%S %Z %Y')
    expirationDate = datetime.strftime(expirationDate, '%Y-%m-%d')

    # Calculates the amount of days remaining on the certificate given current date.
    dateFormat= "%Y-%m-%d"
    a = time.mktime(time.strptime(expirationDate, dateFormat))
    b = time.mktime(time.strptime(currentTime, dateFormat))
    delta = a-b
    days = int(delta / 86400)
    
    # Print receipt with details
    print ("######################################################################")
    print ("The certifiate for", node, "Is about to Expire in", days, "days")
    print ("This certifiate is used by", usedBy)
    print ("The Certificates Friendly name is", friendlyName) 
    print ("The Certificate ID is", id)
    print ("######################################################################")



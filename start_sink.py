import pulsar, time
from pulsar.schema import *
import json
import requests
from schema import TableSchema

#Pulsar Auth Debian/Ubuntu:
service_url = 'pulsar+ssl://pulsar-gcp-useast4.streaming.datastax.com:6651'
trust_certs = '/etc/ssl/certs/ca-certificates.crt'
pulsar_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjbGllbnQ7MzJhMDkyZWEtMjBiMS00NzQ1LWIzYWQtOTFkNGFiNDU2YWJkO2RISmxjeTFoYldsbmIzTXRhR0ZqYXkxblkzQT0ifQ.YEJTwuUr0ywu-cwK3Cf1o2iUOSCn6b2899E0bxnQltM-4yiT161oWcudhXjR-TXYpoAJ-sGl0TJ0117WBMRHw4-8zbZ3EM8u7VBGKS5xJfiK0wiMzz0v00W-PauL-gwQ_CAaUGaulBkLz13IVUfN6XPpdfdOUJ4ESllJ19lKrxFnjJ4TfdkBtqwbnCg4uOf-8RmfSX_C27jc6UxaLk8cEaSnMTn0skXTDvZhEs43t41e7iiyO1N47t_bAzl5uwCiVY4xOLfCZko9p6Kf8Sb68BCxxDy1jcrJjNaSD3RlY0MetiDrjNqP0gBHepqLVBqdiM2ptyeSlIyIEwq_mtHtcg'
client = pulsar.Client(service_url, authentication=pulsar.AuthenticationToken(pulsar_token), tls_trust_certs_file_path=trust_certs)
print("client created")

#DSE Auth
auth_url = "http://13.92.103.252:8081/v1/auth"
auth_header = {'Content-type': 'application/json'}
body = '{"username": "cassandra","password": "cassandra"}'
r = requests.post(auth_url, data=body, headers=auth_header)
response_dict = json.loads(r.text)
dse_token = response_dict.get("authToken")

#DSE insert
insert_row_url = "http://13.92.103.252:8082/v2/keyspaces/biometrics/biometrics_by_voter"
insert_headers = {'X-Cassandra-Token': dse_token,'Content-type': 'application/json'}

#Dynamic schema reader
def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m

msjdata = String()

#Create Pulsar client
client = pulsar.Client(service_url,
                        authentication=pulsar.AuthenticationToken(pulsar_token),
                        tls_trust_certs_file_path=trust_certs)
#Create subscriber
consumer = client.subscribe('persistent://tres-amigos-hack-gcp/biometrics/dseconsumer', 'dseconsumer-sub',  schema=AvroSchema(TableSchema))

#Check for new messages and wait.
waitingForMsg = True
while waitingForMsg:
    try:
        msg = consumer.receive(2000)
        msjdata = str(msg.value()).replace("'", '"')
        print(msjdata)
        consumer.acknowledge(msg)

        #Post to DSE
        r = requests.post(insert_row_url, data=msjdata, headers=insert_headers)
        print(str(r))
    except:
        print("Still waiting for a message...");

    time.sleep(1)

client.close()
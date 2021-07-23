import pulsar, time
import json
import requests
import auth
import sys,os


#DSE Auth
r = requests.post(auth.auth_url, data=auth.body, headers=auth.auth_header)
response_dict = json.loads(r.text)
dse_token = response_dict.get("authToken")

#DSE insert
insert_headers = {'X-Cassandra-Token': dse_token,'Content-type': 'application/json'}

msjdata = str()

#Class
class TableSchema(Record):
    voter_uuid = String() 
    face_photo_1 = String()
    face_photo_2 = String()
    face_photo_3 = String()
    fingerprint_left_pinky = String()
    fingerprint_left_ring = String()
    fingerprint_left_middle = String()
    fingerprint_left_index = String()
    fingerprint_left_thumb = String()
    fingerprint_right_thumb = String()
    fingerprint_right_index = String()
    fingerprint_right_middle = String()
    fingerprint_right_ring = String()
    fingerprint_right_pinky = String()
    signature = String()
    updated_ts = String()




#Create Pulsar client
client = pulsar.Client(auth.service_url,
                        authentication=pulsar.AuthenticationToken(auth.pulsar_token),
                        tls_trust_certs_file_path=auth.trust_certs)
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
        r = requests.post(auth.insert_row_url, data=msjdata, headers=insert_headers)
        print(str(r))
    except:
        print("Still waiting for a message...");

    time.sleep(1)

client.close()

import pulsar, time
import argparse
import sys,os
import json
import requests

service_url = 'pulsar+ssl://pulsar-gcp-useast4.streaming.datastax.com:6651'
print("parse created")

# Debian/Ubuntu:
trust_certs = '/etc/ssl/certs/ca-certificates.crt'
token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjbGllbnQ7MzJhMDkyZWEtMjBiMS00NzQ1LWIzYWQtOTFkNGFiNDU2YWJkO2RISmxjeTFoYldsbmIzTXRhR0ZqYXkxblkzQT0ifQ.YEJTwuUr0ywu-cwK3Cf1o2iUOSCn6b2899E0bxnQltM-4yiT161oWcudhXjR-TXYpoAJ-sGl0TJ0117WBMRHw4-8zbZ3EM8u7VBGKS5xJfiK0wiMzz0v00W-PauL-gwQ_CAaUGaulBkLz13IVUfN6XPpdfdOUJ4ESllJ19lKrxFnjJ4TfdkBtqwbnCg4uOf-8RmfSX_C27jc6UxaLk8cEaSnMTn0skXTDvZhEs43t41e7iiyO1N47t_bAzl5uwCiVY4xOLfCZko9p6Kf8Sb68BCxxDy1jcrJjNaSD3RlY0MetiDrjNqP0gBHepqLVBqdiM2ptyeSlIyIEwq_mtHtcg'
client = pulsar.Client(service_url, authentication=pulsar.AuthenticationToken(token), tls_trust_certs_file_path=trust_certs)
print("client created")

class Example(Record):
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

producer = client.create_producer(topic='persistent://tres-amigos-hack-gcp/biometrics/dseconsumer', schema=AvroSchema(Example))
print("producer created")

producer.send(Example(voter_uuid="voter_uuid9",
face_photo_1="face_photo_1",
face_photo_2="face_photo_2",
face_photo_3="face_photo_3",
fingerprint_left_pinky="fingerprint_left_pinky",
fingerprint_left_ring="fingerprint_left_ring",
fingerprint_left_index="fingerprint_left_index",
fingerprint_left_thumb="fingerprint_left_thumb",
fingerprint_right_thumb="fingerprint_right_thumb",
fingerprint_right_index="fingerprint_right_index",
fingerprint_right_middle="fingerprint_right_middle",
fingerprint_right_ring="fingerprint_right_ring",
fingerprint_right_pinky="fingerprint_right_pinky",
signature="signature",
updated_ts="2021-04-01T00:00:00Z"))
client.close()
print("message sent")

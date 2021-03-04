import os
import csv
import json

lines = []
with open('data.txt', 'r') as f:
    lines = [line.strip('\n').split('\t') for line in f.readlines()]

model = "business.usarealestate"

fixtures = []

for i, line in enumerate(lines):
    fixtures.append({
        "model": model,
        "pk": int(line[0]),
        "fields": {
            "name": line[1],
            "phone": line[2],
            "city": int(line[3]),
            "street_address": line[4],
            "locality": line[5],
            "pincode": line[6],
            "website": line[7]
        }
    })

with open('usarealestate_fix.json', 'w') as f:
    json.dump(fixtures, f, indent=4)
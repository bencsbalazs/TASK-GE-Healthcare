from datetime import datetime
from flask import request
from flask_restful import Resource
import json


class geHealthcareRestApi(Resource):
    def get(self):
        if (request.form):
            dataRecieved = json.loads(request.form.to_dict(flat=False))
        else:
            try:
                file = open("src/input.json")
                dataRecieved = json.load(file)
                file.close()
            except:
                return str('No input given.')
        return self.parseData(dataRecieved)

    def parseData(self, data):
        dataCollection = []
        for i in range(len(data["entry"])):
            dataCollection.append(self.createEntry(data["entry"][i]))

        return dataCollection

    def getPerformer(self, performerList):
        if performerList is not None:
            pList = []
            for performer in performerList:
                pList.append(performer.get("reference", ""))
            return ", ".join(pList)
        else:
            return ""

    def getValue(self, component):
        if component is not None:
            cList = []
            uList = []
            for c in component:
                if (c.get("valueQuantity", None) is not None):
                    cList.append(c["valueQuantity"]["value"])
                    uList.append(c["valueQuantity"]["unit"])
                else:
                    continue
            return {
                "value": cList,
                "unit": str(set(uList))
            }
        else:
            return {
                "value": "",
                "unit": ""
            }

    def getCoding(self, resource):
        codes = []
        if resource.get("code", None) is not None:
            codes.extend(resource["code"]["coding"])
        return codes

    def createEntry(self, entry):
        res = entry["resource"]
        newEntry = {
            "observationId": res.get("id", ""),
            "patientId": "" if res.get("subject", None) is None else res["subject"].get("reference", ""),
            "performerId": self.getPerformer(res.get("performer", None)),
            "measurementCoding": self.getCoding(res),
            "measurementValue": self.getValue(res.get("component", None))["value"],
            "measurementUnit": self.getValue(res.get("component", None))["unit"],
            "measurementDate": res.get("issued", ""),
            "dataFetched": str(datetime.now())
        }
        return newEntry

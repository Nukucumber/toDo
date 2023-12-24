import json

def updateDate(operation, data, subject, task_name, dateline="", description=""):
    if operation == "ADD":
        if subject == "" or task_name == "" or dateline == "":
            pass
        else:
            if subject not in data:
                data[subject] = {}
                data[subject]["tasks"] = {}
                data[subject]["tasks"]["task_name"] = []
                data[subject]["tasks"]["dateline"] = []
                data[subject]["tasks"]["description"] = []
            try:
                index = data[subject]["tasks"]["task_name"].index(task_name)
                data[subject]["tasks"]["task_name"].pop(index)
                data[subject]["tasks"]["dateline"].pop(index)  
                data[subject]["tasks"]["description"].pop(index)
            except:
                pass              
            data[subject]["tasks"]["task_name"].append(task_name)
            data[subject]["tasks"]["dateline"].append(dateline)
            data[subject]["tasks"]["description"].append(description)

            postData(data)   

    if operation == "DELETE":
        if subject == "" or subject not in data or task_name not in data[subject]["tasks"]["task_name"]:
            pass
        else:
            if task_name == "":
                del data[subject]
            else:
                if (len(data[subject]["tasks"]["task_name"]) == 1):
                    del data[subject]
                else:
                    index = data[subject]["tasks"]["task_name"].index(task_name)
                    data[subject]["tasks"]["task_name"].pop(index)
                    data[subject]["tasks"]["dateline"].pop(index)
                    data[subject]["tasks"]["description"].pop(index)
            postData(data)  

def getData():
    with open("data/data.json") as inputFile:
        try:
            data = json.load(inputFile)
            return data
        except:
            return {}

def postData(data):
    with open("data/data.json", 'w') as outputFile:
        json.dump(data, outputFile)
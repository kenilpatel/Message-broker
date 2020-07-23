import json

empty_dict = "{\"A\":{\"data\":[]},\"B\":{\"data\":[]},\"C\":{\"data\":[]}}"
dict = json.loads(empty_dict)
fr = open("queue.txt", "w")
fr.write(json.dumps(dict))
fr.close()
fr = open("queue.txt", "r")
data = fr.read()
print(data)
dict = json.loads(data)
fr.close()
# perform append data
dict["A"]["data"].append("this is kenil")
fr = open("queue.txt", "w")
fr.write(json.dumps(dict))
fr.close()


dict={}
dict["A"]["data"] = []
dict["B"]["data"] = []
dict["C"]["data"] = []
fr = open("queue.txt", "w")
fr.write(json.dumps(dict))
fr.close()

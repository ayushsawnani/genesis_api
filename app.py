import time
from flask import Flask
import backend
import json
app = Flask(__name__)



#app route for summary (name, mp)
@app.route("/summary/user=<user>&pass=<pas>")
def summary(user, pas):
    for i in pas:
        if i == '=':
            pas = pas.replace(i, '#')
        elif i == "~":
            pas = pas.replace(i, '%')
    

    b = backend.PortalControl(user, pas)
    print(user, " ", pas)
    b.login()

    name = b.get_name()
    mp = b.get_currentMP()

    classes = b.get_scheduleClasses()
    rooms = b.get_scheduleRooms()
    times = b.get_scheduleTimes()
    teachers = b.get_scheduleTeachers()



    json_string = {}

    json_string["name"] = name
    json_string["markingPeriod"] = mp

    json_string["schedule"] = []

    for i in range(len(classes)):

        json_string["schedule"].append({"class" : classes[i],"teacher" : teachers[i], "room": rooms[i], "time": times[i]})

    



    print (json_string)

    json_obj = json.loads(json.dumps(json_string))
    
    return json_obj




@app.route("/gradebook/user=<user>&pass=<pas>")
def gradebook(user, pas):


    for i in pas:
        if i == '=':
            pas = pas.replace(i, '#')
        elif i == "~":
            pas = pas.replace(i, '%')
    

    b = backend.PortalControl(user, pas)
    print(user, " ", pas)
    b.login()

    
    classes = b.get_classes()
    grades = b.get_grades()
    teachers = b.get_teachers()
    letters = b.get_letters()

    json_string = {}

    json_string["classes"] = []

    for i in range (len(letters)):
        print(i)
        json_string["classes"].append({"class" : classes[i], "teacher" : teachers[i], "grade" : grades[i], "letter" : letters[i]})


    print (json_string)

    json_obj = json.loads(json.dumps(json_string))
    
    return json_obj



    
    




if __name__ == '__main__':
    app.run()
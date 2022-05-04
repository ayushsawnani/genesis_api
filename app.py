import time
from flask import Flask
import backend
import json
app = Flask(__name__)



@app.route("/login/user=<user>&pass=<pas>")
def getClassesAndGrades(user, pas):


    for i in pas:
        if i == '3':
            pas = pas.replace(i, '#')
    

    b = backend.PortalControl(user, pas)
    print(user, " ", pas)
    b.login()

    
    classes = b.get_classes()
    grades = b.get_grades()
    teachers = b.get_teachers()
    letters = b.get_letters()

    json_string = {}

    for i in range (len(classes)-1):
        print(i)
        json_string[classes[i]] = []
        json_string[classes[i]].append({"teacher" : teachers[i], "grade" : grades[i], "letter" : letters[i]})


    print (json_string)

    json_obj = json.loads(json.dumps(json_string))
    
    return json.dumps(json_obj, indent=4)
    
    




if __name__ == '__main__':
    app.run()
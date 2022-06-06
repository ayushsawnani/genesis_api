
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import secret



getlogin = ('https://students.sbschools.org/genesis/sis/view?gohome=true')

dc = DesiredCapabilities.CHROME
dc['goog:loggingPrefs'] = { 'browser':'ALL' }
chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.3')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument("headless")

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])



class PortalControl:
    def __init__(self, u, pa):
        self.user = u
        self.p = pa
        self.name = ""
        self.currentMP = ""
        self.day = ""
        self.date = ""
        self.scheduleClasses = []
        self.scheduleRooms = []
        self.scheduleTeachers = []
        self.scheduleTimes = []
        self.classes = []
        self.classes_ = []
        self.grades = []
        self.teachers = []
        self.letters = []
        self.driver = webdriver.Chrome(desired_capabilities=dc, executable_path=secret.path, chrome_options=chrome_options, options=options)
        self.driver.minimize_window()


    def login(self):


    
        self.driver.get(getlogin)

        #enter credentials
        email_path = self.driver.find_element(By.ID, 'j_username')

        pass_path = self.driver.find_element(By.ID, 'j_password')

        login = self.driver.find_element(By.CLASS_NAME, 'saveButton')

        email_path.send_keys(self.user+'@sbstudents.org')
        pass_path.send_keys(self.p)

        login.click()
        print("logged in")

        #SUMMARY URL
        self.driver.get('https://students.sbschools.org/genesis/parents?tab1=studentdata&tab2=studentsummary&action=form&studentid=' + self.user)
        name = self.driver.find_element(By.XPATH, '/html/body/form[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table[1]/tbody/tr[1]/td[1]')

        #get the name
        self.name = name.text

        #get the day (a or b)
        self.day = self.driver.find_element(By.XPATH, '/html/body/form[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr/td[4]/div/b').text

        #get the date
        self.date = self.driver.find_element(By.XPATH, '/html/body/form[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div[1]').text

        
        #schedule
        w = self.driver.find_elements(By.CLASS_NAME, 'cellLeft')

        h = []

        for i in range (0, len(w)):
            if i > 12:
                h.append(w[i].text)

        
        
        
        for j in range(0, len(h)):

            #times
            if j%2 == 0:
                qwe = h[j][9 : len(h[j])]
                if j > 0:
                    qwe = h[j][9 : len(h[j])]
                
                if j == 4 or j == 6:
                    qwe = qwe[2 : len(qwe)]
            
                self.scheduleTimes.append(qwe)

   
        #rooms teachers classes
        for k in range(1, len(h), 2):

            self.scheduleClasses.append( h[k : k+1][0][ 0 : h[k : k+1][0].index("\n")] )
            ti = h[k : k+1][0].find("\n", h[k : k+1][0].find("\n") + 1)
            if ti != -1:
                self.scheduleTeachers.append(h[k : k+1][0][h[k : k+1][0].index("\n") + 1 : ti])
                self.scheduleRooms.append(h[k : k+1][0][ti+1 : len(h[k : k+1][0])])
            else:
                self.scheduleTeachers.append(" ")
                self.scheduleRooms.append("Lunch Room")
            
        
        
                    



        #get the schedule rooms

        #get the schedule teachers

        #GRADEBOOK URL
        self.driver.get('https://students.sbschools.org/genesis/parents?tab1=studentdata&tab2=gradebook&tab3=weeklysummary&studentid=' + self.user + '&action=form')


        #get the marking period
        select = Select(self.driver.find_element(By.NAME, 'fldMarkingPeriod'))
        option = select.first_selected_option
        self.currentMP = option.text
        




        #get the classes
        h = self.driver.find_elements(By.CLASS_NAME, "categorytab")
        for i in h:
            #append the text
            self.classes.append(i.text)

            #append the object for getting assignments
            self.classes_.append(i)


        #get the grades
        z = self.driver.find_elements(By.CLASS_NAME, "cellRight")
        for j in z:
        
            if j.get_attribute("onclick") != None: 
                
                if "%" in j.text:
                    self.grades.append(j.text)
                else:
                    self.letters.append(j.text)

            elif "Not Graded MP4" in j.text:
                self.grades.append("n/a")
                self.letters.append("n/a")
        
        #get the teachers
        b = self.driver.find_elements(By.CLASS_NAME, "cellLeft")
        for k in b:
            if k.get_attribute("onclick") == None and k.text not in self.classes and "Email" in k.text:
                self.teachers.append(k.text[0 : k.text.index('Email')-1])
        
        self.driver.close()
        
        
    

    def get_name(self):
        return self.name
    def get_currentMP(self):
        return self.currentMP
    def get_classes(self):
        return self.classes
    def get_grades(self):
        return self.grades
    def get_teachers(self):
        return self.teachers
    def get_letters(self):
        return self.letters
    def get_day(self):
        return self.day
    def get_date(self):
        return self.date
    def get_scheduleClasses(self):
        return self.scheduleClasses
    def get_scheduleRooms(self):
        return self.scheduleRooms
    def get_scheduleTeachers(self):
        return self.scheduleTeachers
    def get_scheduleTimes(self):
        return self.scheduleTimes
    

    
        

    def getAssignments(self, student_class):
        class_name = None
        
        for c in self.classes_:
            if student_class in c.text:
                class_name = c.get_attribute("onclick")[int(c.get_attribute("onclick").index("H")): int(c.get_attribute("onclick").index(")"))-1]

        #print('https://students.sbschools.org/genesis/parents?tab1=studentdata&tab2=gradebook&tab3=listassignments&studentid='+ self.user +'&action=form&dateRange=MP4&date=05/02/2022&courseAndSection='+class_name)
        self.driver.get('https://students.sbschools.org/genesis/parents?tab1=studentdata&tab2=gradebook&tab3=listassignments&studentid='+ self.user +'&action=form&dateRange=MP4&date=05/02/2022&courseAndSection='+class_name)

        x = self.driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr[2]/td/table/tbody")
        #print(x.text)
        self.driver.close()

        

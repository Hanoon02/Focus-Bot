import cal
class User:
    def __init__(self):
        self.tasks = []
        self.time = 0
    def signUp(self):
        try:
            cal.main()
            return True
        except:
            return False
    def getTask(self,date):
        with open('calendar.txt', 'r') as reader:
            a = False
            for row in reader:
                fRow = row.split('--::')
                if fRow[0] == date:
                    a = True
                    tm = int(fRow[2].split(':')[0])*60+int(fRow[1].split(':')[1])-(int(fRow[1].split(':')[0])*60+int(fRow[1].split(':')[1]))
                    self.time += tm
                    self.tasks.append(str(fRow[3]) + ' for duration of ' + str(tm) + ' minutes')
                elif a:
                    self.tasks.append(f'You have work scheduled for {self.time} minutes')
                    return self.tasks
            if len(self.tasks) == 0 :
                return []
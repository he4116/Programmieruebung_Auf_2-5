import json

class Person:
    
    @staticmethod
    def load_person_data():
        """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
        file = open("data/person_db.json")
        person_data = json.load(file)
        return person_data

    @staticmethod
    def get_person_list(person_data):
        """A Function that takes the persons-dictionary and returns a list auf all person names"""
        list_of_names = []

        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names
    
    @staticmethod
    def find_person_data_by_name(suchstring):
        """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
        und die die Person als Dictionary zurück gibt"""

        person_data = Person.load_person_data()
        #print(suchstring)
        if suchstring == "None":
            return {}

        two_names = suchstring.split(", ")
        vorname = two_names[1]
        nachname = two_names[0]

        for eintrag in person_data:
            print(eintrag)
            if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
                print()

                return eintrag
        else:
            return {}
        

    # kalkulierung des Alters
    @staticmethod
    def calc_age(date_of_birth):
        """A Function that calculates the age from a date of birth"""
        from datetime import datetime
        today = datetime.today()
        dob = datetime.strptime(str(date_of_birth), "%Y")
        age = today.year - dob.year
        return age
    
    def calc_max_heart_rate(self):
        """A Function that calculates the maximum heart rate"""
        if self.gender == "male":
            return 220 - self.calc_age(self.date_of_birth)
        else:
            return 226 - self.calc_age(self.date_of_birth)
        
    def load_by_id(self, person_id):
        """A Function that loads a person by their ID"""
        person_data = Person.load_person_data()
        for eintrag in person_data:
            if eintrag["id"] == person_id:
                return eintrag
        return {}
    
   

    def __init__(self, person_dict) -> None:
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]
        self.date_of_birth = person_dict["date_of_birth"]
        self.gender = person_dict["gender"]


if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    persons = Person.load_person_data()
    person_names = Person.get_person_list(persons)
    print(person_names)
    print(Person.find_person_data_by_name("Huber, Julian"))

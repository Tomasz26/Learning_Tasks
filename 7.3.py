from faker import Faker
fake = Faker()

class BaseContact:
    def __init__(self, name, surname, mail, private_number):
        self.name = name
        self.surname = surname
        self.mail = mail
        self.private_number = private_number
    
        #variables
        self._name_and_surname_len = len(self.name) + len(self.surname) + 1

    @property
    def label_length(self):
        return self._name_and_surname_len

    def __str__(self):
        return f"Imię i nazwisko: {self.name} {self.surname}, mail: {self.mail}, numer: {self.private_number}"
    
    
    def contact(self):
        print(f"Wybieram numer {self.private_number} i dzwonię do {self.name} {self.surname}")

class BusinessContact(BaseContact):
    def __init__(self, job, company, job_number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job = job
        self.company = company
        self.job_number = job_number

    def __str__(self):
        return f"Imię i nazwisko: {self.name} {self.surname}, mail: {self.mail}, firma: {self.company}, pozycja: {self.job}, numer służbowy: {self.job_number}"
    
    def contact(self):
        print(f"Wybieram numer {self.job_number} i dzwonię do {self.name} {self.surname}, z firmy: {self.company}")


def RandomGuy():
    return BaseContact(fake.first_name(), fake.last_name(), fake.email(), fake.phone_number())

def RandomWorkGuy():
    return BusinessContact(fake.job(), fake.company(), fake.phone_number(), fake.first_name(), fake.last_name(), fake.email(), fake.phone_number())

someone = RandomGuy()
someone2 = RandomGuy()
someonework = RandomWorkGuy()

def create_contacts(card_type, number):
    for i in range(number):
        if card_type == "Business":
            Cards.append(RandomWorkGuy())
        elif card_type == "Home":
            Cards.append(RandomGuy())
        else:
            print("You need to give Business or Home argument")


Cards = [someone, someone2, someonework]

create_contacts('Business', 5)

by_name = sorted(Cards, key=lambda card: card.name)
by_surname = sorted(Cards, key=lambda card: card.surname)
by_mail = sorted(Cards, key=lambda card: card.mail)

print(someonework.label_length)
someone.contact()
someonework.contact()

for card in by_surname:
    print(f"{card}")
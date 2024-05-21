# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class codeCreatorAction(Action):
    def __init__(self) -> None:
        self.storage = Storage()

    def name(self):
        return "action_code_creator"

    def run(self, dispatcher, tracker, domain):
        code_reservation = self.storage.getNewCode()
        
        slot_date_heure = tracker.get_slot('slot_date_heure')
        slot_nb_personnes = tracker.get_slot('slot_nb_personnes')
        slot_nom = tracker.get_slot('slot_nom')
        slot_numero_telephone = tracker.get_slot('slot_numero_telephone')
        slot_commentaire = tracker.get_slot('slot_commentaire')

        self.storage.addReservation(code_reservation, slot_date_heure, slot_nb_personnes, slot_nom, slot_numero_telephone, slot_commentaire)
        dispatcher.utter_message(text=f"Voici votre code de reservation. Veuillez le noter afin de ne pas le perdre : {code_reservation}")
        return {"code_reservation": code_reservation}


class validateCodeInformations(Action):
    def __init__(self) -> None:
        self.storage = Storage()

    def name(self):
        return "validation_code_informations"

    def run(self, dispatcher, tracker, domain):
        slot_code = tracker.get_slot('slot_code')
        for i in self.storage.getReservationList():
            if(i.getCode()==slot_code):
                infos = i.getInfos()
                dispatcher.utter_message(text=f"Voici les informations de votre reservation : \n{infos}.\nVoulez vous modifier votre commentaire ?")
                return []
        dispatcher.utter_message(text=f"Aucune reservation n'a été trouvée pour ce code, veuillez réessayer avec un code correct.")
        return []

class validateTableAvailable(Action):
    def __init__(self) -> None:
        self.storage = Storage()

    def name(self):
        return "validation_table_available"

    def run(self, dispatcher, tracker, domain):
        slot_date_heure = tracker.get_slot('slot_date_heure')
        slot_date_heure_list = tracker.get_slot('slot_date_heure').split(" ")
        slot_nb_personnes = tracker.get_slot('slot_nb_personnes')

        date = slot_date_heure_list[0] + " " + slot_date_heure_list[1]
        personNumber = self.storage.getPersonNumberByDate(date)
        if(int(personNumber) + int(slot_nb_personnes) <= 5):
            dispatcher.utter_message(text=f"Très bien pour le {slot_date_heure} pour {slot_nb_personnes} personnes\nIl y a une table de libre pour vous !\nVous confirmez ?")
            return[]
        dispatcher.utter_message(text=f"Malheureusement, aucune table n'est libre pour le {slot_date_heure} pour {slot_nb_personnes} personnes")
        return []

class modificationCommentaire(Action):
    def __init__(self) -> None:
        self.storage = Storage()

    def name(self):
        return "modification_commentaire"

    def run(self, dispatcher, tracker, domain):
        slot_code = tracker.get_slot('slot_code')
        slot_commentaire = tracker.get_slot('slot_commentaire')
        self.storage.modifierCommentaire(slot_code, slot_commentaire)
        dispatcher.utter_message(text=f"Votre ancien commentaire a été remplacé par : \n{slot_commentaire}")
        return []
    

class validateCodeAnnulation(Action):
    def __init__(self) -> None:
        self.storage = Storage()

    def name(self):
        return "validation_code_annulation"

    def run(self, dispatcher, tracker, domain):
        slot_code = tracker.get_slot('slot_code')
        for i in self.storage.getReservationList():
            if(i.getCode()==slot_code):
                nom = i.getNom()
                date = i.getDate()
                dispatcher.utter_message(text=f"Une reservation a été trouvée au nom de {nom} le {date}.\nÊtes vous sur de vouloir annuler votre reservation ?")
                return []
        dispatcher.utter_message(text=f"Aucune reservation n'a été trouvée pour ce code, veuillez réessayer avec un code correct.")
        return []
    
class annulationReservation(Action):
    def __init__(self) -> None:
        self.storage = Storage()

    def name(self):
        return "annulation_reservation"

    def run(self, dispatcher, tracker, domain):
        slot_code = tracker.get_slot('slot_code')
        nom = self.storage.getNomFromCode(slot_code)
        self.storage.removeReservation(slot_code)
        print("nom trouvé : "+nom)
        dispatcher.utter_message(text=f"Votre reservation au nom de {nom} a bien été annulée.\nBonne fin de journée et au plaisir de vous revoir !")
        return []
    
class Reservation:
    def __init__(self, code, date_heure, nb_personnes, nom, numero_tel, commentaire):
        self.code = code
        self.date_heure = date_heure
        self.nb_personnes = nb_personnes
        self.nom = nom
        self.numero_tel = numero_tel
        self.commentaire = commentaire

    def reservationFromList(informations):
        return Reservation(informations[0], informations[1], informations[2], informations[3], informations[4], informations[5])
    
    def getCode(self):
        return self.code
    
    def getNom(self):
        return self.nom
    
    def getDate(self):
        return self.date_heure

    def getPersonNumber(self):
        return self.nb_personnes

    def getInfos(self):
        return "code : "+self.code + ", date et heure : "+ self.date_heure+ ", nombre de personnes : "+ self.nb_personnes + ", nom : "+ self.nom + ", numéro de téléphone : "+ self.numero_tel + ", Commentaire : " + self.commentaire

class Storage:
    def __init__(self):
        self.codeStorage = []
        self.integer = 0

    def getCodeStorage(self):
        return self.codeStorage

    def getNewCode(self):
        self.integer += 1
        return self.integer
    
    def addReservation(self, code, date_heure, nb_personnes, nom, numero_tel, commentaire):
        with open('actions/storage/reservation_storage.csv', 'a', encoding='utf-8') as writer:
            writer.write("\n"+str(code) +';' + str(date_heure) +';'+ str(nb_personnes) +';'+ str(nom) +';'+ str(numero_tel) +';'+ str(commentaire))

    def getAllReservation(self) -> str:
        string = "Les reservations :"
        file = open('actions/storage/reservation_storage.csv', 'r', encoding='utf-8')
        lines = file.readlines()
        if(len(lines)>1):
            for i in range(1, len(lines)):
                reservation = Reservation.reservationFromList(lines[i].split(";"))
                string += "\n"+ reservation.getInfos()
        return string

    def getReservationList(self):
        reservationList = []
        file = open('actions/storage/reservation_storage.csv', 'r', encoding='utf-8')
        lines = file.readlines()
        if(len(lines)>1):
            for i in range(1, len(lines)):
                reservation = Reservation.reservationFromList(lines[i].split(";"))
                reservationList.append(reservation)
        return reservationList
    
    #procédure qui supprime une reservation du fichier à partir d'un code
    def removeReservation(self, code):
        with open('actions/storage/reservation_storage.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open('actions/storage/reservation_storage.csv', 'w', encoding='utf-8') as f:
            for line in lines:
                if line.split(";")[0] != str(code):
                    f.write(line)

    #fonction qui renvoie le nom associé à une reservation à partir d'un code
    def getNomFromCode(self, code):
        file = open('actions/storage/reservation_storage.csv', 'r', encoding='utf-8')
        lines = file.readlines()
        for line in lines:
            if line.split(";")[0] == str(code):
                return line.split(";")[3]
        return "0"

    #procédure qui modifie le commentaire d'une reservation à partir d'un code
    def modifierCommentaire(self, code, commentaire):
        with open('actions/storage/reservation_storage.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open('actions/storage/reservation_storage.csv', 'w', encoding='utf-8') as f:
            for line in lines:
                if line.split(";")[0] == str(code):
                    line = line.replace(line.split(";")[5], commentaire)
                f.write(line)

    def getPersonNumberByDate(self, date):
        reservationList = self.getReservationList()
        personNumber = 0
        for reservation in reservationList:
           full_date = reservation.getDate()
           current_date = full_date.split(" ")[0] + " " + full_date.split(" ")[1]
           if(current_date.lower() == date.lower()):
               personNumber += int(reservation.getPersonNumber())
        return personNumber

#code;date_heure;nb_personnes;nom;numero_telephone;commentaire
#3;1 mai à 12h20;5;PERSONNE;6465210245;j'adore la viande miam miam
#2;1 avril à 00h01;5;Dupont;0285745698;j'ai faim donc un plein de bouffe svp
#1;3 novembre à 00h00;2;Durant;0636545210;je suis végétarien
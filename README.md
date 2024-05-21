# rasa_reservation_bot
Agent conversationnel permettant notamment de reserver une table et de gérer ses réservations (et d'autres fonctionnalités)


## Mode d'emploi

### Lancement du bot
Ouvrez un terminal dans le dossier "rasa_reservation_bot", puis entrez la commande 
```rasa run actions```
Puis, ouvrez un second terminal dans le même dossier et entrez la commande 
```rasa shel```

<br>
Après un certain moment, vous apercevrez "Your input ->" et pourrez échanger avec le bot.

Commencez par saluer le bot avec un "bonjour" ou "bonsoir", et laissez vous guider !

### Remarques
Afin de simuler l'affluence (et donc le manque de places) dans le restaurant, le nombre maximum de personnes par jour est de 5 cumulé. Par exemple, vous ne pourrez pas faire de réservation pour 2 personnes le 2 avril si une réservation est déjà prévue ce jour pour 4 personnes. Il en va de même pour les réservations de plus de 5 personnes.

### Conseils d'utilisation : 
- Certaines formulations de phrases sont ambigues pour le bot, si un parcourt qui vous semble anormal survient, veuillez reformuler votre dernière phrase autrement. Les phrases construites fonctionnent mieux que des phrases trop courtes
- Veuillez renseigner la date avec ce format quand demandé : "X mois à XXhXX", autrement votre reservation pourrait être difficilement reconnue. 

Bug connus : 
- Votre nom ne sera probablement pas corrrectement pris en charge et sera remplacé par None le cas échéant. Dans le cas contraire : **Félicitations** !

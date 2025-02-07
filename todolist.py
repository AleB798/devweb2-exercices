# Concevoir une petite application type todolist simple en python et mongoDB.

# Voici les fonctionnalités attendu.
# Un menu avec : 
# - Afficher les tâches
# - Ajouter une tâche
# - Supprimer une tâche
# - Mettre à jour la description
# - Mettre à jour le statut d'une tâche (0 : nouvelle, en cours : 1, terminée : 2)

import pymongo
# print ("version:", pymongo.version)
import datetime
import os
# Import pour manipuler les ObjectId de MongoDB
from bson.objectid import ObjectId  

#  classe MongoClient du module pymongo : permet de se connecter à une base de données MongoDB depuis un script Python.
from pymongo import MongoClient 

# // teste si l'on arrive a se connecter à la DB sinon renvoit une erreur
try: 
    
    # Lien de connexion (en local) 
    client = MongoClient('mongodb://localhost:27017/') 
    
    # Accès à la DB
    mydatabase = client['todolist'] 
    
    # Accès à la collection 
    mycollection = mydatabase['tasks'] 

except Exception as e:
    print(f"Erreur de connexion : {e}")
    exit()
  
# Création de plusieurs tâches pour "initaliser" la DB
tasks = [
    {
        "title": "faire les courses",
        "description": "Acheter du pain et du lait",
        "status": 0,

        # méthode de la bibliothèque datetime en Python 
        # elle renvoit la date et l'heure actuelles du système au moment de l'exécution.
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now()
    },
    {
        "title": "réviser Python",
        "description": "Chapitre sur MongoDB",
        "status": 1,
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now()
    },
    {
        "title": "sport",
        "description": "Aller courir 30 minutes",
        "status": 2,
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now()
    }
]
  
# insertion dans la DB si celle-ci ne contient pas de données
if mycollection.count_documents({}) == 0:
    # utilisation de many car plusieurs tâches a insérer.
    mycollection.insert_many(tasks)
    # print(tasks)

# ========> TO DO LIST ACTIONS <========

# --> 1. Afficher les tâches <--
def showTasks ():
    tasks = mycollection.find() # stocke dans une constante les données trouvées dans la collection ()
    print("\n--- LISTE DES TÂCHES ---")
    for task in tasks:
        print(f"Titre       : {task['title']}")
        print(f"Description : {task['description']}")
        print(f"Statut      : {'Nouvelle' if task['status'] == 0 else 'En cours' if task['status'] == 1 else 'Terminée'}")
        print(f"Créée le    : {task['created_at']}")
        print(f"Mise à jour : {task['updated_at']}")
        print("-" * 80)


# --> 2. Ajouter une tâche <--
def addTask():

    while True:

        taskTitle = input("Entrer le nom de la tâche : ").lower()
        taskDescription = input("Entrer une courte description : ").lower()
        taskStatus = int(input("Entrer le chiffre correspondant au status : "))
        newTask = {
            'title' : taskTitle,
            'description' : taskDescription,
            'status' : taskStatus,
            'created_at' : datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        }

        # vérifier si la tâche est déjà présente sinon l'ajouter + prévenir
        existingTask = mycollection.find_one({"title": newTask['title']})
        if existingTask:
            print("Cette tâche existe déjà dans la base de données.")
        else:
            addNewTask = mycollection.insert_one(newTask)
            print("Tâche ajoutée avec succès !")

        # on demande si l'utilisateur souhaite ajouter une nouvelle tâche sinon on sort de la boucle
        addAnotherTask = input("Voulez-vous ajouter une autre tâche ? (oui/non) : ").strip().lower()
        if(addAnotherTask != 'oui'):
            break


# --> 3. Supprimer une tâche <--
def deleteTask():

    taskToDelete = input("Nommer la tâche que vous souhaitez supprimer : ").lower()

    # vérifier que la tâche existe en comparant les titles existant et l'input entré
    existingTask = mycollection.find_one({"title": taskToDelete})

    # condition : si la tâche existe récupérer son ID, reconfirmer la suppression et si oui la supprimer
    if existingTask:
        taskId = existingTask["_id"]
        confirm = input(f"Êtes-vous sûr(e) de vouloir supprimer '{taskToDelete}' ? (oui/non) : ").strip().lower()
        if confirm == "oui":
            mycollection.delete_one({"_id": ObjectId(taskId)})  # Supprimer via l'ID
            print(f"La tâche '{taskToDelete}' a été supprimée avec succès.")
        else:
            print("Suppression annulée.")
    else:
        print("Cette tâche n'existe pas.")


# --> 4. Modifier une tâche <--
def updateDescription():
    taskToUpdate = input("Nommer la tâche dont la description doit être modifiée : ").lower()

    existingTask = mycollection.find_one({"title": taskToUpdate})
    if existingTask:
        newDescription = input("Entrer la nouvelle description : ").lower()
        mycollection.update_one(
            {"_id": existingTask["_id"]},
            {"$set": {"description": newDescription, "updated_at": datetime.datetime.now()}}
        )
        print("Description mise à jour avec succès.")
    else:
        print("Cette tâche n'existe pas.")


# --> 5. Mettre à jour le statut <--
def updateStatus():
    taskToUpdate = input("Nommer la tâche dont le statut doit être modifié : ").lower()

    existingTask = mycollection.find_one({"title": taskToUpdate})
    if existingTask:
        newStatus = int(input("Entrer le nouveau status (0 : nouvelle, en cours : 1, terminée : 2) : "))
        mycollection.update_one(
            {"_id": existingTask["_id"]},
            {"$set": {"status": newStatus, "updated_at": datetime.datetime.now()}}
        )
        print("Statut mis à jour avec succès.")
    else:
        print("Cette tâche n'existe pas.")

# =====> MENU INTERACTIF <=====

print("Que souhaitez-vous faire ?")
print("1. Afficher les tâches")
print("2. Ajouter une tâche")
print("3. Supprimer une tâche")
print("4. Mettre à jour une tâche")
print("5. Mettre à jour le statut d'une tâche (0 : nouvelle, en cours : 1, terminée : 2)")

try:
    choix = int(input('Quel est votre choix : '))
except ValueError:
    print("Veuillez entrer un nombre valide.")
    exit()

os.system('cls')


if choix == 1 :
    showTasks()

if choix == 2 :
    print("Pour ajouter une tâche veuillez renseigner un nom, une courte description, et le status")
    print("Les statuts sont le suivants : 0 : nouvelle, en cours : 1, terminée : 2")
    addTask()
    showTasks()

if choix == 3 :
    showTasks()
    deleteTask()

if choix == 4 :
    updateDescription()
    showTasks()

if choix == 5 :
    updateStatus()
    showTasks()

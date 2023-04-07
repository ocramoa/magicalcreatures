import firebase_admin
from firebase_admin import firestore

app = firebase_admin.initialize_app()
db = firestore.Client(project='magical-creatures-38046')

# class User:

#     def __init__(self, creatures, habitats, money, password):
#         self.creatures = creatures # Dict of Creature classes
#         self.habitats = habitats
#         self.money = money
#         self.password = password

# class Creature:

#     def __init__(self, name, info, size, price, status, dislikes, likes, friendliness, byproduct):
#         self.name = name
#         self.info = info
#         self.size = size
#         self.price = price
#         self.status = status
#         self.dislikes = dislikes
#         self.likes = likes
#         self.friendliness = friendliness
#         self.byproduct = byproduct

def print_all_users():
    users_ref = db.collection('users')
    docs = users_ref.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

def new_user(username, password):
    username_string = str(username)
    password_string = str(password)
    doc_ref = db.collection('users').document(username_string)
    doc_ref.set({
        'money' : 3000, 
        'habitats' : ["Ocean"], 
        'password' : password_string,
        'username' : username_string,
        'creatures' : 
            { 'creature' : 
             {'name' : 'Minnow',
              'info' : 'A small minnow.',
              'size' : 1,
              'price': 3,
              'status' : True,
              'dislikes' : ['Cat', 'kibble', 'heat'],
              'likes' : ['water', 'Minnow', 'flakes'],
              'friendliness' : 1,
              'byproduct': { 'name' : 'scale', 'price' : 1}}}})
    
    newdoc = doc_ref.get()
    doc = newdoc.to_dict()
    return doc
    
def get_zoo_names():
    animals = db.collection('zoo').select(field_paths=[]).stream()
    names = [item.id for item in animals]
    print(names)

def get_habitat_names():
    habitats = db.collection('habitats').select(field_paths=[]).stream()
    names = [item.id for item in habitats]
    return names

def auth_user():
    inp = input("Enter your username and password in this format: Username|Password, then hit enter. ")
    real_inp = inp.split('|')
    
    if len(real_inp) < 2 or len(real_inp) > 2:
        print("Invalid input. Try again.")
        auth_user()
    
    username = real_inp[0]
    password = real_inp[1]
    
    try:
        user = db.collection('users').document(username).get()
    except:
        inp2 = input("Dang, it didn't work! Would you like to add yourself as a user? Y/N ")
        if inp2 == 'Y':
            new = new_user(username, password)
            print(f"There you go! Remember your username and password are: {username}, {password} ")
            display_user_info(new)
        else:
            print(':\'(')
    
    userdoc = user.to_dict()
    
    if userdoc['password'] == password:
        print("Gotcha!")
        now_go(userdoc)
    else:
        print("Invalid password or user.")
        inp2 = input("Dang, it didn't work! Would you like to add yourself as a user? Y/N ")
        if inp2 == 'Y':
            new = new_user(username, password)
            print(f"There you go! Remember your username and password are: {username}, {password} ")
            display_user_info(new)
        else:
            print(':\'(')

def now_go(user_dict): # To be removed. Added while I was confused and debugging.
    display_user_info(user_dict)
    
def display_user_info(user_dict):
    question = input("Enter what you would like to see: Creatures/Money/Habitats ")
    
    if question == "Creatures":
        print(user_dict['creatures'])
        prompt = input("Would you like to work with your creatures? Y/N ")
        if prompt == 'N':
            display_user_info(user_dict)
        elif prompt == 'Y':
            prompt2 = input("Would you like to purchase, sell, or feed a creature? P/S/F ")
            if prompt2 == 'P':
                purchase_creature(user_dict)
            elif prompt2 == 'S':
                sell_creature(user_dict)
            elif prompt2 == 'F':
                feed_creature(user_dict)
            
    elif question == "Money":
        print(user_dict['money'])
        prompt = input("Would you like to purchase a creature or habitat? Y/N ")
        if prompt == 'N':
            display_user_info(user_dict)
        elif prompt == 'Y':
            prompt2 = input("Creature or Habitat? C/H ")
            if prompt2 == 'C':
                purchase_creature(user_dict)
            elif prompt2 == 'H':
                purchase_habitat(user_dict)
            else:
                print('AHHHHHH')

    elif question == "Habitats":
        print(user_dict['habitats'])
        print("Would you like to purchase an additional habitat?")
        prompt = input(f"Your available funds are: {user_dict['money']}. Y/N ")
        if prompt == 'N':
            display_user_info(user_dict)
        elif prompt == 'Y':
            purchase_habitat(user_dict)
    
    else:
        print("Invalid command! Sorry!")
        display_user_info(user_dict)

def purchase_creature(user_dict):
    print("Here are the available creatures: ")
    get_zoo_names()
    print(f"Your available funds are: {user_dict['money']}")
    prompt = input("What creature would you like to purchase? Enter the name or N if none. ")
    if prompt == 'N':
        display_user_info(user_dict)
    else:
        # try:
            creature = db.collection('zoo').document(prompt).get()
            doc = creature.to_dict()
            if doc['price'] <= user_dict['money']:
                # Update user db
                userdoc = db.collection('users').document(user_dict['username'])
                userdoc.update({f'creatures.{creature.id}' : doc})
                new_balance = user_dict['money'] - doc['price']
                userdoc.update({f'money' : new_balance})
                print("Gotcha!")
                userdoc_updated = db.collection('users').document(user_dict['username']).get()
                new_dict = userdoc_updated.to_dict()
                print("New Creature!")
                print(new_dict['creatures'])
                display_user_info(new_dict)
            else:
                print("Not enough money!")
                display_user_info(user_dict)
        # except:
        #     print("Invalid creature! Or something else happened. idk lol")
        #     purchase_creature(user_dict)

def sell_creature(user_dict):
    # Must return new user dict to display user info
    print("Here are your creatures: ")
    print(user_dict['creatures'])
    
    prompt = input("Which creature would you like to sell? Enter N if none. ")

    if prompt == 'N':
        display_user_info(user_dict)
    
    else: 
        userdoc_s = db.collection('users').document(user_dict['username'])
        creature_price = user_dict['creatures'][f'{prompt}']['price']
        new_balance = user_dict['money'] + creature_price

        userdoc_s.update({f'creatures.{prompt}' : firestore.DELETE_FIELD})
        userdoc_s.update({f'money' : new_balance})
        
        userdoc_updated = db.collection('users').document(user_dict['username']).get()
        new_dict = userdoc_updated.to_dict()
        print(f"Sadness! {prompt} was sold. Your new balance is {new_dict['money']}")
        display_user_info(new_dict)

def feed_creature(user_dict):
    print("Here are your creatures: ")
    print(user_dict['creatures'])

    creature = input("Which creature would you like to feed? ")
    food = input(f"What would you like to feed {creature}? Or enter N if you've changed your mind. (The creatures are very cute)")

    if food == 'N':
        display_user_info(user_dict)

    curr_friendliness = user_dict['creatures'][creature]['friendliness']
    creature_byproduct_price = user_dict['creatures'][creature]['byproduct']['price']
    creature_byproduct = user_dict['creatures'][creature]['byproduct']['name']

    userdoc_s = db.collection('users').document(user_dict['username'])
    if food in user_dict['creatures'][creature]['likes']:
        new_friendliness = curr_friendliness + 2
        userdoc_s.update({f'creatures.{creature}.friendliness' : new_friendliness})
        new_balance = user_dict['money'] + creature_byproduct_price
        userdoc_s.update({f'money' : new_balance})
        print(f"Yay! {creature} loves that food! They like you even more!")
        print(f"{creature} gave you a {creature_byproduct}! You sold it and gained {creature_byproduct_price} money!")
        userdoc_updated = db.collection('users').document(user_dict['username']).get()
        new_dict = userdoc_updated.to_dict()
        display_user_info(new_dict)
    elif food in user_dict['creatures'][creature]['dislikes']:
        new_friendliness = curr_friendliness - 2
        userdoc_s.update({f'creatures.{creature}.friendliness' : new_friendliness})
        print(f"Oh no! {creature} hates that food!")
        userdoc_updated = db.collection('users').document(user_dict['username']).get()
        new_dict = userdoc_updated.to_dict()
        display_user_info(new_dict)
    else:
        print(f"You fed your {creature} {food}.")
        display_user_info(user_dict)


def purchase_habitat(user_dict):
    print("Here are your habitats: ")
    print(user_dict['habitats'])

    all_habitat_names = get_habitat_names()
    avail_habitats = []

    print("Here are the available habitats for purchase: ")
    for elem in all_habitat_names:
        if elem in user_dict['habitats']:
            pass
        else:
            avail_habitats.append(elem)
    print(avail_habitats)

    new_habitat = input("What new habitat would you like to purchase? Enter N if you've changed your mind. ")

    if new_habitat == 'N':
        display_user_info(user_dict)
    
    # try:
    habitat = db.collection('habitats').document(new_habitat).get()
    doc = habitat.to_dict()
    if doc['price'] <= user_dict['money']:
            # Update user db
        userdoc = db.collection('users').document(user_dict['username'])
        userdoc.update({f'habitats' : firestore.ArrayUnion([habitat.id])})
        new_balance = user_dict['money'] - doc['price']
        userdoc.update({f'money' : new_balance})
        print("Gotcha!")
        userdoc_updated = db.collection('users').document(user_dict['username']).get()
        new_dict = userdoc_updated.to_dict()
        print("New Habitat!")
        print(new_dict['habitats'])
        display_user_info(new_dict)
    else:
        print("Not enough money!")
        display_user_info(user_dict)
    # except:
    #     print("Invalid habitat! Or something else happened. idk lol")
    #     purchase_habitat(user_dict)


def main():
    auth_user()

if __name__ == "__main__":
    main()


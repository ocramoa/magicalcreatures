import firebase_admin
from firebase_admin import firestore
# initialize app
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

# unused utility function -- print all users
def print_all_users():
    users_ref = db.collection('users')
    docs = users_ref.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

def new_user(username, password):
    """Creates a new user in the DB."""
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
    # We return the dictionary for other functions to use.
    return doc
    
def get_zoo_names():
    """Get the names of all the existing Magical Creatures."""
    animals = db.collection('zoo').select(field_paths=[]).stream()
    names = [item.id for item in animals]
    print(names)
    # return(names)

def get_habitat_names():
    """Get the names of all the existing Habitats."""
    habitats = db.collection('habitats').select(field_paths=[]).stream()
    names = [item.id for item in habitats]
    return names

def auth_user():
    """Authenticates the user and starts the main loop."""
    inp = input("Enter your username and password in this format: Username|Password, then hit enter. ")
    real_inp = inp.split('|')
    
    if len(real_inp) < 2 or len(real_inp) > 2:
        print("Invalid input. Try again.")
        auth_user()
    
    username = real_inp[0]
    password = real_inp[1]
    
    # Check if their username exists
    try:
        user = db.collection('users').document(username).get()
    except:
    # If the username doesn't exist, ask them if they want to add themselves as a user
        inp2 = input("Dang, it didn't work! Would you like to add yourself as a user? Y/N ")
        if inp2 == 'Y':
            new = new_user(username, password)
            print(f"There you go! Remember your username and password are: {username}, {password} ")
            # Main function
            display_user_info(new)
        else:
            print(':\'(')
    
    # Convert to dict before checking password
    userdoc = user.to_dict()
    
    # Check if valid password. If not rerun auth_user
    if userdoc['password'] == password:
        print("Gotcha!")
        now_go(userdoc)
    else:
        print("Invalid password.")
        auth_user()

def now_go(user_dict): # To be removed. Added while I was confused and debugging.
    display_user_info(user_dict)
    
def display_user_info(user_dict):
    """Main menu function -- root of decision tree. Asks the user what they want to do. All decisions return to this point."""
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
    """Purchase a creature."""
    print("Here are the available creatures: ")
    get_zoo_names()
    print(f"Your available funds are: {user_dict['money']}")
    prompt = input("What creature would you like to purchase? Enter the name or N if none. ")
    # Return back to main menu if they change their mind
    if prompt == 'N':
        display_user_info(user_dict)
    else:
            # Try block commented out for now while I debug
        # try:
            creature = db.collection('zoo').document(prompt).get()
            doc = creature.to_dict()
            # Do they have enough money?
            if doc['price'] <= user_dict['money']:
                # Update user db
                userdoc = db.collection('users').document(user_dict['username'])
                # Update the user's doc with the new creature
                userdoc.update({f'creatures.{creature.id}' : doc})
                # Store the new balance in a variable. If we don't do this, it breaks the DB with invalid data types.
                new_balance = user_dict['money'] - doc['price']
                # Update the user's balance.
                userdoc.update({f'money' : new_balance})
                print("Gotcha!")
                # Show the user their new creature. Then return to main menu.
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
    """Sell a creature."""
    print("Here are your creatures: ")
    print(user_dict['creatures'])
    
    prompt = input("Which creature would you like to sell? Enter N if none. ")

    if prompt == 'N':
        display_user_info(user_dict)
    
    else:
        # Follows a similar pattern as all the other purchase/sell functions.
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
    food = input(f"What would you like to feed {creature}? Or enter N if you've changed your mind. (The creatures are very cute) ")

    if food == 'N':
        display_user_info(user_dict)
    # We need to store the friendliness, the byproduct, and the price now so we don't break the DB.
    curr_friendliness = user_dict['creatures'][creature]['friendliness']
    creature_byproduct_price = user_dict['creatures'][creature]['byproduct']['price']
    creature_byproduct = user_dict['creatures'][creature]['byproduct']['name']
    # Access the user doc
    userdoc_s = db.collection('users').document(user_dict['username'])
    # If the creature likes the food, they become more friendly and they give the user something to sell
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
    # If the creature dislikes the food, they get less friendly.
    elif food in user_dict['creatures'][creature]['dislikes']:
        new_friendliness = curr_friendliness - 2
        userdoc_s.update({f'creatures.{creature}.friendliness' : new_friendliness})
        
        print(f"Oh no! {creature} hates that food!")
        
        userdoc_updated = db.collection('users').document(user_dict['username']).get()
        new_dict = userdoc_updated.to_dict()
        display_user_info(new_dict)
    # If the creature neither likes or dislikes the food, just print something lame out and return.
    else:
        print(f"You fed your {creature} {food}.")
        display_user_info(user_dict)


def purchase_habitat(user_dict):
    """Purchase a habitat that you don't own."""
    print("Here are your habitats: ")
    print(user_dict['habitats'])

    all_habitat_names = get_habitat_names()
    avail_habitats = []

    # Get the habitats the user does not have.
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
    
    # try: - Try block commented out for debugging
    habitat = db.collection('habitats').document(new_habitat).get()
    doc = habitat.to_dict()
    if doc['price'] <= user_dict['money']:
        userdoc = db.collection('users').document(user_dict['username'])
        # We have to use ArrayUnion because the habitats are stored as an array.
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

# Run the program.
def main():
    auth_user()

if __name__ == "__main__":
    main()


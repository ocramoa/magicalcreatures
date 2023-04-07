# Overview

This is a quick example of a Python project that integrates with Google Firestore. With the console application, you can purchase creatures and habitats. You can also feed your creatures or sell them.

Someone who is not me will not be able to use this program. However, if you want to create your own Firestore DB, it's free. Just install the Google Firebase SDK and authenticate yourself. Then, if you want to, copy my code and DB structure for a copy of this project.

The way I use this program is by starting client.py. It initializes a connection with the DB and then authenticates the user. After that, it has a menu where the user can decide what to do.

This isn't intended to be anything professional. Rather, it is a quick demonstration of how Python and Firestore can work together. Also, I really wanted to make a cute magical creatures app :smile:

[Software Demo Video](https://www.youtube.com/watch?v=4TFtah5hrbQ)

# Cloud Database

I am using Firestore for this project. I like it because of its collection/document/field structure. It makes it easy to read and write data.

If you want to, you could try redoing this project in a DB with a similar structure.

# Development Environment

I used VSCode, the online Firestore interface, and the Google SDK to make this project.

I used Python with the firebase_admin and firestore libraries.

# Useful Websites

- [Methods for Google Firestore Documents](https://cloud.google.com/python/docs/reference/firestore/latest/document)
- [Google Firestore Quickstart](https://firebase.google.com/docs/firestore/quickstart)
- [Create Client with Project ID](https://cloud.google.com/firestore/docs/samples/firestore-setup-client-create-with-project-id)

# Future Work

There's a lot of fields in the DB that are going unused. It would be good to add functionality to the project to support them.

- Creatures can be placed in habitats
- Creatures friendliness (basically happiness) changes based on where they are and who they are with
- The UI needs to be a bit cleaner
- Habitats should have a size limit for creatures inside of them
- It should be easier to feed your creatures
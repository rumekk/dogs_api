from enum import IntEnum
import webbrowser
import api_dogs

Menu = IntEnum('Menu', 'Get Show Add Delete Quit')
# print(list(Menu))
userId = '1'
random_doggo = None
number = 0

status = True
while status:
    try:
        choice = int(input("""Type: 1 - to get random picture,
      2 - to show your favourites,
      3 - to add picture to favourites,
      4 - to select picture to delete from favourites,
      5 - to quit. \nYour choice: """))

        if (choice == Menu.Get):
            random_doggo = api_dogs.get_random_doggo()
            # print(random_doggo)
            webbrowser.open_new_tab(random_doggo['url'])

        elif (choice == Menu.Show):
            favourite_dogs = api_dogs.get_favourites(userId)
            if favourite_dogs:
                valid_dogs = [
                    doggo for doggo in favourite_dogs
                    if doggo.get('image', {}).get('url') is not None
                ]
                if valid_dogs:
                    print('Your favourite images:')
                    for doggo in favourite_dogs:
                        doggo_id = doggo.get('id')
                        doggo_url = doggo.get('image', {}).get('url')
                        if doggo_id and doggo_url:
                            print(f'Image ID: {
                                  doggo_id}, image URL: {doggo_url}')
                else:
                    print('----- Favourites list is empty. -----')
            else:
                print('----- Favourites list is empty. -----')

        elif (choice == Menu.Add):
            if random_doggo is not None:
                api_dogs.add_to_favourites(random_doggo['id'], userId)
                print(f"Image {random_doggo['url']} added to favourites")
            else:
                print('----- You need to get a picture first. -----')

        elif choice == Menu.Delete:
            favourite_dogs = api_dogs.get_favourites(userId)
            if favourite_dogs:
                favDogsById = {str(dog.get('id')): dog.get('image', {}).get('url', 'No URL avaliable')
                               for dog in favourite_dogs}

                print('Your favourite images:')
                for doggo in favourite_dogs:
                    doggo_id = doggo.get('id')
                    doggo_url = doggo.get('image', {}).get('url')
                    if doggo_id and doggo_url:
                        print(f'Image ID: {doggo_id}, URL: {doggo_url}')

                idToRemove = input(
                    'Enter the ID of the image you want to delete: ')
                if idToRemove in favDogsById:
                    print(api_dogs.remove_from_favourites(userId, idToRemove))
                    print(f"Image with ID {
                          idToRemove} has been removed from favourites.")

                else:
                    print('----- No image found with that ID in favourites. -----')
            else:
                print('----- Favourites list is empty. -----')

        elif (choice == Menu.Quit):
            print('Bye!')
            status = False

        else:
            print('----- Incorrect value. -----')

    except ValueError:
        print('----- Enter a valid number. -----')

    except Exception as e:
        print(f'----- An error occured: {e} -----')

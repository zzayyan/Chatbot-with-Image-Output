import requests
import tkinter as tk
from PIL import Image, ImageTk
import flickrapi

# Set up Flickr API credentials
api_key = '6dd7c603e2d0f3687067307c465b1d08'
api_secret = '7a155e8eb65ce868'
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# Create GUI window
window = tk.Tk()
window.title('Flickr Image Search')

# Create text input field
query_entry = tk.Entry(window)
query_entry.pack()

# Create function to search for images and display them in the GUI
def search_images():
    # Get user's search query
    query = query_entry.get()
    
    # Search for images on Flickr
    results = flickr.photos.search(text=query, per_page=1)
    
    # Display images in GUI
    for photo in results['photos']['photo']:
        # Get image URL
        url = 'https://farm{}.staticflickr.com/{}/{}_{}.jpg'.format(photo['farm'], photo['server'], photo['id'], photo['secret'])
        
        # Load image from URL using PIL
        image = Image.open(requests.get(url, stream=True).raw)
        
        # Display image in GUI
        photo_image = ImageTk.PhotoImage(image)
        label = tk.Label(window, image=photo_image)
        label.image = photo_image
        label.pack()

# Create button to submit search query
search_button = tk.Button(window, text='Search', command=search_images)
search_button.pack()

# Run GUI window
window.mainloop()

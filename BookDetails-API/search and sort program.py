import pymongo

# Connect to your MongoDB server and database
client = pymongo.MongoClient("mongodb+srv://sss:123@cluster0.f0xb8zo.mongodb.net/")
db = client["bookstore"]
collection = db["books"]

def get_books_by_genre():
    genre = input("Enter a genre to search for books: ")  # Prompt for genre here    
    # Query the database for books with the specified genre
    books = collection.find({"genre": genre})

    # Convert the cursor to a list and get its length
    books_list = list(books)
    count = len(books_list)

    # Print the list of books
    if count > 0:
        print(f"Books in the '{genre}' genre:")
        for book in books_list:
            print(f"Title: {book['name']}")
            print(f"Author: {book['author']}")
            print(f"Publisher: {book['publisher']}")            
            print(f"Description: {book['desc']}")
            print(f"Price: ${book['priceUSD']:.2f}")
            print(f"Discount: {book.get('discount')}%")
            print(f"Rating: {book.get('rating')}")
            print(f"Sold: {book.get('numSold')}")   
            print("-----------")
    else:
        print(f"No books found in the '{genre}' genre.")

def get_books_by_rating():
    min_rating = float(input("Enter the minimum book rating you are willing to read: "))
    # Query the database for books with ratings greater than or equal to min_rating
    books = collection.find({"rating": {"$gte": min_rating}})

    # Convert the cursor to a list
    books_list = list(books)

    # Print the list of books
    if books_list:
        print(f"Books with a rating greater than or equal to {min_rating}:")
        for book in books_list:
            print(f"Title: {book['name']}")
            print(f"Author: {book['author']}")
            print(f"Publisher: {book['publisher']}")            
            print(f"Description: {book['desc']}")
            print(f"Price: ${book['priceUSD']:.2f}")
            print(f"Discount: {book.get('discount')}%")
            print(f"Rating: {book.get('rating')}")
            print(f"Sold: {book.get('numSold')}")   
            print("-----------")
    else:
        print(f"No books found with a rating greater than or equal to {min_rating}.")

def get_books_by_author_and_discount():
    author = input("Enter the author's name: ")
    min_discount = float(input("Enter the minimum discount: "))
    # Query the database for books by the specified author with a discount greater than or equal to min_discount
    books = collection.find({"author": author, "discount": {"$gte": min_discount}})
    
    # Convert the cursor to a list
    books_list = list(books)

    if not books_list:
        print(f"No books found by {author} with a discount greater than or equal to {min_discount}.")
        return
    
    # Print the list of books
    if books_list:
        print(f"Books by {author} with a discount greater than or equal to {min_discount}:")
        for book in books_list:
            print(f"Title: {book['name']}")
            print(f"Author: {book['author']}")
            print(f"Publisher: {book['publisher']}")            
            print(f"Description: {book['desc']}")
            print(f"Price: ${book['priceUSD']:.2f}")
            print(f"Discount: {book.get('discount')}%")
            print(f"Rating: {book.get('rating')}")
            print(f"Sold: {book.get('numSold')}")   
            print("-----------")
    else:
        print(f"No books found by {author} with a discount greater than or equal to {min_discount}.")

def get_books_by_publisher_and_discount():
    publisher = input("Enter the publisher's name: ")
    min_discount = float(input("Enter the minimum discount: "))

    # Query the database for books by the specified publisher with a discount greater than or equal to min_discount
    books = collection.find({"publisher": publisher, "discount": {"$gte": min_discount}})
    
    # Convert the cursor to a list
    books_list = list(books)

    if not books_list:
        print(f"No books found by {publisher} with a discount greater than or equal to {min_discount}.")
        return

    # Print the list of books
    if books_list:
        print(f"Books by {publisher} with a discount greater than or equal to {min_discount + 0.01}:")
        for book in books_list:
            print(f"Title: {book['name']}")
            print(f"Author: {book['author']}")
            print(f"Publisher: {book['publisher']}")            
            print(f"Description: {book['desc']}")
            print(f"Price: ${book['priceUSD']:.2f}")
            print(f"Discount: {book.get('discount')}%")
            print(f"Rating: {book.get('rating')}")
            print(f"Sold: {book.get('numSold')}")   
            print("-----------")

def get_top_10_most_sold_books():
    # Query the database for all books and sort them by the number of books sold in descending order
    books = collection.find().sort("numSold", pymongo.DESCENDING).limit(10)
    
    # Convert the cursor to a list
    books_list = list(books)
    
    if not books_list:
        print("No books found.")
        return
    
    # Print the top 10 most sold books
    print("Top 10 Most Sold Books:")
    for book in books_list:
            print(f"Title: {book['name']}")
            print(f"Author: {book['author']}")  
            print(f"Publisher: {book['publisher']}")            
            print(f"Description: {book['desc']}")
            print(f"Price: ${book['priceUSD']:.2f}")
            print(f"Discount: {book.get('discount')}%")
            print(f"Rating: {book.get('rating')}")
            print(f"Sold: {book.get('numSold')}")   
            print("-----------")


def update_discount_by_author():
    author = input("Enter the author's name: ")
    new_discount = float(input("Enter the new discount value: "))

    # Update discounts for books by the specified authorclear
    update_result = collection.update_many(
        {"author": author},
        {"$set": {"discount": new_discount}}
    )

    if update_result.modified_count > 0:
        print(f"Discounts updated for books by {author}.")
    else:
        print(f"No books found by {author} to update discounts.")

def main():
    while True:
        search_option = input("What would you like to search by? (type 'genre' to search by genre, 'author' to search by author and by discount, 'publisher' to search by publisher and by discount, 'rating' to search by rating, 'most_sold' to search for the top 10 most sold books, 'exit' to quit): ")
        
        if search_option == 'genre':
            get_books_by_genre()
        elif search_option == 'rating':
            get_books_by_rating()
        elif search_option == 'author':
            get_books_by_author_and_discount()
        elif search_option == 'publisher':
            get_books_by_publisher_and_discount() 
        elif search_option == 'most_sold':
            get_top_10_most_sold_books()   
        elif search_option == 'update_discount':
            update_discount_by_author()
        elif search_option == 'exit':
            break
        else:
            print("Invalid option. Please enter 'genre', 'author', 'rating', 'publisher', 'most_sold' or 'exit'.")

if __name__ == "__main__":
    main()

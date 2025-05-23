from graphene import ObjectType, String, List, Field, Schema, Mutation, Boolean

# In-memory data store for books
books_data = [
    {"title": "1984", "author": "George Orwell"},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
]

#
# 1) GraphQL Book type
#
class Book(ObjectType):
    title = String()
    author = String()


#
# 2) Query class
#
class Query(ObjectType):
    """
    Defines two fields:
      - book(title): returns a single Book
      - books: returns a list of all books
    """

    book = Field(Book, title=String(required=True))
    books = List(Book)

    def resolve_book(root, info, title):
        # Return the first matching book or None
        for b in books_data:
            if b["title"] == title:
                return Book(title=b["title"], author=b["author"])
        return None

    def resolve_books(root, info):
        return [
            Book(title=b["title"], author=b["author"]) for b in books_data
        ]

#
# 3A) Mutation to add a new book
#
class AddBook(Mutation):
    class Arguments:
        title = String(required=True)
        author = String(required=True)

    success = Boolean()
    book = Field(Book)

    def mutate(root, info, title, author):
        # Add the new book to our in-memory data
        new_entry = {"title": title, "author": author}
        books_data.append(new_entry)
        print('books data')

        # Return the mutation result
        return AddBook(
            success=True,
            book=Book(title=title, author=author)
        )

#
# 4B) Mutation to remove a book
#
class RemoveBook(Mutation):
    class Arguments:
        title = String(required=True)

    success = Boolean()
    book = Field(Book)

    def mutate(root, info, title):
        # Remove the book from our in-memory data
        for b in books_data:
            if b["title"] == title:
                books_data.remove(b)
                break

        # Return the mutation result
        return RemoveBook(
            success=True,
            book=Book(title=title)
        )



#
# 4) Mutation class (can contain multiple mutations)
#
class Mutation(ObjectType):
    add_book = AddBook.Field() #addBook
    remove_book = RemoveBook.Field() #removeBook


#
# 5) Build the GraphQL schema
#
schema = Schema(query=Query, mutation=Mutation)


if __name__ == "__main__":
    # A1) Query all books
    query_all = """
    {
      books {
        title
        author
      }
    }
    """
    result_all = schema.execute(query_all)
    print("\nInitial Books Query:\n", result_all.data)

    # A2) Query A Book
    query_book = """
    {
      book(title: "The Great Gatsby") {
        title
        author
      }
    }
    """
    result_book = schema.execute(query_book)
    print("\nFind A Book Query:\n", result_book.data)

    # B) Mutation: Add a new Book
    mutation_add = """
    mutation {
      addBook(title: "Dune", author: "Frank Herbert") {
        success
        book {
          title
          author
        }
      }
    }
    """
    result_mutation = schema.execute(mutation_add)
    print("\nAdd Book Mutation:\n", result_mutation.data)

    # C) Query again to confirm the new book was added
    result_all_after = schema.execute(query_all)
    print("\nBooks After Mutation:\n", result_all_after.data)

    # D) Mutation: Remove a book
    mutation_remove = """
    mutation {
      removeBook(title: "The Great Gatsby") {
        success
        book {
          title
          author
        }
      }
    }
    """
    result_mutation = schema.execute(mutation_remove)
    print("\nRemove Book Mutation:\n", result_mutation.data)

    # E) Query again to confirm the book was removed
    result_all_after = schema.execute(query_all)
    print("\nBooks After Mutation:\n", result_all_after.data)
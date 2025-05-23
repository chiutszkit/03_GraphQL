from graphene import ObjectType, String, List, Field, Schema, Mutation, Boolean

# Sample in-memory to-do list
todos_data = [
    {"id": 1, "task": "Learn Flask", "done": False},
    {"id": 2, "task": "Build a REST API", "done": False},
    {"id": 3, "task": "Test the API", "done": False},
    {"id": 4, "task": "Watch another course from Kesha", "done": False}
]

next_todo_id = len(todos_data) + 1

#
# 1) GraphQL Book type
#
class Todo(ObjectType):
    id = String()
    task = String()
    done = Boolean()

#
# 2) Query class
#
class Query(ObjectType):
    """
    Defines three fields:
      - todoItem(task): returns a single To-Do Task
      - todos: returns a list of To-Do Tasks
    """

    todo = Field(Todo, task=String(required=True)) #Use Camel Case
    todos = List(Todo)

    def resolve_todo(root, info, task):
        # Return the first matching book or None
        for t in todos_data:
            if t["task"] == task:
                return Todo(task=t["task"], done=t["done"], id=t["id"])
        return None

    def resolve_todos(root, info):
        return [
            Todo(task=t["task"], done=t["done"], id=t["id"]) for t in todos_data
        ]

#
# 3A) Mutation to add a new Todo item
#
class AddTodo(Mutation):
    class Arguments:
        task = String(required=True)

    success = Boolean()
    todo = Field(Todo)

    def mutate(root, info, task):
        global next_todo_id

        # Add the new book to our in-memory data
        new_entry = {"task": task, "done": False, "id": next_todo_id}
        todos_data.append(new_entry)
        next_todo_id += 1

        # Return the mutation result
        return AddTodo(
            success=True,
            todo=Todo(task=task, done=False, id=new_entry["id"])
        )

#
# 4B) Mutation to remove a book
#
class RemoveToDo(Mutation):
    class Arguments:
        task = String(required=True)

    success = Boolean()
    todo = Field(Todo)

    def mutate(root, info, task):
        # Remove the book from our in-memory data
        for t in todos_data:
            if t["task"] == task:
                todos_data.remove(t)
                break

        # Return the mutation result
        return RemoveToDo(
            success=True,
            todo=Todo(task=task)
        )
    
class UpdateTodo(Mutation):
    class Arguments:
        task = String(required=True)
        newTask = String()
        done = Boolean()

    success = Boolean()
    todo = Field(Todo)

    def mutate(root, info, task, newTask=None, done=None):
        updated_entry = None
        # Mark done to a todo item
        for t in todos_data:
            if t["task"] == task:
                if newTask is not None:
                  t["task"] = newTask
                if done is not None:
                  t["done"] = done
                updated_entry = t
                break

        # Return the mutation result
        if updated_entry is None:
          return UpdateTodo(
              success=False,
          )
        else:
          return UpdateTodo(
              success=True,
              todo=Todo(task=updated_entry["task"], done=updated_entry["done"], id=updated_entry["id"])
          )



#
# 4) Mutation class (can contain multiple mutations)
#
class Mutation(ObjectType):
    add_todo = AddTodo.Field() #addTodo
    remove_todo = RemoveToDo.Field() #removeTodo
    update_todo = UpdateTodo.Field() #updateTodo


#
# 5) Build the GraphQL schema
#
schema = Schema(query=Query, mutation=Mutation)


if __name__ == "__main__":
    # A1) Query all todos
    query_all = """
    {
      todos {
        id
        task
        done
      }
    }
    """
    result_all = schema.execute(query_all)
    print("\nInitial Todos Query:\n", result_all.data)

    # A2) Query a todo item
    query_item = """
    {
      todo(task: "Learn Flask") {
        id
        task
        done
      }
    }
    """
    result_item = schema.execute(query_item)
    print("\nFind A Todo Query:\n", result_item.data)

    # B) Mutation: Add a new Todo
    mutation_add = """
    mutation {
      addTodo(task: "House Cleaning") {
        success
        todo {
          id
          task
        }
      }
    }
    """
    result_mutation = schema.execute(mutation_add)
    print("\nAdd Todo Mutation:\n", result_mutation.data.get("addTodo"))

    # C) Query again to confirm the new todo item was added
    result_all_after = schema.execute(query_all)
    print("\nTodos After Mutation:\n", result_all_after.data)

    # D) Mutation: Remove a todo item
    mutation_remove = """
    mutation {
      removeTodo(task: "Learn Flask") {
        success
      }
    }
    """
    result_mutation = schema.execute(mutation_remove)
    print("\nRemove Todo Mutation:\n", result_mutation.data)

    # E) Query again to confirm the todo item was removed
    result_all_after = schema.execute(query_all)
    print("\nTodos After Mutation:\n", result_all_after.data)

    # F) Mutation: Update a todo item
    mutation_update = """
    mutation {
      updateTodo(task: "Car Cleaning", done: true) {
        success
        todo {
          id
          task
          done
        }
      }
    }
    """
    result_mutation = schema.execute(mutation_update)
    print("\nUpdate Todo Mutation:\n", result_mutation.data)

    # G) Query again to confirm the todo item was updated
    result_all_after = schema.execute(query_all)
    print("\nTodos After Mutation:\n", result_all_after.data)
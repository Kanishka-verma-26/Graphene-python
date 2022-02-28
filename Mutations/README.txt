MUTATION

With Graphene-Django we can take advantage of pre-existing Django features to quickly build CRUD functionality, while still
using the core graphene mutation features to add custom mutations to a Django project.

1) Simple Example

            * create model, register, migrate

                            """"
                                class Category(models.Model):
                                    topic = models.CharField(max_length=250)

                                    def __str__(self):
                                        return self.topic
                            """"

            * write schema

                            """"
                                class CategoryType(DjangoObjectType):
                                    class Meta:
                                        model = Category
                                        fields = ("topic",)
                            """"

            * add mutations

                        ( adding new Category )

                                    """"
                                        class CategoryMutationAdd(graphene.Mutation):
                                            class Arguments:
                                                topic = graphene.String(required=True)       # passing all the arguments present in the
                                                                                                        particular model to fetch data
                                            category = graphene.Field(CategoryType)         # connecting to the schema field

                                            @classmethod
                                            def mutate(cls, root,info,topic):
                                                category = Category(topic=topic)
                                                category.save()                             # saving new category
                                                return CategoryMutationAdd(category=category)
                                    """"

                        ( updating existing elements in the Category Field )

                                    """"
                                        class CategoryMutationUpdate(graphene.Mutation):
                                            class Arguments:
                                                id = graphene.ID()
                                                topic = graphene.String(required=True)

                                            category = graphene.Field(CategoryType)

                                            @classmethod
                                            def mutate(cls,root,info,topic,id):
                                                category = Category.objects.get(pk=id)
                                                category.topic = topic
                                                category.save()

                                                return CategoryMutationUpdate(category=category)
                                    """"

            * register your mutations

                             """"
                                class Mutation(graphene.ObjectType):
                                    add_category = CategoryMutationAdd.Field()
                                    update_category = CategoryMutationUpdate.Field()
                             """"


                ( run query to add category )

                            """"
                                mutation
                                    {
                                      addCategory(topic:"<category_name>"){
                                        category{
                                          topic
                                          id
                                        }
                                      }
                                    }
                            """"

                ( run query to update category )
                            """"
                                mutation{
                                  updateCategory(id:4,topic:"laguages"){
                                    category{
                                      topic
                                    }
                                  }
                                }
                            """"

2) Django Forms

            * DjangoFormMutation ( without model )

                            Graphene-Django comes with mutation classes that will convert the
                            fields on Django forms into inputs on a mutation.

                                    """"
                                        from graphene_django.forms.mutation import DjangoFormMutation

                                            class MyForm(forms.Form):
                                                name = forms.CharField()

                                            class MyMutation(DjangoFormMutation):
                                                class Meta:
                                                    form_class = MyForm
                                    """"


                            ( "MyMutation" will automatically receive an input argument. This argument should be a "dict" where
                            the key is "name" and the value is a string.)


                            * create mutation object
                                       'django_form_mutation_MyForm = MyMutation.Field()''


                             Note: but this will require a save attribute for form

                                    ( query : )

                                            """"
                                                 mutation{
                                                    djangoFormMutationMyform(input:{name:"Meow",}) {
                                                      name
                                                    }
                                                  }
                                            """"

            * DjangoModelFormMutation ( with model )

                            "DjangoModelFormMutation" will pull the fields from a "ModelForm".

                            1) create model
                                        """"
                                            class Pet(models.Model):
                                                name = models.CharField(max_length=100)

                                                def __str__(self):
                                                    return self.name
                                        """"

                            2) create form
                                        """"
                                            class PetForm(forms.ModelForm):
                                                class Meta:
                                                    model = Pet
                                                    fields = ("name",)
                                        """"

                            3) write schema
                                        """"
                                            class PetType(DjangoObjectType):
                                                class Meta:
                                                    model = Pet
                                        """"

                            4) write mutation
                                        """"
                                            class PetMutation(DjangoModelFormMutation):
                                                pet = (PetType)
                                                class Meta:
                                                    form_class = PetForm
                                        """"
                            5) create mutation object
                                        ' django_form_mutation_PetForm = PetMutation.Field() '


                            (( "PetMutation" will grab the fields from "PetForm" and turn them into inputs.
                                If the form is valid then the mutation will lookup the "DjangoObjectType" for the "Pet" model and
                                return that under the key "pet". Otherwise it will return a list of errors. ))



                            ( run query to create new object of Pet )
                                        """"
                                             mutation{
                                                djangoFormMutationPetform(input:{name:"Meow",}) {
                                                pet{
                                                  name
                                                }
                                              }
                                            }
                                        """"

                            You can change the "input" name (default is input) and the return field name (default is the model name lowercase).

                                        """"
                                            class PetMutation(DjangoModelFormMutation):
                                                class Meta:
                                                    form_class = PetForm
                                                    input_field_name = 'data'
                                                    return_field_name = 'my_pet'
                                        """"


            * Form Validation

                             Form mutations will call "is_valid()" on your forms.

                             If the form is valid then the class method "perform_mutate(form, info)" is called on the mutation.
                              Override this method to change how the form is saved or to return a different Graphene object type.

                             If the form is not valid then a list of errors will be returned. These errors have two fields:
                             field, a string containing the name of the invalid form field, and "messages", a list of strings with the validation messages.



3) Django REST Framework
            Django DRF is a package that allow us to convert our application into an API ( for  example in this project
            next js can access the data in the database through django )

            * create model, register ( we are using Product model for DRF )

            * Configure DRF

                             1) pip install djangorestframework
                             2) add 'rest_framework' into INSTALLED_APPS
                             3) give permission for accessing information, add the below in settings.py

                                             REST_FRAMEWORK = {
                                                     'DEFAULT_PERMISSION_CLASSES': [
                                                         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
                                                     ]
                                                 }

            * set URLS

            * define Views  ( refer 'ProductDRFListView' and 'ProductDRF' )

            * define Serializers    (refer ProductSerializer)

            (You can re-use your Django Rest Framework serializer with Graphene Django mutations.)

            You can create a Mutation based on a serializer by using the SerializerMutation base class:

                            example : """"
                                          from graphene_django.rest_framework.mutation import SerializerMutation

                                          class MyProductMutation(SerializerMutation):
                                              class Meta:
                                                  serializer_class = ProductSerializer
                                      """"

            3.1) Create/Update Operations

                            By default ModelSerializers accept create and update operations. To customize this use the
                             model_operations attribute on the "SerializerMutation" class.

                            The update operation looks up models by the primary key by default. You can customize the
                            look up with the "lookup_field" attribute on the "SerializerMutation" class.

                                """"
                                    class MyProductMutation(SerializerMutation):
                                        class Meta:
                                            serializer_class = ProductSerializer
                                            model_operations = ['create', 'update']
                                            lookup_field = 'id'
                                """"

                            * ( CREATE QUERY )

                                        """"
                                            mutation{
                                                 myProductMutation(input: {category: "accessory",title:"ring",
                                                                            slug:"ring",description:"a small rounded metal",
                                                                            regularPrice:399,discountPrice:299}){
                                                  id
                                                  title
                                                  category
                                                  slug
                                                  errors{
                                                      field
                                                      messages
                                                    }
                                                  }
                                                }
                                        """"

                            * ( UPDATE QUERY ( update query and create query are same but in updation u need to paas id
                                along with all fields ))

                                        """"
                                            mutation{
                                              myProductMutation(input: {id:7, category: "How to heal my burn wound?",
                                                                    slug:"ring",regularPrice:399,discountPrice:200,
                                                                    title:"hello"}){
                                                id
                                                category
                                                title
                                                regularPrice
                                                discountPrice
                                                slug
                                              }
                                            }
                                        """"

            3.2) Overriding Update Queries

                            Use the method "get_serializer_kwargs" to override how updates are applied.

                                            """"
                                                class MyProductMutationOverriding(SerializerMutation):
                                                    class Meta:
                                                        serializer_class = ProductSerializer

                                                    @classmethod
                                                    def get_serializer_kwargs(cls, root, info, **input):
                                                        if 'id' in input:
                                                            instance = Product.objects.filter(
                                                                id=input['id'],
                                                            ).first()
                                                            if instance:
                                                                return {'instance': instance, 'data': input, 'partial': True}

                                                            else:
                                                                raise http.Http404

                                                        return {'data': input, 'partial': True}
                                            """"

                                      (run query)
                                            """"
                                                mutation{
                                                     myProductMutationOverriding(input:{id:2,slug:"abc",
                                                                    category:"xyz",regularPrice:120,title:"kjchdw",discountPrice:111}){
                                                        category
                                                      }
                                                    }
                                            """"

4) Relay (similar to add new category class)

            Most APIs don’t just allow you to read data, they also allow you to write.

            In GraphQL, this is done using mutations. Just like queries, Relay puts some additional requirements on mutations,
             but Graphene nicely manages that for you. All you need to do is make your mutation a subclass of "relay.ClientIDMutation".

            You can use relay with mutations. A Relay mutation must inherit from "ClientIDMutation" and implement
            the "mutate_and_get_payload" method:

                            """"
                                from graphene import relay
                                from graphql_relay import from_global_id

                                class CategoryRelay(relay.ClientIDMutation):
                                    class Input:
                                        topic = graphene.String(required=True)
                                        id = graphene.ID()

                                    category = graphene.Field(CategoryType)

                                    @classmethod
                                    def mutate_and_get_payload(cls, root,info,topic,id):
                                        category = Category.objects.get(pk=from_global_id(id)[1])
                                        category.topic=topic
                                        category.save()
                                        return CategoryMutationAdd(category=category)
                            """"

            Notice that the "class Arguments" is renamed to "class Input" with relay. This is due to a deprecation of class
             Arguments in graphene 2.0.

            Relay ClientIDMutation accept a "clientIDMutation" argument. This argument is also sent back to the client with the
            mutation result (you do not have to do anything). For services that manage a pool of many GraphQL requests in bulk,
            the "clientIDMutation" allows you to match up a specific mutation with the response.






5) Accepting Files

            Mutations can also accept files, that’s how it will work with different integrations:

            """"
                class UploadFile(graphene.ClientIDMutation):
                     class Input:
                         pass                               # nothing needed for uploading file

                     # your return fields
                     success = graphene.String()

                    @classmethod
                    def mutate_and_get_payload(cls, root, info, **input):
                        files = info.context.FILES              # When using it in Django, context will be the request

                        # Or, if used in Flask, context will be the flask global request
                        # files = context.files

                        # do something with files

                        return UploadFile(success=True)
            """"


6) Django Database Transactions

            Django gives you a few ways to control how database transactions are managed.

            * Tying transactions to HTTP requests

                        A common way to handle transactions in Django is to wrap each request in a transaction.
                        Set "ATOMIC_REQUESTS" settings to "True" in the configuration of each database for which you want
                        to enable this behavior.

                        It works like this. Before calling "GraphQLView" Django starts a transaction. If the response is
                        produced without problems, Django commits the transaction. If the view, a "DjangoFormMutation" or a
                        "DjangoModelFormMutation" produces an exception, Django rolls back the transaction.

                        WARNING

                        While the simplicity of this transaction model is appealing, it also makes it inefficient when traffic
                        increases. Opening a transaction for every request has some overhead. The impact on performance depends
                        on the query patterns of your application and on how well your database handles locking.


                        ( Check the next section for a better solution. )

            * Tying transactions to mutations

                        A mutation can contain multiple fields, just like a query. There’s one important distinction between
                        queries and mutations, other than the name:

                                  " While query fields are executed in parallel, mutation fields run in series, one after the other. "

                        This means that if we send two "incrementCredits" mutations in one request, the first is guaranteed to
                        finish before the second begins, ensuring that we don’t end up with a race condition with ourselves.

                        On the other hand, if the first "incrementCredits" runs successfully but the second one does not, the
                        operation cannot be retried as it is. That’s why is a good idea to run all mutation fields in a transaction,
                        to guarantee all occur or nothing occurs.

                        To enable this behavior for all databases set the graphene "ATOMIC_MUTATIONS" settings to "True" in your settings file:

                                    """"
                                        GRAPHENE = {
                                            "ATOMIC_MUTATIONS": True,
                                        }
                                    """"

                        On the contrary, if you want to enable this behavior for a specific database, set "ATOMIC_MUTATIONS" to "True"
                         in your database settings:

                                    """"
                                        DATABASES = {
                                            "default": {
                                                "ATOMIC_MUTATIONS": True,
                                            },
                                        }
                                    """"

                         Now, given the following example mutation:

                                    """"
                                        mutation IncreaseCreditsTwice {

                                            increaseCredits1: increaseCredits(input: { amount: 10 }) {
                                                balance
                                                errors {
                                                    field
                                                    messages
                                                }
                                            }

                                            increaseCredits2: increaseCredits(input: { amount: -1 }) {
                                                balance
                                                errors {
                                                    field
                                                    messages
                                                }
                                            }

                                        }
                                    """"

                         The server is going to return something like:

                                    """"
                                        {
                                            "data": {
                                                "increaseCredits1": {
                                                    "balance": 10.0,
                                                    "errors": []
                                                },
                                                "increaseCredits2": {
                                                    "balance": null,
                                                    "errors": [
                                                        {
                                                            "field": "amount",
                                                            "message": "Amount should be a positive number"
                                                        }
                                                    ]
                                                },
                                            }
                                        }
                                    """"

                         But the balance will remain the same.






-----------------------------------------------------------------------------------------------------------------------------------

SUBSCRIPTIONS

           The "graphene-django" project does not currently support GraphQL subscriptions out of the box. However, there are
           several community-driven modules for adding subscription support, and the provided GraphiQL interface supports
           running subscription operations over a websocket.


           To implement websocket-based support for GraphQL subscriptions, you’ll need to do the following:

                        1) Install and configure django-channels.
                        2) Install and configure* a third-party module for adding subscription support over websockets.
                            A few options include:

                                        * graphql-python/graphql-ws
                                        * datavance/django-channels-graphql-ws
                                        * jaydenwindle/graphene-subscriptions

                        3) Ensure that your application (or at least your GraphQL endpoint) is being served via an ASGI protocol
                        server like 'daphne' (built in to django-channels), 'uvicorn', or 'hypercorn'.

                        * Note: By default, the GraphiQL interface that comes with graphene-django assumes that you are handling
                        subscriptions at the same path as any other operation (i.e., you configured both urls.py and routing.py to handle
                        GraphQL operations at the same path, like /graphql).

                        If these URLs differ, GraphiQL will try to run your subscription over HTTP, which will produce an error.
                        If you need to use a different URL for handling websocket connections, you can configure "SUBSCRIPTION_PATH"
                         in your settings.py:

                                    """"
                                        GRAPHENE = {
                                            # ...
                                            "SUBSCRIPTION_PATH": "/ws/graphql"  # The path you configured in `routing.py`, including a leading slash.
                                        }
                                    """"


                         Once your application is properly configured to handle subscriptions, you can use the GraphiQL interface to test subscriptions like any other operation.






















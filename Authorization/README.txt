1) Basic setup

                * sudo apt-get install python
                * activate virtualenv
                * create project and app; register app
                * pip install graphene-django; register 'graphene_django'
                * setup urls and add GRAPHENE for schema path in settings.py
                * write models, register and create schema file

                        """"
                            from graphene import relay
                            import graphene
                            from graphene import ObjectType
                            from graphene_django.filter import DjangoFilterConnectionField
                            from graphene_django.types import DjangoObjectType
                            from .models import Post

                            """ schema to print all posts that got published """
                            class PostNode(DjangoObjectType):
                                class Meta:
                                    model = Post
                                    fields = '__all__'
                                    interfaces = (relay.Node, )
                                    filter_fields = ["title", "content"]


                            class Query(ObjectType):
                                all_posts = DjangoFilterConnectionField(PostNode)

                                def resolve_all_posts(self, info):
                                     return Post.objects.filter(published=True)

                            schema = graphene.Schema(query=Query)
                        """"

                ( query to print all posts i.e. published)
                        """"
                            query{
                              allPosts{
                                edges{
                                  node{
                                    title
                                    content
                                    published

                                  }
                                }
                              }
                            }
                        """"


2) User-based Queryset Filtering  ( you can only access this if you are a superuser )

                If you are using 'GraphQLView' you can access Django’s request with the context argument.

                            """"
                                from graphene import ObjectType
                                from graphene_django.filter import DjangoFilterConnectionField
                                from .models import Post

                                class Query(ObjectType):
                                    my_posts = DjangoFilterConnectionField(PostNode)

                                    def resolve_my_posts(self, info):
                                        # context will reference to the Django request
                                        if not info.context.user.is_authenticated:
                                            return Post.objects.none()
                                        else:
                                            return Post.objects.filter(owner=info.context.user)
                            """"


                If you’re using your own view, passing the request context into the schema is simple.
                ( didnt worked for me so i used the basic LOC i.e. 'schema = graphene.Schema(query=Query)' )

                            " result = schema.execute(query, context_value=request) "


                ( query to printout all of the posts of current loggedin superuser )

                        """"
                            query{
                              myPosts{
                                edges{
                                  node{
                                    title
                                    id
                                    content
                                    published
                                  }
                                }
                              }
                            }
                        """"

3) Global Filtering

                If you are using 'DjangoObjectType' you can define a custom 'get_queryset'.

                        """"
                            class PostNodeGlobalFiltering(DjangoObjectType):
                                class Meta:
                                    model = Post

                                @classmethod
                                def get_queryset(cls,queryset,info):
                                    if info.context.user.is_anonymous:              # we are returning all posts for anonymous  user
                                        return queryset.filter(published=True)
                                    return queryset
                        """"

                ( query to return all objects )

                        """"
                            query{
                              allPostsGlobalFiltering{
                                edges{
                                  node{
                                    title
                                    id
                                    content
                                    published
                                  }
                                }
                              }
                            }
                        """"


4) Filtering ID-based Node Access

                ( this will print all of the published posts of a logged in superuser and can access a particular post by
                defining id in float data type (the user can access only their posts ))

                In order to add authorization to id-based node access, we need to add a method to your "DjangoObjectType".

                * schema

                        """"
                            class PostIDBasedNodeAccess(DjangoObjectType):
                                class Meta:
                                    model = Post
                                    fields = '__all__'
                                    interfaces = (relay.Node,)
                                    filter_fields = ["title", "content","id"]
                        """"

                * query

                        """"
                            post_ID_based_node_access = DjangoFilterConnectionField(PostIDBasedNodeAccess)

                            def resolve_post_ID_based_node_access(self,info,**kwargs):
                                print("inside def")
                                print(kwargs)
                                id = kwargs.get('id')

                                if info.context.user.is_authenticated:
                                    return Post.objects.filter(owner=info.context.user,published=True)
                                return None
                        """"

                (run query for all posts)
                        """"
                            query{
                              postIdBasedNodeAccess{
                                edges{
                                  node{
                                    id
                                    content
                                    title
                                    published
                                  }
                                }
                              }
                            }
                        """"

                ( run query for a particular user's post )
                        """"
                            query{
                              postIdBasedNodeAccess(id:1){
                                edges{
                                  node{
                                    id
                                    content
                                    title
                                    published
                                  }
                                }
                              }
                            }
                        """"


5) Adding Login Required

                To restrict users from accessing the GraphQL API page the standard Django "LoginRequiredMixin" can be used
                to create your own standard Django Class Based View, which includes the "LoginRequiredMixin" and subclasses
                the "GraphQLView".

                ( this will restrict user to access graphql site if user is not logged into admin ste )


                * app/views.py

                            """"
                                from django.contrib.auth.mixins import LoginRequiredMixin
                                from graphene_django.views import GraphQLView

                                class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
                                    pass
                            """"

                * update url

                            """ path("graphql",PrivateGraphQLView.as_view(graphiql=True)), """

                            or

                            """ path('graphql', PrivateGraphQLView.as_view(graphiql=True, schema=schema)), """










********************************************* Django Debug Middleware ************************************************

You can debug your GraphQL queries in a similar way to django-debug-toolbar, but outputting in the results in GraphQL response
as fields, instead of the graphical HTML interface.

For that, you will need to add the plugin in your graphene schema.

* Installation

            For use the Django Debug plugin in Graphene:

            1) Add "graphene_django.debug.DjangoDebugMiddleware" into 'MIDDLEWARE' in the 'GRAPHENE' settings.

                        """"
                            GRAPHENE = {
                                ...
                                'MIDDLEWARE': [
                                    'graphene_django.debug.DjangoDebugMiddleware',
                                ]
                            }
                        """"

            2) Add the "debug" field into the schema root "Query" with the value "graphene.Field(DjangoDebug, name='_debug')".

                        """"
                            from graphene_django.debug import DjangoDebug

                            class Query(graphene.ObjectType):
                                # ...
                                debug = graphene.Field(DjangoDebug, name='_debug')

                            schema = graphene.Schema(query=Query)
                        """"


* Querying

                You can query it for outputting all the sql transactions that happened in the GraphQL request, like:

                        """"
                            query{
                              allPosts{                       # A example that will use the ORM for interact with the DB
                                edges{
                                  node{
                                    id
                                    title
                                    content
                                    published
                                  }
                                }
                              }

                              _debug{                             # Here is the debug field that will output the SQL queries
                                sql{
                                  rawSql
                                  startTime
                                  isSelect
                                }
                              }
                            }
                        """"

                * Note that the _debug field must be the last field in your query.







******************************************* Settings *************************************************




Graphene-Django can be customised using settings. This page explains each setting and their defaults.

* Usage

            Add settings to your Django project by creating a Dictonary with name "GRAPHENE" in the project’s "settings.py":

                    """"
                        GRAPHENE = {
                            ...
                        }
                    """"

* SCHEMA

            The location of the top-level 'Schema' class; Default: "None"

                    """"
                        GRAPHENE = {
                            'SCHEMA': 'path.to.schema.schema',
                        }
                    """"

* SCHEMA_OUTPUT

            The name of the file where the GraphQL schema output will go; Default: "schema.json"

                    """"
                        GRAPHENE = {
                            'SCHEMA_OUTPUT': 'schema.json',
                        }
                    """"

* SCHEMA_INDENT

            The indentation level of the schema output; Default:2

                    """"
                        GRAPHENE = {
                            'SCHEMA_INDENT': 2,
                        }
                    """"

* MIDDLEWARE

            A tuple of middleware that will be executed for each GraphQL query. See the middleware documentation for more information.
            Default: ()

                    """"
                        GRAPHENE = {
                            'MIDDLEWARE': (
                                'path.to.my.middleware.class',
                            ),
                        }
                    """"

* RELAY_CONNECTION_ENFORCE_FIRST_OR_LAST

            Enforces relay queries to have the first or last argument; Default:'False'

                    """"
                        GRAPHENE = {
                            'RELAY_CONNECTION_ENFORCE_FIRST_OR_LAST': False,
                        }
                    """"

* RELAY_CONNECTION_MAX_LIMIT

            The maximum size of objects that can be requested through a relay connection; Default: 100

                    """"
                        GRAPHENE = {
                            'RELAY_CONNECTION_MAX_LIMIT': 100,
                        }
                    """"

* CAMELCASE_ERRORS

            When set to "True" field names in the "errors" object will be camel case. By default they will be snake case.
            Default: False

                    """"
                        GRAPHENE = {
                           'CAMELCASE_ERRORS': True,
                        }

                        # result = schema.execute(...)
                        print(result.errors)
                    """"

* DJANGO_CHOICE_FIELD_ENUM_V3_NAMING

            Set to "True" to use the new naming format for the auto generated Enum types from Django choice fields.
            The new format looks like this: "{app_label}{object_name}{field_name}Choices"

            Default: False

* DJANGO_CHOICE_FIELD_ENUM_CUSTOM_NAME

            Define the path of a function that takes the Django choice field and returns a string to completely customise the
            naming for the Enum type.

            If set to a function then the "DJANGO_CHOICE_FIELD_ENUM_V3_NAMING" setting is ignored.

            Default: None

                    """"
                        # myapp.utils
                        def enum_naming(field):
                           if isinstance(field.model, User):
                              return f"CustomUserEnum{field.name.title()}"
                           return f"CustomEnum{field.name.title()}"

                        GRAPHENE = {
                           'DJANGO_CHOICE_FIELD_ENUM_CUSTOM_NAME': "myapp.utils.enum_naming"
                        }
                    """"

* SUBSCRIPTION_PATH

            Define an alternative URL path where subscription operations should be routed.

            The GraphiQL interface will use this setting to intelligently route subscription operations. This is useful
            if you have more advanced infrastructure requirements that prevent websockets from being handled at the same path
            (e.g., a WSGI server listening at '/graphql' and an ASGI server listening at '/ws/graphql').

            Default: None

                    """"
                        GRAPHENE = {
                           'SUBSCRIPTION_PATH': "/ws/graphql"
                        }
                    """"

* GRAPHIQL_HEADER_EDITOR_ENABLED

            GraphiQL starting from version 1.0.0 allows setting custom headers in similar fashion to query variables.

            Set to 'False' if you want to disable GraphiQL headers editor tab for some reason.

            This setting is passed to "headerEditorEnabled" GraphiQL options, for details refer to GraphiQLDocs.

            Default: True

                    """"
                        GRAPHENE = {
                           'GRAPHIQL_HEADER_EDITOR_ENABLED': True,
                        }
                    """"
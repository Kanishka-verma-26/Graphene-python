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

                In order to add authorization to id-based node access, we need to add a method to your "DjangoObjectType".





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


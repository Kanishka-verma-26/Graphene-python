*************   FILTERING   ************


Graphene-Django integrates with django-filter (2.x for Python 3 or 1.x for Python 2) to provide filtering of results using 'filter_fields'.

This filtering is automatically available when implementing a relay.Node. Additionally django-filter is an optional dependency of Graphene.




1) Basic Setup
                * create project, app, register, migrate
                * pip install django graphene_django; add in INSTALLED_APPS
                * write model and schema
                * setup urls
                            path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
                * add: GRAPHENE = {
                            "SCHEMA": "cookbook.schema.schema"
                        }

2) Filtering Setup
                * pip install django-filter>=2
                * add 'django_filters' in INSTALLED_APPS



3) Filterable fields

                The "filter_fields" parameter is used to specify the fields which can be filtered upon.
                The value specified here is passed directly to "django-filter",
                (see the filtering documentation for full details on the range of options available. )

                * model.py :
                            """"
                                class Animal(models.Model):
                                    DOG = 'DO'
                                    CAT = "CA"
                                    RABBIT = "RA"
                                    COW="CO"
                                    MOUSE = 'MO'
                                    PARROT = 'PA'
                                    OTHER = 'OT'

                                    animal_choices = [(DOG,'Dog'),(CAT,'Cat'),(RABBIT,'Rabbit'),
                                                      (COW,'Cow'),(MOUSE,'Mouse'),(PARROT,'Parrot'),(OTHER,'Other'),]

                                    name = models.CharField(max_length=100)
                                    animal = models.CharField(max_length=2, choices=animal_choices, default=DOG,)
                                    age = models.IntegerField()
                                    is_domestic = models.BooleanField(default=True)

                                    def __str__(self):
                                        return self.name
                            """"



                * schema.py :
                            """"
                                    """ Basic schema to print all animals present in db """
                                    class AllAnimals(DjangoObjectType):
                                        class Meta:
                                            model = Animal
                                            fields = ("id","name","animal","is_domestic","age")


                                    """ schema to print all animals or filtered animals using relay """
                                    class AnimalNode(DjangoObjectType):
                                        class Meta:
                                            # Assume you have an Animal model defined with the following fields
                                            model = Animal
                                            filter_fields = ['name','animal','age','is_domestic']
                                            interfaces = (relay.Node,)


                                    class Query(ObjectType):
                                        all_of_animal = graphene.List(AllAnimals)
                                        animals = relay.Node.Field(AnimalNode)                   # specific category
                                        all_animals = DjangoFilterConnectionField(AnimalNode)       #  list all categories

                                        def resolve_all_of_animal(root,info):
                                            return Animal.objects.all()


                                    schema = graphene.Schema(query=Query)
                            """"

                        ( run the below query to print all-of-the animals using basic method )

                                            """"
                                                query{
                                                  allOfAnimal{
                                                    id
                                                    isDomestic
                                                    animal
                                                  }
                                                }
                                            """"

                        ( run the below query to print all-of-the animals using relay method )

                                            """"
                                                query{
                                                  allAnimals{
                                                    edges{
                                                      node{
                                                        id
                                                        name
                                                        age
                                                        animal
                                                        isDomestic
                                                      }
                                                    }
                                                  }
                                                }
                                            """"

                        ( run the below query to print all-of-the specific animals based on the filters using relay method )

                                            """"
                                                query {
                                                  # Note that fields names become camelcased
                                                  allAnimals(animal:"DO", isDomestic:true) {                # this will print all-of-the
                                                    edges {                                            # animals i.e. Dog and is-domestic
                                                      node {
                                                        id,                                 # Graphene creates globally unique IDs for all objects in relay method
                                                        name
                                                        animal
                                                        age
                                                      }
                                                    }
                                                  }
                                                }
                                            """"

                        ( run the below query to print a specific animal based on its id )

                                            """"
                                                query{
                                                  animals(id:"QW5pbWFsTm9kZTo2"){
                                                    id
                                                    age
                                                    name
                                                    isDomestic
                                                  }
                                                }
                                            """"


                * You can also make more complex lookup types available:

                                """"
                                    class AnimalNodeComplex(DjangoObjectType):
                                        class Meta:
                                            model = Animal
                                            # Provide more complex lookup types
                                            filter_fields = {
                                                'name': ['exact', 'icontains', 'istartswith'],
                                                'animal': ['exact'],
                                                'is_domestic': ['exact'],
                                            }
                                            interfaces = (relay.Node, )
                                """"

                        ( run the below query )

                                """"
                                    query{
                                      allAnimalsComplex(name_Istartswith:"d"){
                                        edges{
                                          node{
                                            id
                                            age
                                            name
                                            animal
                                            isDomestic
                                          }
                                        }
                                      }
                                    }
                                """"


4) Custom Filtersets

                By default Graphene provides easy access to the most commonly used features of "django-filter".
                This is done by transparently creating a "django_filters.FilterSet" class for you and passing in the values for
                "filter_fields".

                However, you may find this to be insufficient. In these cases you can create your own "FilterSet". You can pass it directly as follows:

                                """"
                                    class AnimalNode(DjangoObjectType):
                                        class Meta:
                                            # Assume you have an Animal model defined with the following fields
                                            model = Animal
                                            filter_fields = ['name', 'animal', 'is_domestic']
                                            interfaces = (relay.Node, )


                                    class AnimalNodeFilters(django_filters.FilterSet):
                                        # Do case-insensitive lookups on 'name'
                                        name = django_filters.CharFilter(lookup_expr='iexact')

                                        class Meta:
                                            model = Animal
                                            fields = ['name', 'animal', 'is_domestic']


                                    class Query(ObjectType):
                                        animal = relay.Node.Field(AnimalNode)
                                        # We specify our custom AnimalFilter using the filterset_class param
                                        all_animals_filter_set1 = DjangoFilterConnectionField(AnimalNode, filterset_class=AnimalNodeFilters)

                                """"


                            ( query same as relay query to print all animals )
                                    """"
                                        query{
                                          allAnimalsFilterSet1{
                                            edges{
                                              node{
                                                id
                                                name
                                                animal
                                                age
                                                isDomestic
                                              }
                                            }
                                          }
                                        }
                                    """"

                            ( query to print particular animals wrt name )
                                    """"
                                        query{
                                          allAnimalsFilterSet1(name:"doggo"){
                                            edges{
                                              node{
                                                id
                                                name
                                                animal
                                                age
                                                isDomestic
                                              }
                                            }
                                          }
                                        }
                                    """"


                You can also specify the FilterSet class using the "filterset_class" parameter when defining your "DjangoObjectType",
                however, this can’t be used in unison with the "filter_fields" parameter:

                                """"
                                    class AnimalNodeFilters(django_filters.FilterSet):
                                        # Do case-insensitive lookups on 'name'
                                        name = django_filters.CharFilter(lookup_expr=['iexact'])

                                        class Meta:
                                            # Assume you have an Animal model defined with the following fields
                                            model = Animal
                                            fields = ['name', 'animal', 'is_domestic']


                                    class AnimalNode_filterset(DjangoObjectType):
                                        class Meta:
                                            model = Animal
                                            filterset_class = AnimalNodeFilters
                                            interfaces = (relay.Node, )


                                    class Query(ObjectType):
                                        animal = relay.Node.Field(AnimalNode)
                                        all_animals_filter_set2 = DjangoFilterConnectionField(AnimalNode_filterset)
                                """"

                            ( queries are same as previous two queries )


                The context argument is passed on as the request argument in a "django_filters.FilterSet" instance.
                You can use this to customize your filters to be context-dependent. We could modify the "AnimalFilter"
                above to pre-filter animals owned by the authenticated user (set in "context.user").

                                """"
                                    class AnimalNodeFilters(django_filters.FilterSet):
                                        # Do case-insensitive lookups on 'name'
                                        name = django_filters.CharFilter(lookup_type=['iexact'])

                                        class Meta:
                                            model = Animal
                                            fields = ['name', 'genus', 'is_domesticated']

                                        @property
                                        def qs(self):
                                            # The query context can be found in self.request.
                                            return super(AnimalNodeFilters, self).qs.filter(owner=self.request.user)
                                """"


5) Ordering

                You can use "OrderFilter" to define how you want your returned results to be ordered.
                Extend the tuple of fields if you want to order by more than one field.

                                """"
                                    from django_filters import FilterSet, OrderingFilter

                                    class UserFilter(FilterSet):
                                        class Meta:
                                            model = UserModel

                                        order_by = OrderingFilter(
                                            fields=(
                                                ('name', 'created_at'),
                                            )
                                        )

                                    class Group(DjangoObjectType):
                                      users = DjangoFilterConnectionField(Ticket, filterset_class=UserFilter)

                                      class Meta:
                                          name = 'Group'
                                          model = GroupModel
                                          interfaces = (relay.Node,)

                                      def resolve_users(self, info, **kwargs):
                                        return UserFilter(kwargs).qs
                                """"

                        (with this set up, you can now order the users under group: )

                                """"
                                    query {
                                      group(id: "xxx") {
                                        users(orderBy: "-created_at") {
                                          xxx
                                        }
                                      }
                                    }
                                """"



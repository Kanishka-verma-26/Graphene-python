import graphene
from graphene_django import DjangoObjectType
from .models import Animal
from graphene import relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from django_filters import FilterSet, OrderingFilter


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

""" OR """

""" Provide more complex lookup types """
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



""" Creating our own FilterSet class for AnimalNode class and Animal model """
class AnimalNodeFilters(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Animal
        fields = ['name','animal','is_domestic']


""" OR """


""" specify the 'FilterSet' class using the 'filterset_class' (i.e. AnimalNodeFilters) parameter when defining your 'DjangoObjectType' in Custom Filtersets """
class AnimalNode_filterset(DjangoObjectType):
    class Meta:
        model = Animal
        filterset_class = AnimalNodeFilters
        interfaces = (relay.Node, )








class Query(ObjectType):

    all_of_animal = graphene.List(AllAnimals)
    animals = relay.Node.Field(AnimalNode)                   # specific category
    all_animals = DjangoFilterConnectionField(AnimalNode)       #  list all categories
    all_animals_complex = DjangoFilterConnectionField(AnimalNodeComplex)        # category based  on complex lookupps

    # query for all animals with new custom Fieldset class 'AnimalNodeFilters' and DjangoObjectType 'AnimalNode'
    all_animals_filter_set1 = DjangoFilterConnectionField(AnimalNode, filterset_class = AnimalNodeFilters)

    # query for all animals with new custom Fieldset class 'AnimalNodeFilters' and DjangoObjectType 'AnimalNode_filterset'
    all_animals_filter_set2 = DjangoFilterConnectionField(AnimalNode_filterset)



    def resolve_all_of_animal(root,info):
        return Animal.objects.all()




schema = graphene.Schema(query=Query)
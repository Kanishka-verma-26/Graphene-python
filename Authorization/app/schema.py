from graphene import relay
import graphene
from graphene import ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from .models import Post
from graphene_django.debug import DjangoDebug

""" schema to print all posts that got published """
class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'
        interfaces = (relay.Node, )
        filter_fields = ["title", "content"]


""" defining custom 'get_queryset' instead of creating another resolve function ( just an upgraded version for upper class ) """
class PostNodeGlobalFiltering(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (relay.Node, )
        filter_fields = ["title", "content"]

    @classmethod
    def get_queryset(cls,queryset,info):
        print(info.context.user.is_anonymous)
        if info.context.user.is_anonymous:              # we are returning all posts for anonymous  user
            return queryset.filter(published=True)
        return queryset


""" Filtering ID-based Node Access """
class PostIDBasedNodeAccess(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'
        interfaces = (relay.Node,)
        filter_fields = ["title", "content","id"]






class Query(ObjectType):
    all_posts = DjangoFilterConnectionField(PostNode)       # print all posts
    my_posts = DjangoFilterConnectionField(PostNode)        #  User-based Queryset Filtering
    all_posts_global_filtering = DjangoFilterConnectionField(PostNodeGlobalFiltering)           # Global_filtering
    post_ID_based_node_access = DjangoFilterConnectionField(PostIDBasedNodeAccess)          #Post ID Based Node Access
    debug = graphene.Field(DjangoDebug,name ='_debug')

    def resolve_all_posts(self, info):
         return Post.objects.filter(published=True)

    def resolve_my_posts(self,info):
        # context will reference to the Django request
        print(info.context.user.is_authenticated)
        if not info.context.user.is_authenticated:
            return Post.objects.none()
        else:
            return Post.objects.filter(owner=info.context.user)

    def resolve_post_ID_based_node_access(self,info,**kwargs):
        print("inside def")
        print(kwargs)
        id = kwargs.get('id')

        if info.context.user.is_authenticated:
            return Post.objects.filter(owner=info.context.user,published=True)
        return None


schema = graphene.Schema(query=Query)
# result = schema.execute(query=Query, context_value=request)

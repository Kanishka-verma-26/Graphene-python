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


""" defining custom 'get_queryset' instead of creating another resolve function ( just an upgraded version for upper class ) """
class PostNodeGlobalFiltering(DjangoObjectType):
    class Meta:
        model = Post

    @classmethod
    def get_queryset(cls,queryset,info):
        if info.context.user.is_anonymous:              # we are returning all posts for anonymous  user
            return queryset.filter(published=True)
        return queryset


"""




class Query(ObjectType):
    all_posts = DjangoFilterConnectionField(PostNode)       # print all posts
    my_posts = DjangoFilterConnectionField(PostNode)        #  User-based Queryset Filtering
    all_posts_global_filtering = DjangoFilterConnectionField(PostNode)           # Global_filtering



    def resolve_all_posts(self, info):
         return Post.objects.filter(published=True)

    def resolve_my_posts(self,info):
        # context will reference to the Django request
        if not info.context.user.is_authenticated:
            return Post.objects.none()
        else:
            return Post.objects.filter(owner=info.context.user)


schema = graphene.Schema(query=Query)
# result = schema.execute(query=Query, context_value=request)

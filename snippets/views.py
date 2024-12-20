from tracemalloc import Trace

from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from rest_framework.reverse import reverse

from rest_framework import status, generics, renderers, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import permissions

from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides list,create,retrieve,update and destroy actions.
    Additionally we also provide ab extra highlight action.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self,request, *args, **kwargs):
        snippet = self.get_object()
        return  Response(snippet.highlighted)
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """This viewset automaticlly provides list and retrieve actions."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
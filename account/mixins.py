from django.http import Http404
from blog.models import Article
from django.shortcuts import get_object_or_404


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ['title', 'slug', 'category', 'description', 'thumbnail', 'publish', 'is_special', 'status',
                           'author']
        elif request.user.is_author:
            self.fields = ['title', 'slug', 'category', 'description', 'thumbnail', 'is_special', 'publish', ]
        else:
            raise Http404("You can't access to this page")
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = 'd'
        return super().form_valid(form)


class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if request.user.is_superuser or article.author == request.user and article.status in ['b', 'd']:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You can not see this page")


class SuperUserAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Yoy don't access to this page")

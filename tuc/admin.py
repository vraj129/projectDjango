from functools import update_wrapper

from django.contrib import admin
from django.http import (
    Http404, HttpResponseRedirect,
)
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect


# class MyAdminSite(admin.AdminSite):
#     def admin_view(self, view, cacheable=False):
#         def inner(request, *args, **kwargs):
#             if not self.has_permission(request):
#                 if request.path == reverse('admin:logout',
#                                            current_app=self.name):
#                     index_path = reverse('admin:index',
#                                          current_app=self.name)
#                     return HttpResponseRedirect(index_path)
#                 raise Http404()
#             return view(request, *args, **kwargs)
#         if not cacheable:
#             inner = never_cache(inner)
#         # We add csrf_protect here so this function can be used as a utility
#         # function for any view, without having to repeat 'csrf_protect'.
#         if not getattr(view, 'csrf_exempt', False):
#             inner = csrf_protect(inner)
#         return update_wrapper(inner, view)

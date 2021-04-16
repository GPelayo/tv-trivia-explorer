from django.contrib import admin

from superhero import helpers

for m in helpers.get_all_models():
    admin.site.register(m)

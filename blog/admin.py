from django.contrib import admin
from .models import Article, Person


class ArticleAdmin(admin.ModelAdmin):
    # list_display = ('title', 'pub_date', 'update_time',)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('full_name',)
    fields = (('last_name','first_name'))
    list_display = ('full_name','first_name', 'last_name')
    search_fields = ('first_name',)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(PersonAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(age=search_term_as_int)
        except:
            pass
        return queryset, use_distinct

admin.site.register(Article, ArticleAdmin)
admin.site.register(Person, PersonAdmin)
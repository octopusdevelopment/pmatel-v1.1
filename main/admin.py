from django.contrib import admin
from .models import Produit, Solution

admin.autodiscover()
admin.site.enable_nav_sidebar = False



class ProduitAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'solution')
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ('id','name',)
    list_per_page = 40
    list_filter = ('name',)
    search_fields = ('id', 'name',)


class SolutionAdmin(ProduitAdmin):
    list_display = ('id','name')


admin.site.register(Produit, ProduitAdmin)
admin.site.register(Solution, SolutionAdmin)




# admin.site.register(Slide, CategoryAdmin)
# admin.site.register(Categorie_produit, CategoryAdmin)
# admin.site.register(Categories_Solution, SolutionCategoryAdmin)
# admin.site.register(SliderAPropos, SliderAProposAdmin)
# admin.site.register(Catalogue, CatalogueAdmin)
# admin.site.register(ContactForm, ContactFormAdmin)
# admin.site.register(Partenaire, PartenairesAdmin)
# admin.site.register(ProduitDetail, ProduitDetailAdmin)
# admin.site.register(Post, PostAdmin)
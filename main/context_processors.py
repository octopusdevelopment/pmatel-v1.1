from .models import Category

def category(request):
    categories = Category.objects.all()
    categories_not_empty = []
    for cat in categories:
        category = cat
        category.number_products = len(category.products.filter(stock__gte=1, available=True))
        if not category.number_products == 0:
            categories_not_empty.append(category)
    return {
            'categories' : categories_not_empty
        }
    
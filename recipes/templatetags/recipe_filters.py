from django import template

register = template.Library()

@register.filter
def get_rating_percentage(ratings, value):
    total_ratings = ratings.count()
    if total_ratings == 0:
        return 0
    count = sum(1 for r in ratings if r.value == int(value))
    return (count / total_ratings) * 100 
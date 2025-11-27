from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """템플릿에서 딕셔너리 키로 값 가져오기"""
    if dictionary is None:
        return None
    return dictionary.get(key)


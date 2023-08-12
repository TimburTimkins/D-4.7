from django import template


register = template.Library()

@register.filter()
def censor(value):
   value_censor = ""
   for i in value.split():
      if i[0].isupper():
         i = i[0] + '*' * (len(i) - 1) + ' '
         value_censor += i
      else:
         i += ' '
         value_censor += i
   return value_censor

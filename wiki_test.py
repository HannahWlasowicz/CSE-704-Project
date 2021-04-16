import wikipedia
import wptools

test = 'Jimmy Fallon'
print(test.strip())

try:
   print(test, wikipedia.page(test))
except wikipedia.DisambiguationError as e:
    print('cant disambiguate', test)
    print(e.options)
    # fails.append((line, name_to_handle[line]))
except wikipedia.PageError as e:
    print('page error', test)
    print(e)
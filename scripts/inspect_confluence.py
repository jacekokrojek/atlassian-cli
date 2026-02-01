from inspect import getmembers, isfunction
from atlassian import Confluence
m = [name for name, obj in getmembers(Confluence, predicate=isfunction) if 'pdf' in name.lower() or 'export' in name.lower()]
print('\n'.join(m))
print('\n--- module file ---')
print(Confluence.__module__)
try:
    import pkgutil
    loader = pkgutil.get_loader(Confluence.__module__)
    print(loader.get_filename())
except Exception:
    pass

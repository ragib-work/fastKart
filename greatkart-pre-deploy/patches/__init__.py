def patch_admin_honeypot():
    import os
    import admin_honeypot
    models_file = os.path.join(os.path.dirname(admin_honeypot.__file__), 'models.py')
    
    with open(models_file, 'r') as f:
        content = f.read()
    
    content = content.replace(
        'from django.utils.translation import ugettext_lazy as _',
        'from django.utils.translation import gettext_lazy as _'
    )
    
    with open(models_file, 'w') as f:
        f.write(content)
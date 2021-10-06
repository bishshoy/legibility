def process_profile(doc, profile):
    
    # ICLR profile
    if profile == 'iclr':
        doc._profile = profile
        doc.article_class('article')
        doc.imports(['iclr2022_conference, times'])
        return
    
    # Elsevier profile
    # TODO: Add elsevier custom bst support
    # TODO: Add custom options like in article_class method
    elif profile == 'elsevier':
        doc._profile = profile
        doc.article_class('elsarticle')
        return
    
    else:
        raise ValueError('Profile '+profile+' not found.')
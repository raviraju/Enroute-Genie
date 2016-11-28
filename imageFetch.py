
# coding: utf-8

# In[17]:

from GoogleScraper import scrape_with_config, GoogleSearchError
from urllib.parse import unquote

def fetchImages(query):
    config = {
        'keyword': query,
        'search_engines': ['yandex'],
        'search_type': 'image',
        'scrape_method': 'selenium',
        'do_caching': True,
        'log_level': 'CRITICAL',
        'print_results': 'summary',
        'output_format': ''
    }

    try:
        search = scrape_with_config(config)
    except GoogleSearchError as e:
        print(e)

    image_urls = []

    for serp in search.serps:
        image_urls.extend(
            [link.link for link in serp.links]
        )
    max_num_of_images = 2
    images = []
    i = 0
    for image_url in image_urls:
        images.append(unquote(image_url))
        i += 1
        if i > max_num_of_images:
            break
    return images
images = fetchImages('golden gate bridge')
print(images)


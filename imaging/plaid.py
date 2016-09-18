import thumbnail.py

with open("links/plaid.txt", 'r') as f:
    paths = [download_image(url) for url in f]
    for path in paths:
        make_square_thumbnail(path, 128, "thumbnails")


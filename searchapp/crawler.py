from .models import Document, Term, DocumentTermFrequency
from .text_processor import process_text

import requests

from bs4 import BeautifulSoup

from urllib.parse import urljoin, urlparse



HEADERS = {

    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

}



def crawl_website(url):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=10
    )


    response.raise_for_status()


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    title = (
        soup.title.get_text(strip=True)
        if soup.title
        else "No Title"
    )


    # Remove unwanted content
    for tag in soup(
        [
            "script",
            "style",
            "noscript",
            "header",
            "footer",
            "nav",
            "aside"
        ]
    ):
        tag.decompose()



    # Create snippet

    meta = soup.find(
        "meta",
        attrs={
            "name": "description"
        }
    )


    if meta and meta.get("content"):

        snippet = meta["content"].strip()


    else:

        paragraphs = soup.find_all("p")


        text = " ".join(

            p.get_text(
                " ",
                strip=True
            )

            for p in paragraphs

        )


        text = " ".join(
            text.split()
        )


        if text:

            snippet = (
                " ".join(text.split()[:35])
                + "..."
            )

        else:

            snippet = (
                "No description available."
            )



    # Content for indexing

    text = soup.get_text(
        " ",
        strip=True
    )


    text = " ".join(
        text.split()
    )


    return title, text, snippet





def get_internal_links(url):

    links = set()

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        domain = urlparse(url).netloc

        for a in soup.find_all("a", href=True):

            link = urljoin(url, a["href"])

            parsed = urlparse(link)

            if parsed.scheme not in ["http", "https"]:
                continue

            if parsed.netloc != domain:
                continue

            clean_url = link.split("#")[0].split("?")[0]

            if clean_url.endswith((
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".svg",
                ".pdf",
                ".zip",
                ".css",
                ".js",
                ".xml"
            )):
                continue

            links.add(clean_url)

    except Exception as e:

        print(e)

    return list(links)






def index_website(url):


    title, text, snippet = crawl_website(url)



    document, created = Document.objects.get_or_create(

        url=url,

        defaults={
            "title": title,
            "snippet": snippet
        }

    )



    if not created:


        DocumentTermFrequency.objects.filter(
            document=document
        ).delete()



        document.title = title

        document.snippet = snippet

        document.save()



    word_frequency = process_text(text)



    for word, frequency in word_frequency.items():


        term, _ = Term.objects.get_or_create(

            word=word

        )


        DocumentTermFrequency.objects.create(

            document=document,

            term=term,

            frequency=frequency

        )







def index_multiple_pages(start_url, max_pages=10):


    visited = set()


    queue = [start_url]



    while queue and len(visited) < max_pages:


        current_url = queue.pop(0)



        if current_url in visited:

            continue



        try:


            print(
                "Indexing:",
                current_url
            )


            index_website(
                current_url
            )



            visited.add(
                current_url
            )



            links = get_internal_links(
                current_url
            )



            for link in links:


                if (
                    link not in visited
                    and link not in queue
                ):

                    queue.append(link)



        except Exception as e:


            print(
                "Skipped:",
                current_url,
                e
            )



    return len(visited)
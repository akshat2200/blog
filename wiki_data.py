import argparse
import wikipedia
import os
import json


def get_articles(language, max_no_articles, search, max_no_words):
    """ Retrieve articles from Wikipedia """
    wikipedia.set_rate_limiting(True) # be polite
    wikipedia.set_lang(language)

    if search is not None:
        titles = wikipedia.search(search, results = max_no_articles)
    else:
        titles = wikipedia.random(pages = max_no_articles)

    articles = []
    for title in titles:
        print("INFO: loading {}".format(title))
        page = wikipedia.page(title=title, auto_suggest=False)
        content = page.content
        article_no_words = len(content.split())
        if article_no_words > max_no_words:
            print("INFO: article contains {} words".format(article_no_words))
            articles.append((title, content))
        else:
            print("INFO: {}, article omitted because number of words are less than {}".format(title, max_no_words))

    print(f"Total articles in dataset: {len(articles)}")
    return articles


def articles2json(articles):
    """ Converts a list of (title, content) articles into an json file """

    data_json = [
                    {
                        'text': paragraph,
                        'meta': {
                            'source': title
                        }
                    } for title, paragraph in articles
                ]

    return data_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--max-no-articles", type = int, default=10,
                        help = "maximum number of articles to download")

    parser.add_argument("-s", "--search",
                        help = "if specified will use this search term")

    parser.add_argument("-l" ,"--language",
                        help = "2 letter language code")

    parser.add_argument("-w" ,"--max_no_words", type = int, default=1000,
                        help = "maximum number of words in article to download")

    args = parser.parse_args()
    articles = get_articles(**vars(args))
    data_json = articles2json(articles)

    with open(os.path.join('./text.json'), "w") as outfile:
        json.dump(data_json, outfile)


if __name__ == "__main__":
    main()
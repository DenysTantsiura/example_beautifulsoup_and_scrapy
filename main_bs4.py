"""скрапінг сайту http://quotes.toscrape.com.
отримати два файли: 
qoutes.json, куди помістіть всю інформацію про цитати, з усіх сторінок сайту 
та 
authors.json, де буде знаходитись інформація про авторів зазначених цитат.

Структура файлів json повинна повністю збігатися:

authors.json
[
  {
    "fullname": "Albert Einstein",
    "born_date": "March 14, 1879",
    "born_location": "in Ulm, Germany",
    "description": "In 1879, Albert Einstein was born in Ulm, Germany. He completed his Ph.D. at the University of Zurich by 1909. His 1905 paper explaining the photoelectric effect, the basis of electronics, earned him the Nobel Prize in 1921. His first paper on Special Relativity Theory, also published in 1905, changed the world. After the rise of the Nazi party, Einstein made Princeton his permanent home, becoming a U.S. citizen in 1940. Einstein, a pacifist during World War I, stayed a firm proponent of social justice and responsibility. He chaired the Emergency Committee of Atomic Scientists, which organized to alert the public to the dangers of atomic warfare.At a symposium, he advised: \"In their struggle for the ethical good, teachers of religion must have the stature to give up the doctrine of a personal God, that is, give up that source of fear and hope which in the past placed such vast power in the hands of priests. In their labors they will have to avail themselves of those forces which are capable of cultivating the Good, the True, and the Beautiful in humanity itself. This is, to be sure a more difficult but an incomparably more worthy task . . . \" (\"Science, Philosophy and Religion, A Symposium,\" published by the Conference on Science, Philosophy and Religion in their Relation to the Democratic Way of Life, Inc., New York, 1941). In a letter to philosopher Eric Gutkind, dated Jan. 3, 1954, Einstein stated: \"The word god is for me nothing more than the expression and product of human weaknesses, the Bible a collection of honorable, but still primitive legends which are nevertheless pretty childish. No interpretation no matter how subtle can (for me) change this,\" (The Guardian, \"Childish superstition: Einstein's letter makes view of religion relatively clear,\" by James Randerson, May 13, 2008). D. 1955.While best known for his mass–energy equivalence formula E = mc2 (which has been dubbed \"the world's most famous equation\"), he received the 1921 Nobel Prize in Physics \"for his services to theoretical physics, and especially for his discovery of the law of the photoelectric effect\". The latter was pivotal in establishing quantum theory.Einstein thought that Newtonion mechanics was no longer enough to reconcile the laws of classical mechanics with the laws of the electromagnetic field. This led to the development of his special theory of relativity. He realized, however, that the principle of relativity could also be extended to gravitational fields, and with his subsequent theory of gravitation in 1916, he published a paper on the general theory of relativity. He continued to deal with problems of statistical mechanics and quantum theory, which led to his explanations of particle theory and the motion of molecules. He also investigated the thermal properties of light which laid the foundation of the photon theory of light.He was visiting the United States when Adolf Hitler came to power in 1933 and did not go back to Germany. On the eve of World War II, he endorsed a letter to President Franklin D. Roosevelt alerting him to the potential development of \"extremely powerful bombs of a new type\" and recommending that the U.S. begin similar research. This eventually led to what would become the Manhattan Project. Einstein supported defending the Allied forces, but largely denounced the idea of using the newly discovered nuclear fission as a weapon. Later, with Bertrand Russell, Einstein signed the Russell–Einstein Manifesto, which highlighted the danger of nuclear weapons."
  },
  {
    "fullname": "Steve Martin",
    "born_date": "August 14, 1945",
    "born_location": "in Waco, Texas, The United States",
    "description": "Stephen Glenn \"Steve\" Martin is an American actor, comedian, writer, playwright, producer, musician, and composer. He was raised in Southern California in a Baptist family, where his early influences were working at Disneyland and Knott's Berry Farm and working magic and comedy acts at these and other smaller venues in the area. His ascent to fame picked up when he became a writer for the Smothers Brothers Comedy Hour, and later became a frequent guest on the Tonight Show.In the 1970s, Martin performed his offbeat, absurdist comedy routines before packed houses on national tours. In the 1980s, having branched away from stand-up comedy, he became a successful actor, playwright, and juggler, and eventually earned Emmy, Grammy, and American Comedy awards."
  }
]

qoutes.json
[
  {
    "tags": [
      "change",
      "deep-thoughts",
      "thinking",
      "world"
    ],
    "author": "Albert Einstein",
    "quote": "“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”"
  },
  {
    "tags": [
      "inspirational",
      "life",
      "live",
      "miracle",
      "miracles"
    ],
    "author": "Albert Einstein",
    "quote": "“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”"
  },
  {
    "tags": [
      "adulthood",
      "success",
      "value"
    ],
    "author": "Albert Einstein",
    "quote": "“Try not to become a man of success. Rather become a man of value.”"
  },
  {
    "tags": [
      "humor",
      "obvious",
      "simile"
    ],
    "author": "Steve Martin",
    "quote": "“A day without sunshine is like, you know, night.”"
  }
]

завантаження json файлів у хмарну базу даних для отриманих файлів. 
Попередня домашня робота повинна коректно працювати з новою отриманою базою даних.
"""
from collections import Counter
import json
import logging
from pprint import pprint
import re
from timeit import default_timer

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')


def duration(fun):
    def inner(*args, **kwargs):
        start = default_timer()
        rez = fun(*args, **kwargs)
        logging.info(f'{default_timer()-start=} sec')

        return rez

    return inner


def author_about(href):
    """Filter for specific(re) seach."""
    return href and re.compile("/author/").search(href)


def save_to_json(file: str, json_data: list) -> None:
    with open(file, "w", encoding="utf-8") as fh:  # try-except!
        json.dump(json_data, fh)


@duration
def main() -> None:
    url = 'https://quotes.toscrape.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    quotes = [quote.text for quote in soup.find_all('span', class_='text')]
    fullnames = [name.text for name in soup.find_all('small', class_='author')]
    # generate list of right links to author's about:
    abouts = [url.replace('https:','http:')+about['href'][1:]+'/' 
              for about in soup.find_all(href=author_about)]   # ('a', href=True)
    tags = [tag.find_all('a', class_='tag') for tag in soup.find_all('div', class_='tags')]
    tags = [[el.text for el in tag] for tag in tags]

    # grab author's about data to lists
    born_date = []
    born_location = []
    description = []

    for about in abouts:
        response_about = requests.get(about)
        soup_about = BeautifulSoup(response_about.text, 'lxml')
        born_date.append(soup_about.find('span', class_='author-born-date').text)
        born_location.append(soup_about.find('span', class_='author-born-location').text)
        description.append(soup_about.find('div', class_='author-description').text)

    quotes_in_json = [{'tags':tags[el],
                       'author':fullnames[el],
                       'quote':quotes[el],
                       } 
                       for el in range(len(quotes))]
    
    # remove duplicates:
    fix_dublicates = dict(Counter(description))
    for item in description:
        if fix_dublicates.get(item, None) > 1:
            number = description.index(item)
            del description[number]  # description.pop(number)
            del fullnames[number]
            del born_date[number]
            del born_location[number]
            fix_dublicates[item] -= 1

    authors_in_json = [{'fullname':fullnames[el],
                        'born_date':born_date[el],
                        'born_location':born_location[el],
                        'description':description[el],
                        } 
                       for el in range(len(fullnames))]  
    save_to_json('authors.json', authors_in_json)
    save_to_json('qoutes.json', quotes_in_json)


if __name__ == "__main__":
    main()

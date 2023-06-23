import os

def get_tag_content(ancestor, selector=None, attribute=None, return_list=False):
    try:
        if return_list:
            return [tag.get_text().strip() for tag in ancestor.select(selector)]
        if not selector and attribute:
            return ancestor[attribute].strip()
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).get_text().strip()
    except (AttributeError, TypeError):
        return None

selectors = {
    "opinion_id": (None, "data-entry-id"),
    "author": ("span.user-post__author-name",),
    "recommendation": ("span.user-post__author-recomendation > em",),
    "stars": ("span.user-post__score-count",),
    "purchased": ("div.review-pz",),
    "opinion_date": ("span.user-post__published > time:nth-child(1)","datetime"),
    "purchase_date": ("span.user-post__published > time:nth-child(2)","datetime"),
    "usefull_count": ("button.vote-yes","data-total-vote"),
    "unusefull_count": ("button.vote-no","data-total-vote"),
    "content": ("div.user-post__text",),
    "pros": ("div.review-feature__title--positives ~ div.review-feature__item", None, True),
    "cons": ("div.review-feature__title--negatives ~ div.review-feature__item", None, True)
}

def create_data_dir(name = None):
    if name:
        try:
            create_data_dir()
            os.mkdir(f"./app/data/{name}")
        except FileExistsError:
            pass
    else:
        try:
            os.mkdir("./app/data")
        except FileExistsError:
            pass
"""
Update review ratings/counts everywhere on mahadevniwas.com in one step.

1. Edit the 4 numbers below (Google Maps + Airbnb host dashboard).
2. Run from the repo root:   python tools/update_reviews.py
3. Commit and push.

Counts are shown rounded down to the nearest 10 with "+" (151 -> "150+"),
so the site stays true until the next update.
"""
import glob, re

GOOGLE_RATING = "4.9"    # Google Maps rating
GOOGLE_COUNT  = 151      # Google Maps review count
AIRBNB_RATING = "4.93"   # Airbnb overall host rating (Hosting > Insights > Reviews)
AIRBNB_COUNT  = 187      # Airbnb total reviews

def plus(n): return f"{(n // 10) * 10}+"
g, gc, a, ac = GOOGLE_RATING, plus(GOOGLE_COUNT), AIRBNB_RATING, plus(AIRBNB_COUNT)

# key -> (English HTML, Hindi HTML). data-hi always holds the Hindi text.
BLOCKS = {
 "g-badge": (f'<span class="badge"><span class="star" aria-hidden="true">★</span><b>{g}</b> <span data-hi="Google पर ({gc} रिव्यू)">on Google ({gc} reviews)</span></span>',
             f'<span class="badge"><span class="star" aria-hidden="true">★</span><b>{g}</b> <span data-hi="Google पर ({gc} रिव्यू)">Google पर ({gc} रिव्यू)</span></span>'),
 "a-badge": (f'<span class="badge"><span class="star" aria-hidden="true">★</span><b>{a}</b> <span data-hi="Airbnb पर ({ac} रिव्यू)">on Airbnb ({ac} reviews)</span></span>',
             f'<span class="badge"><span class="star" aria-hidden="true">★</span><b>{a}</b> <span data-hi="Airbnb पर ({ac} रिव्यू)">Airbnb पर ({ac} रिव्यू)</span></span>'),
 "host-line": (f'<li data-hi="सात बार Airbnb सुपरहोस्ट · Airbnb पर {a}★ और Google पर {g}★">Seven-time Airbnb Superhost · {a}★ on Airbnb and {g}★ on Google</li>',
               f'<li data-hi="सात बार Airbnb सुपरहोस्ट · Airbnb पर {a}★ और Google पर {g}★">सात बार Airbnb सुपरहोस्ट · Airbnb पर {a}★ और Google पर {g}★</li>'),
 "reviews-h2": (f'<h2 class="reveal" data-hi="Google पर {g}★ और Airbnb पर {a}★">Rated {g}★ on Google and {a}★ on Airbnb</h2>',
                f'<h2 class="reveal" data-hi="Google पर {g}★ और Airbnb पर {a}★">Google पर {g}★ और Airbnb पर {a}★</h2>'),
}

changed = 0
for f in glob.glob("*.html"):
    h = open(f, encoding="utf-8").read(); orig = h
    hindi = f.startswith("hi")
    for key, (en, hi) in BLOCKS.items():
        h = re.sub(rf"<!--stat:{key}-->.*?<!--/stat-->",
                   f"<!--stat:{key}-->{hi if hindi else en}<!--/stat-->", h, flags=re.S)
    # meta / og descriptions
    h = re.sub(r"\d\.\d+★ on Google(, \d\.\d+★ on Airbnb)?(?=, )", f"{g}★ on Google, {a}★ on Airbnb", h)
    if h != orig:
        open(f, "w", encoding="utf-8").write(h); changed += 1
print(f"Google {g} ({gc}) · Airbnb {a} ({ac}) -> updated {changed} file(s)")

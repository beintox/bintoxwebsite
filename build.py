#!/usr/bin/env python3
"""
BEINTOX static site generator.

    python3 build.py

Writes every *.html page in this folder from the content + templates below.
Pure standard library: no dependencies, no build step on the host.
Edit content in the DATA section, re-run, deploy the folder as-is.
"""
from __future__ import annotations

import html
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "assets" / "img"
VERSION = "32"  # bump to bust CSS/JS caches

# =====================================================================
# DATA
# =====================================================================

CONTACT = {
    "email": "info@beintox.com",
    "phone": "+92 308 4762273",
    "tel": "+923084762273",
    "location": "Lahore, Pakistan",
    "map": "https://maps.google.com/?q=Lahore%2C+Pakistan",
    "wa": "923084762273",
    "ig": "beintox",
    "fb": "https://www.facebook.com/profile.php?id=61593967393059",
}

NAV = [("index", "Home"), ("services", "Services"), ("portfolio", "Portfolio"), ("case-studies", "Case Studies"), ("about", "About"), ("contact", "Contact")]

SERVICES = [
    # (id, title, short, long, deliverables, case-slug or None)
    ("identity", "Logo Design & Branding", "Distinctive logos and cohesive brand identities.",
     "Build a clear, recognisable brand with a custom logo, color system, typography and practical brand guidelines.",
     ["Logo design", "Brand identity system", "Color & typography", "Brand guidelines"], "khyber-sajji"),
    ("social", "Social Media Management", "Consistent social content and day-to-day channel management.",
     "Keep your channels active and on-brand with planned content, publishing, community care and clear monthly reporting.",
     ["Content calendar", "Post & story design", "Publishing", "Community management", "Monthly reporting"], "khyber-sajji"),
    ("ads", "Performance Marketing", "Measurable campaigns built to grow leads and sales.",
     "Plan, launch and optimize paid campaigns across relevant channels, with clear tracking and reporting against business goals.",
     ["Campaign planning", "Paid social & search ads", "Audience targeting", "Conversion tracking", "Performance reports"], None),
    ("seo", "SEO", "Improve search visibility and attract qualified organic traffic.",
     "Make it easier for customers to find your business with technical improvements, useful content and ongoing search optimization.",
     ["Technical SEO review", "On-page optimization", "Keyword research", "Content recommendations", "Progress reporting"], None),
    ("photo", "Photography & Videography", "Professional imagery for products, people and campaigns.",
     "Create polished photo and video assets that show your products and brand at their best across your marketing channels.",
     ["Product photography", "Brand & lifestyle shoots", "Video production", "Editing & color grading"], "khyber-sajji"),
    ("web", "Website Design & Development", "Fast, responsive websites shaped around your brand.",
     "Design and develop a user-friendly website that explains your offer, works across devices and helps turn visitors into customers.",
     ["UX & interface design", "Responsive development", "Content structure", "SEO-ready foundations", "Launch support"], "khyber-sajji"),
    ("registration", "Brand Registration (IPO)", "Trademark registration guidance and filing support.",
     "Protect your brand name and identity with trademark availability checks, class guidance and support through the filing process.",
     ["Trademark availability search", "Class selection guidance", "Filing support", "Documentation follow-up"], None),
]
GROUPS = [("Brand", "Brand", ["identity", "registration"]),
          ("Digital", "Digital", ["social", "ads", "seo", "web"]),
          ("Content", "Content", ["photo"])]

# Case studies. Image paths are relative to assets/img.
CASES = [
    {
        "slug": "tomgai", "brief": "Create a warm, memorable identity for a new Chinese & Thai kitchen, and carry it consistently from launch billboards to takeaway bags and table service.", "services": ["identity", "social", "photo"], "name": "Tomgai Chinese", "sector": "Restaurant · Chinese & Thai", "brand": "#8f1a1e",
        "tags": ["Logo Design & Branding", "Social Media Management", "Photography & Videography"],
        "summary": "A warm, modern identity for a Chinese & Thai kitchen. A bamboo-stroke wordmark, a cheerful chef mascot and a red-and-cream system that runs from chopstick sleeves to billboards.",
        "cover": "tomgai/app-chefs", "hero": "tomgai/app-chefs", "logo": "logos/tomgai.png",
        "story": [
            "Tomgai is a fusion of warmth and tradition, inspired by the comforting essence of Asian cuisine. The name blends “Tom”, a nod to beloved soups like Tom Yum, with “Gai”, the Cantonese word for chicken: nourishment and heart in one word.",
            "Bold black typography spells the name, while a vertical red bamboo stroke replaces the “I”. It's a symbol of resilience and harmony that gives the mark its Chinese roots without leaning on cliché. The mascot is a cheerful chef holding a steaming bowl, dressed in traditional red with a branded hat.",
        ],
        "facts": [("Client", "Tomgai Chinese"), ("Sector", "Restaurant"), ("Scope", "Identity, content, packaging"), ("Deliverables", "Guidelines, mascot, 9+ applications")],
        "palette": [("#9e1c20", "#9E1C20"), ("#f9e1bb", "#F9E1BB"), ("#282725", "#282725"), ("#ffffff", "#FFFFFF")],
        "fonts": None,
        "sections": [
            ("identity", "Brand identity", "A guideline book that covers <em>every touchpoint.</em>", "Logo construction, meaning, usage rules, colour, type, pattern and character, documented so every supplier gets it right.",
             "gallery", ["bb-cover:Guidelines cover", "bb-logo-variations:Logo on colour", "bb-meaning:Name & meaning", "bb-logo-description:Logo description", "bb-logo-donts:Logo misuse", "bb-fonts:Brand fonts", "bb-palette:Colour palette", "bb-character:The Tomgai chef", "bb-pattern:Brand pattern"]),
            ("social", "Social media", "A feed that <em>tastes</em> like the menu.", "Dark, cinematic food photography with editorial type, built to stop the scroll and make the menu the hero.",
             "posts", ["post-dumplings:Chicken dumplings", "post-drink:Complimentary drink", "post-hotpot:Signature hot pot", "post-soup:19B soup", "post-legacy:The legacy of taste and love", "post-drumstick:Chicken drumstick"]),
            ("applications", "Applications", "From billboard to <em>chopstick sleeve.</em>", "The system applied across launch media, packaging, uniforms and table service.",
             "gallery", ["app-billboard-1:Launch billboard", "app-billboard-2:Launch billboard — dish", "pk-bag:Takeaway bag — “Wok your world”", "pk-chopsticks:Chopstick sleeves", "app-napkins:Napkins", "bb-business-card:Business cards", "bb-letterhead:Letterhead", "app-uniform:Chef uniform", "app-comment-card:Comment card", "app-table:Table setting", "app-hotpot:Hot pot detail", "bb-social:Teaser posts"]),
        ],
    },
    {
        "slug": "twenty-two", "brief": "Build one brand that serves two cravings, burgers and pizza, and make it instantly recognisable on every box, cup and post.", "services": ["identity", "social"], "name": "Twenty Two", "sector": "Fast food · Burgers & pizza", "brand": "#4b111f",
        "tags": ["Logo Design & Branding", "Social Media Management"],
        "summary": "Two shapes. One identity. A bold “22” monogram in orange and maroon for a burger-and-pizza brand, built into a full guideline book, a packaging range and a launch feed.",
        "cover": "twentytwo/pk-range", "hero": "twentytwo/pk-range", "logo": "logos/twentytwo.png",
        "story": [
            "Twenty Two serves two cravings under one roof. The identity turns that into a mark: two interlocking 2s, one in warm orange and one in deep maroon, standing for duality, partnership and balance.",
            "The positioning (“One craving. Two choices.”) runs through everything, from the guideline book's core values of Quality, Balance and Character to a packaging range that alternates the two colours piece by piece.",
        ],
        "facts": [("Client", "Twenty Two"), ("Sector", "Fast food"), ("Scope", "Strategy, identity, packaging, social"), ("Deliverables", "12-page guidelines, packaging range")],
        "palette": [("#4b111f", "Maroon"), ("#f0871f", "Orange"), ("#231f20", "Charcoal"), ("#f5ede4", "Warm white")],
        "fonts": ("Poppins", "Playfair Display"),
        "sections": [
            ("identity", "Brand identity", "Two shapes. One identity. <em>Endless balance.</em>", "A 12-page guideline book: story, logo system, clear space, colour, typography, backgrounds, misuse and applications.",
             "gallery", ["bb-cover:Guidelines cover", "bb-story:Our story", "bb-logo-overview:Logo overview", "bb-logo-variations:Logo variations", "bb-clear-space:Clear space & minimum size", "bb-palette:Colour palette", "bb-typography:Typography", "bb-backgrounds:Logo on backgrounds", "bb-misuse:Logo misuse", "bb-applications:Brand applications", "bb-contents:Contents", "bb-thanks:Closing page"]),
            ("packaging", "Packaging", "A range that reads as <em>one brand.</em>", "Bags, fry cartons, burger box, bucket, cups and dip lids, alternating orange and maroon so every piece is recognisable on its own.",
             "gallery2", ["pk-range:Full packaging range", "pk-delivery:Delivery bag & cooler"]),
            ("social", "Social media", "Launch content with <em>appetite.</em>", "A teaser-to-launch feed: bold serif headlines, product close-ups and the monogram as a graphic device.",
             "posts", ["post-coming:Something big is coming", "post-crunch:Crunch time", "post-pull-up:Pull up", "post-choices:One craving, two choices", "post-twice:Twice as good", "post-double:Double the flavor", "post-made-fresh:Made fresh, made right", "post-stay-cool:Stay cool", "post-double-2:Double smash burger"]),
        ],
    },
    {
        "slug": "khyber-sajji", "brief": "Introduce a traditional Khyber sajji brand to Lahore with a character people remember, and build anticipation before the doors opened.", "services": ["identity", "social", "web", "photo"], "name": "Khyber Sajji", "sector": "Restaurant · Traditional sajji", "brand": "#a82c17",
        "tags": ["Logo Design & Branding", "Social Media Management", "Website Design & Development", "Photography & Videography"],
        "summary": "A bold, friendly identity for Khyber-style roasted chicken: a mascot in a Peshawari cap, Urdu-first lettering and a teaser campaign that built anticipation in Lahore before the doors opened.",
        "cover": "khyber/app-storefront", "hero": "khyber/app-storefront", "logo": "logos/khyber.png",
        "story": [
            "Khyber Sajji brings the rich taste and traditional spirit of Khyber cuisine into a memorable, modern food experience. The mission is simple: flavourful, authentic roasted chicken with quality ingredients and consistent taste.",
            "The personality is bold, traditional, friendly, energetic and welcoming, so the brand got a character to match. Warm orange and deep red stand for fire, spice and appetite, and decorative display lettering is inspired by traditional South Asian signage.",
        ],
        "facts": [("Client", "Khyber Sajji"), ("Sector", "Restaurant"), ("Scope", "Identity, campaign, digital, photo"), ("Values", "Quality · Authenticity · Taste · Freshness · Hospitality")],
        "palette": [("#e8601c", "Warm orange"), ("#a82c17", "Deep red"), ("#f6b81c", "Golden yellow"), ("#6b3f22", "Dark brown"), ("#f4ead6", "Cream")],
        "fonts": ("BN Tillman", "Poppins"),
        "sections": [
            ("identity", "Brand identity", "A character people <em>remember.</em>", "Mascot, logo system, variations, colour, pattern, icon set and an illustration library for every occasion.",
             "gallery", ["bb-cover:Guidelines cover", "bb-mascot:Logo & mascot description", "bb-logo-guidelines:Logo guidelines", "bb-variations:Variations", "bb-palette:The colours", "bb-pattern:Brand pattern", "bb-icons:Brand icons & elements", "bb-illustrations:Illustrations"]),
            ("social", "Launch campaign", "“Hello Jii.” <em>Coming soon.</em>", "An Urdu-first teaser campaign for the Lahore launch: the mascot peeks through doors, curtains and newspapers until the reveal.",
             "posts", ["post-door:The door hanger", "post-curtain:Behind the curtain", "post-tension:Tension bhagao", "post-lahore:Lahore", "post-hello-jii:Hello Jii, coming soon", "post-newspaper:Something new for Lahore"]),
            ("applications", "Applications", "Storefront, fleet and <em>uniform.</em>", "The identity at full scale: signage, delivery vehicles, stationery and staff wear.",
             "gallery", ["app-storefront:Storefront", "app-van:Delivery van", "app-uniforms:Uniforms & merchandise", "app-stationery:Stationery set", "app-letterhead:Letterhead", "app-business-card:Business card"]),
            ("digital", "Website & app", "Ordering that looks like <em>the brand.</em>", "A website and mobile ordering flow designed in the brand system, from menu to checkout to order tracking.",
             "gallery", ["app-website:Website", "app-web-app:Website & app screens", "app-mobile:Mobile ordering flow"]),
            ("photo", "Photography", "Fire, smoke and <em>slow roast.</em>", "Food photography direction that shows the craft behind the dish.",
             "gallery4", ["photo-cooking:Preparation", "photo-roast:Signature sajji", "photo-grill:On the fire", "photo-chicken:Plated"]),
        ],
    },
    {
        "slug": "shehar-e-lazzat", "brief": "Give a modern bakery a premium identity rooted in tradition, one that works from the café counter to a gift box.", "services": ["identity", "social"], "name": "Shehar-e-Lazzat", "sector": "Bakery & café", "brand": "#13203a",
        "tags": ["Logo Design & Branding", "Social Media Management"],
        "summary": "The City of Taste. A navy-and-gold identity for a modern bakery rooted in tradition: a croissant-crown logo, jar desserts, gift boxes and a feed that sells every bake.",
        "cover": "shehar/app-mockups", "hero": "shehar/app-mockups", "logo": "logos/shehar.png",
        "story": [
            "Shehar-e-Lazzat is a modern bakery inspired by tradition, created to bring people together over the simple joy of great food. The name means “the city of taste”, and the identity is built to feel like a destination.",
            "A croissant shaped like a crown sits above Urdu lettering, set in deep navy and soft gold. The personality is elegant, welcoming, authentic, timeless and refined, carried through Playfair Display headlines and clean Montserrat text.",
        ],
        "facts": [("Client", "Shehar-e-Lazzat"), ("Sector", "Bakery & café"), ("Scope", "Identity, packaging, social"), ("Values", "Quality · Authenticity · Warmth · Community")],
        "palette": [("#13203a", "Royal navy"), ("#c9a75e", "Gold"), ("#f3ead9", "Cream"), ("#8a6a4a", "Warm taupe")],
        "fonts": ("Playfair Display", "Montserrat"),
        "sections": [
            ("identity", "Brand identity", "A taste of <em>tradition.</em>", "Brand overview, logo guidelines, colour, typography, visual language, patterns and stationery.",
             "gallery", ["bb-overview:Brand overview", "bb-logo-guidelines:Logo guidelines", "bb-palette:Colour palette", "bb-typography:Typography", "bb-visual-identity:Visual identity", "bb-type-specimen:Type specimen", "app-stationery:Stationery", "app-patterns:Brand patterns", "app-marketing:Marketing material"]),
            ("packaging", "Packaging", "Gift-ready, <em>shelf-ready.</em>", "A three-jar dessert gift box, a carry box with full dieline, and a cake-slice box, all print-ready.",
             "gallery", ["pk-jar-box:Dessert jar gift box", "pk-dieline:Carry box & dieline", "pk-slice-box:Cake slice box", "app-mockups:Brand mockups"]),
            ("social", "Social media", "Every bake, <em>a moment.</em>", "Deep navy backdrops, warm light and handwritten script, a feed that feels like walking into the café.",
             "posts", ["post-golden-layers:Golden layers of happiness", "post-flavor-burst:Flavor burst", "post-cookies:Best cookies around", "post-sundae:Sundae delight", "post-croissant-box:Croissant box", "post-donuts:The most delicious donuts", "post-sweet-beginning:A sweet beginning"]),
        ],
    },
]
CASE = {c["slug"]: c for c in CASES}

FAQ = [
    ("How long does a brand identity project take?", "Most identity projects take 3–6 weeks, depending on scope and how quickly feedback comes back. You'll get a timeline with clear milestones before any work starts."),
    ("Do you work with new and small businesses?", "Yes. Several brands in our portfolio were built from scratch, from the first logo and identity to their website and social presence."),
    ("Can I hire you for a single service?", "Yes. Hire us for logo design and branding, social media management, performance marketing, SEO, photo and video, website work or brand registration."),
    ("What do I receive at the end of an identity project?", "Final logo files in the formats you need, a brand guidelines document, color and typography specifications, and the agreed identity applications."),
    ("Can you help register our trademark?", "Yes. Our Brand Registration (IPO) service covers availability search, class guidance and filing support so your name and mark are protected."),
    ("How do we get started?", "Send us a short brief through the contact form or WhatsApp. We'll ask a few questions, then come back with a scoped proposal. Proposals are free."),
]

# Instagram profiles shown on the Portfolio page. Profile numbers are taken from the
# client's 2026 portfolio deck; update them here when they change.
IG = {
    "tomgai": {
        "handle": "tomgaichinese", "name": "TOMGAI Chinese", "category": "Chinese restaurant",
        "bio": ["Authentic Thai & Chinese flavors.", "From our kitchen to your cravings. 🍜"], "link": "tomgai.com",
        "posts": "158", "followers": "14.2K", "following": "182",
        "highlights": [("tomgai/post-hotpot", "Menu"), ("tomgai/app-billboard-1", "Launch"), ("tomgai/pk-bag", "Takeaway"), ("tomgai/bb-character", "Chef"), ("tomgai/app-chefs", "Kitchen")],
        "grid": ["post-drumstick:Chicken drumstick", "post-legacy:The legacy of taste and love", "post-soup:19B soup",
                 "post-hotpot:Signature hot pot", "post-drink:Complimentary drink", "post-dumplings:Chicken dumplings",
                 "app-billboard-1:Now open — launch", "pk-bag:Wok your world — takeaway", "app-chefs:The Tomgai kitchen"],
    },
    "twenty-two": {
        "handle": "twentytwo.official", "name": "Twenty Two", "category": "Restaurant",
        "bio": ["Twice the taste in one bite.", "Burgers · Pizza · Fries"], "link": "twentytwo.official",
        "posts": "124", "followers": "12.4K", "following": "153",
        "highlights": [("twentytwo/post-double", "Burgers"), ("twentytwo/post-pull-up", "Pizza"), ("twentytwo/post-crunch", "Sides"), ("twentytwo/pk-delivery", "Delivery"), ("twentytwo/post-coming", "Launch")],
        "grid": ["post-made-fresh:Made fresh, made right", "post-double:Double the flavor", "post-stay-cool:Stay cool",
                 "post-crunch:Crunch time", "post-pull-up:Pull up", "post-choices:One craving, two choices",
                 "post-twice:Twice as good", "post-double-2:Double smash burger", "post-coming:Something big is coming"],
    },
    "khyber-sajji": {
        "handle": "khyber.sajji", "name": "خیبر سجی · Khyber Sajji", "category": "Restaurant",
        "bio": ["Khyber Sajji serves taste from Khyber.", "Lahore 🔥"], "link": "khybersajji.official",
        "posts": "124", "followers": "12.4K", "following": "153",
        "highlights": [("khyber/post-hello-jii", "Coming soon"), ("khyber/photo-roast", "Sajji"), ("khyber/app-storefront", "Store"), ("khyber/app-van", "Delivery"), ("khyber/bb-mascot", "Mascot")],
        "grid": ["post-newspaper:Lahore, something new is coming", "post-door:The door hanger", "post-curtain:Behind the curtain",
                 "post-lahore:Lahore", "post-tension:Tension bhagao", "post-hello-jii:Hello Jii, coming soon",
                 "photo-roast:Signature sajji", "app-storefront:The storefront", "photo-grill:On the fire"],
    },
    "shehar-e-lazzat": {
        "handle": "shehar_e_lazzat", "name": "Shehar_e_Lazzat | Bakery & Cafe", "category": "Bakery",
        "bio": ["The ultimate baking experience 🥐✨", "The City of Taste"], "link": "Order now",
        "posts": "263", "followers": "1.7K", "following": "219",
        "highlights": [("shehar/post-golden-layers", "Café"), ("shehar/post-sundae", "Desserts"), ("shehar/post-cookies", "Cookies"), ("shehar/pk-jar-box", "Gifting"), ("shehar/app-mockups", "Brand")],
        "grid": ["post-golden-layers:Golden layers of happiness", "post-flavor-burst:Flavor burst", "post-cookies:Best cookies around",
                 "post-sundae:Sundae delight", "post-croissant-box:Croissant box", "post-donuts:The most delicious donuts",
                 "post-sweet-beginning:A sweet beginning", "pk-jar-box:Dessert jar gift box", "pk-slice-box:Cake slice box"],
    },
}

# Image shown beside each service on the Services page: one image, or three posts as a strip.
SVC_IMG = {
    "identity": "khyber/bb-cover",
    "registration": "tomgai/bb-logo-variations",
    "social": "khyber/post-curtain",
    "photo": "khyber/photo-roast",
    "ads": "twentytwo/post-double",
    "seo": "shehar/app-mockups",
    "web": "khyber/app-website",
}

SERVICE_PAGE_COPY = [
    ("identity", "Logo Design & Branding", "We create distinctive logos and cohesive brand identities that capture your business personality, establish recognition, and build a consistent visual presence across every touchpoint.", ["Logo Design", "Brand Identity", "Brand Guidelines"]),
    ("social", "Social Media Management", "We build engaging social media experiences through strategic content planning, consistent publishing, and active community management to strengthen your online presence and audience relationships.", ["Content Calendar", "Content Strategy", "Community Management"]),
    ("ads", "Performance Marketing", "We develop data-driven advertising campaigns that reach the right audience, generate qualified leads, improve conversions, and maximize your marketing performance.", ["Paid Advertising", "Lead Generation", "Conversion Optimization", "Ad Management"]),
    ("seo", "SEO", "We improve your website's search visibility through strategic optimization, helping attract relevant organic traffic, strengthen search rankings, and build sustainable online growth.", ["Technical SEO", "On-Page SEO", "Search Optimization"]),
    ("photo", "Photography & Videography", "We create compelling visual content through professional photography, video production, and creative storytelling that showcases your products and brings your brand vision to life.", ["Product Photography", "Video Production", "Creative Shoots", "Photo & Video Editing", "AI & UGC Video Ads"]),
    ("web", "Website Design & Development", "We design and develop modern, responsive websites with intuitive user experiences, combining creative design and functional technology to strengthen your digital presence and convert visitors into customers.", ["UI/UX Design", "Web Development", "Responsive Websites"]),
    ("registration", "Brand Registration (IPO)", "We guide businesses through the intellectual property protection process, from trademark searches and search reports to trademark and copyright registration, documentation, and filing support.", ["Search Report", "Trademark & Copyright Registration", "Documentation", "Filing Support", "Newspaper Ads"]),
]

SERVICE_INDUSTRIES = ["Startup", "Small Business", "Entrepreneur", "Tech Company", "Corporate", "Nonprofit", "E-commerce Store", "Consulting Firm", "Restaurants"]
SERVICE_FEATURES = [
    ("Creation", "Tailored posts that resonate with your audience, boosting engagement and brand loyalty.", "M5 34 29 10l9 9-24 24H5v-9ZM25 14l9 9M5 43l9-1"),
    ("Management", "Seamless management of all your social media channels, ensuring consistent and effective communication.", "M5 15 24 5l19 10-19 10L5 15ZM5 24l19 10 19-10M5 33l19 10 19-10"),
    ("Advertising", "Strategic ad placements that reach your ideal audience, driving traffic and conversions.", "M17 20a6 6 0 1 0 0-12 6 6 0 0 0 0 12ZM5 41v-5a11 11 0 0 1 22 0v5M33 21a5 5 0 1 0 0-10M31 27a10 10 0 0 1 12 10v4M29 17h5l8-5v20l-8-5h-5z"),
    ("Analytics", "Detailed reports that offer insights into your social media performance, helping you refine your strategy.", "M7 39V25h8v14M20 39V14h8v25M33 39V6h8v33M5 43h38"),
    ("Engagement", "Active engagement with your followers, building a strong and supportive community around your brand.", "M7 28h8l5 5h10l8-7a4 4 0 0 1 6 5L32 43H17L7 37zM15 28l7-12a4 4 0 0 1 7 4l-4 8M8 26v14"),
    ("Consulting", "Expert advice on how to position your brand for success in the digital landscape.", "M24 5a10 10 0 1 0 0 20 10 10 0 0 0 0-20ZM18 24l-2 19 8-5 8 5-2-19"),
]
SERVICE_COMPARISON = {
    "other": ["Slow communication", "Single channel approach", "Outdated growth strategies", "Lack of industry research", "Outsourced to mediocre talent"],
    "beintox": ["Constant, proactive communication", "Omni-channel approach", "Tailored best-fit solutions", "Provides industry specific expertise", "Experts with 10+ years of experience"],
}
CLIENT_VIDEO_PREVIEWS = [
    ("Khyber Sajji", "khyber/photo-roast"),
    ("Twenty Two", "twentytwo/post-double"),
    ("Shehar-e-Lazzat", "shehar/app-mockups"),
]

STEPS = [("Discover", "We study your business, audience and competitors to find what makes you worth choosing."),
         ("Define", "Positioning, personality and message: the strategy every design decision answers to."),
         ("Design", "Identity, content and campaigns crafted with one look, one voice and one feeling."),
         ("Grow", "We launch, measure and refine, turning attention into lasting customer relationships.")]

WHY = [("One team, every discipline", "Strategy, identity, content, ads and web under one roof, so your brand speaks with one voice everywhere."),
       ("Strategy before pixels", "We define who you're for and why you win before we design anything. Every visual answers to that."),
       ("Systems, not one-offs", "Each identity ships with guidelines, so the brand stays consistent long after launch."),
       ("Bilingual creative", "Urdu and English campaigns written and designed for how your customers actually talk."),
       ("Production-ready", "Dielines, print files, signage and uniforms. We design for the real world, not just the screen."),
       ("Clear process", "Defined scope, milestones and one point of contact. You always know what's next.")]

PLANS = [("Project", "Single project", "One defined deliverable with a fixed scope and timeline.", ["Logo and brand identity", "SEO", "Website", "Campaign optimization"], False),
         ("For new brands", "Brand launch", "Everything a new business needs to open strong, from brand identity to its first online campaigns.", ["Logo design & branding", "Brand registration guidance", "Social media launch", "Website & performance marketing"], True),
         ("Ongoing", "Monthly retainer", "A dedicated team managing your social channels and performance campaigns month after month.", ["Monthly content calendar", "Social channel management", "Paid campaign optimization", "Monthly performance report"], False)]

# Team (from the client's previous website). photo=None renders initials until a real photo is supplied.
FOUNDER = ("Ali Imtiaz", "CEO & Founder", "team/ali", "Leading BEINTOX with a vision to redefine branding and marketing standards.")
TEAM = [("Arslan Khizar", "Lead Designer", "team/arslan"),
        ("Farhan Ali", "Graphic Designer, Branding", "team/farhan"),
        ("Fahad", "Videographer", "team/fahad"),
        ("Memona Muneer", "Full Stack Web Developer", None)]

# =====================================================================
# HELPERS
# =====================================================================

E = html.escape


def img_size(path: Path) -> tuple[int, int]:
    """Read pixel dimensions of supported image formats without third-party libraries."""
    with path.open("rb") as image_file:
        b = image_file.read(65536)
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", b[16:24])
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP":
        kind = b[12:16]
        if kind == b"VP8X":
            return (int.from_bytes(b[24:27], "little") + 1, int.from_bytes(b[27:30], "little") + 1)
        if kind == b"VP8 ":
            w, h = struct.unpack("<HH", b[26:30])
            return (w & 0x3FFF, h & 0x3FFF)
        if kind == b"VP8L":
            v = int.from_bytes(b[21:25], "little")
            return ((v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1)
    if b[:2] == b"\xff\xd8":
        i = 2
        while i < len(b):
            if b[i] != 0xFF:
                i += 1
                continue
            while i < len(b) and b[i] == 0xFF:
                i += 1
            if i >= len(b):
                break
            marker = b[i]
            i += 1
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                continue
            if i + 2 > len(b):
                break
            length = int.from_bytes(b[i:i + 2], "big")
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                if i + 7 <= len(b):
                    return (int.from_bytes(b[i + 5:i + 7], "big"), int.from_bytes(b[i + 3:i + 5], "big"))
                break
            if length < 2:
                break
            i += length
    raise ValueError(f"Unsupported image: {path}")


def src(rel: str) -> str:
    return rel if "." in rel.rsplit("/", 1)[-1] else rel + ".webp"


def img(rel: str, alt: str, eager: bool = False, cls: str = "") -> str:
    path = src(rel)
    w, h = img_size(IMG / path)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="assets/img/{path}" alt="{E(alt)}" width="{w}" height="{h}" {load} decoding="async"{c}>'


def href(page: str) -> str:
    return f"{page}.html"


ICON = {
    "arrow": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "check": '<svg viewBox="0 0 18 18" fill="none" aria-hidden="true"><circle cx="9" cy="9" r="8.25" stroke="currentColor" stroke-opacity=".35"/><path d="M5.5 9.2l2.2 2.2 4.8-4.8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "menu": '<svg viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M2 5h14M2 9h14M2 13h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
    "close": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
    "prev": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "next": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M6 3l5 5-5 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "play": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M8 5.5v13l10-6.5-10-6.5Z" fill="currentColor"/></svg>',
    "pause": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M8 6v12M16 6v12" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>',
    "mail": '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="2.5" y="4.5" width="15" height="11" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M3 5.5l7 5 7-5" stroke="currentColor" stroke-width="1.5"/></svg>',
    "phone": '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M5 2.8h2.6l1.3 3.4-1.7 1.1a9.5 9.5 0 0 0 5.5 5.5l1.1-1.7 3.4 1.3V15a2.2 2.2 0 0 1-2.2 2.2A13.2 13.2 0 0 1 2.8 5 2.2 2.2 0 0 1 5 2.8Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>',
    "pin": '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M16 8.2c0 4.3-6 9.2-6 9.2S4 12.5 4 8.2a6 6 0 1 1 12 0Z" stroke="currentColor" stroke-width="1.5"/><circle cx="10" cy="8" r="2" stroke="currentColor" stroke-width="1.5"/></svg>',
    "ig": '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="2.75" y="2.75" width="14.5" height="14.5" rx="4" stroke="currentColor" stroke-width="1.5"/><circle cx="10" cy="10" r="3.4" stroke="currentColor" stroke-width="1.5"/><circle cx="14.4" cy="5.6" r=".9" fill="currentColor"/></svg>',
    "fb": '<svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M11.2 18v-7h2.35l.35-2.73H11.2V6.53c0-.79.22-1.33 1.36-1.33H14V2.76c-.25-.03-1.11-.11-2.11-.11-2.1 0-3.54 1.28-3.54 3.63v1.99H6v2.73h2.35v7z"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M5.3 3.5a2 2 0 1 1 0 4 2 2 0 0 1 0-4ZM3.6 9h3.4v11H3.6zm5.5 0h3.2v1.5h.05A3.5 3.5 0 0 1 15.5 8.8c3.5 0 4.1 2.3 4.1 5.2V20h-3.4v-5.3c0-1.3 0-3-1.8-3s-2.1 1.4-2.1 2.9V20H9.1z"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.2-.2-.5-.3Z"/></svg>',
}
ARROW = ICON["arrow"]

# BEINTOX wordmark — letter paths traced from the brand PDF; X redrawn as vector with the brand gold.
LOGO_PATHS = (
    "M87.84 76.57C86.23 76.99 84.54 77.25 82.88 77.25C64.01 77.3 45.14 77.29 26.27 77.29C25.73 77.29 25.19 77.18 24.34 77.08L24.34 59.9C25.91 59.9 27.26 59.9 28.61 59.9C46.09 59.89 63.56 59.86 81.04 59.9C83.25 59.91 85.51 60.15 87.67 60.62C91.83 61.54 93.62 64.47 93.72 68.55C93.83 72.71 91.94 75.52 87.84 76.57M107.12 50.43C106.96 50.33 106.96 49.96 106.84 49.58C107.18 49.25 107.56 48.86 107.96 48.5C123.17 35.01 119.78 12.41 100.94 4.82C95.02 2.43 88.18 1.47 81.74 1.38C55.86 1.01 29.97 1.23 4.08 1.24C2.85 1.24 1.62 1.37 .23 1.44L.23 22.39C1.58 22.46 2.54 22.56 3.51 22.56C27.99 22.52 52.48 22.45 76.97 22.46C80.16 22.46 83.41 22.63 86.55 23.2C90.55 23.93 92.46 26.76 92.4 30.75C92.35 34.71 90.44 37.44 86.4 38.18C84.09 38.6 81.69 38.79 79.33 38.8C54.57 38.86 29.8 38.86 5.03 38.88C3.41 38.88 1.78 38.88 .08 38.88L.08 100.76C1.53 100.85 2.76 100.98 3.98 100.98C30.98 100.99 57.99 101.01 84.99 100.93C88.47 100.92 92.02 100.7 95.41 100C107.05 97.61 115.95 91.79 118.73 79.43C121.47 67.22 117.75 57.4 107.12 50.43Z"
    "M785.91 64.32C783.36 71.67 778.25 76.97 770.45 77.26C754.13 77.86 737.76 77.87 721.44 77.33C713.34 77.05 707.86 71.85 705.28 64.1C702.41 55.48 702.44 46.72 705.09 38.12C707.83 29.22 714.92 24.19 725.14 23.76C731.99 23.47 738.85 23.71 745.71 23.71C752.56 23.7 759.43 23.45 766.27 23.76C777.64 24.28 784.7 30.45 786.98 41.57C788.55 49.22 788.49 56.86 785.91 64.32M812.63 48.09C811.81 21.2 797.61 4.33 771.46 1.73C754.31 .03 736.8 .61 719.54 1.65C705.45 2.51 693.58 9.06 685.86 21.59C678.95 32.8 677.73 45.21 678.72 57.94C680.58 81.75 694.94 97.44 718.55 100.47C727.34 101.6 736.4 100.65 745.34 100.65C745.34 100.75 745.34 100.84 745.34 100.94C753.58 100.94 761.86 101.41 770.07 100.85C791.03 99.41 806.2 87.07 810.75 67.59C812.23 61.28 812.83 54.58 812.63 48.09Z"
    "M481.19 66.45C479.88 65.39 479.11 64.84 478.42 64.21C456.71 44.25 435.01 24.27 413.27 4.34C411.96 3.15 410.39 1.48 408.88 1.42C401.81 1.11 394.72 1.28 387.48 1.28L387.48 100.68L410.51 100.68L410.51 30.58C412.94 32.85 414.64 34.43 416.32 36.03C438.05 56.79 459.77 77.56 481.52 98.3C482.6 99.33 483.93 100.77 485.19 100.82C491.54 101.08 497.91 100.94 504.27 100.94L504.27 1.59L481.19 1.59Z"
    "M542.62 23.15H585.75V100.81H609.78V22.93H652.61V1.53H542.62Z"
    "M159.89 77.56h110.59v23.06H159.89zM160.07 1.44h110.62v21.39H160.07zM314.61 1.47h23.1v99.22h-23.1zM160.05 38.44h93.35v21.6H160.05z"
)
X_PATHS = ("M835.75 99.75H868.25L965.75 1.5H935.75Z", "M838.25 1.5H872L899.5 29.25L880.75 46.5Z", "M905 71.5L923.25 54.25L967 99.75H933.25Z")


def logo(light: bool = False, sub: bool = True) -> str:
    xs = "".join(f'<path d="{d}" fill="url(#bxg)"/>' for d in X_PATHS)
    # Subtitle lives inside the same SVG and is stretched to the wordmark's exact width,
    # so it always lines up with the B on the left and the X on the right.
    t = ('<text class="logo__sub" x="2" y="178" textLength="964" lengthAdjust="spacing">MARKETING SOLUTIONS</text>' if sub else "")
    h = 182 if sub else 102
    return (f'<span class="logo{" logo--light" if light else ""}"><svg viewBox="0 0 968 {h}" role="img" aria-label="BEINTOX Marketing Solutions">'
            f'<g class="logo__adaptive"><path d="{LOGO_PATHS}" fill="currentColor"/>{t}</g>{xs}</svg></span>')


GRAD_DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
             '<linearGradient id="bxg" x1="830" y1="100" x2="968" y2="0" gradientUnits="userSpaceOnUse">'
            '<stop offset="0" stop-color="#D4A017"/><stop offset=".35" stop-color="#D4A017"/>'
            '<stop offset=".55" stop-color="#D4A017"/><stop offset="1" stop-color="#D4A017"/></linearGradient></defs></svg>')


def checks(items) -> str:
    return '<ul class="checks">' + "".join(f"<li>{ICON['check']}<span>{E(i)}</span></li>" for i in items) + "</ul>"


def head_block(eyebrow: str, title: str, lead: str = "", aside: str = "", h: str = "h2") -> str:
    tag = "h1" if h == "h1" else "h2"
    right = f'<p class="lead">{lead}</p>' if lead else ""
    return (f'<div class="head"><div><span class="eyebrow">{eyebrow}</span><{tag} class="{h}">{title}</{tag}></div>'
            f'<div class="head__aside">{right}{aside}</div></div>')


def cta_band(title="Ready to make your brand <em>unforgettable?</em>",
             lead="Tell us where your brand is today and where you want it to go. We'll reply with a scoped proposal.") -> str:
    return f'''<section class="sec"><div class="wrap"><div class="cta">
  <div><h2 class="h2">{title}</h2><p class="lead">{lead}</p></div>
  <form class="subscribe-form" data-email="{CONTACT["email"]}">
    <label class="sr-only" for="newsletter-email">Email address</label>
    <input id="newsletter-email" name="email" type="email" placeholder="Email address" autocomplete="email" required>
    <button class="btn btn--gold" type="submit">Subscribe {ARROW}</button>
  </form>
</div></div></section>'''


def svc_by_id(i: str):
    return next(s for s in SERVICES if s[0] == i)


def svc_num(i: str) -> str:
    return f"{[s[0] for s in SERVICES].index(i) + 1:02d}"


# =====================================================================
# LAYOUT
# =====================================================================

def layout(page: str, title: str, desc: str, body: str, schema: dict | None = None) -> str:
    cur = ' aria-current="page"'
    links = "".join(
        f'<li><a href="{href(k)}"{cur if k == page or (page.startswith("case:") and k == "case-studies") else ""}>{l}</a></li>'
        for k, l in NAV)
    base = '<base href="/">\n' if page == "404" else ""
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    case_links = "".join(f'<li><a href="case-study-{c["slug"]}.html">{E(c["name"])}</a></li>' for c in CASES)
    svc_links = "".join(f'<li><a href="services.html#{s[0]}">{E(s[1])}</a></li>' for s in SERVICES)
    footer_nav = "".join(f'<li><a href="{href(k)}">{E(label)}</a></li>' for k, label in NAV)
    header = f'''<header class="nav"><div class="wrap">
  <a href="/" aria-label="BEINTOX home">{logo(light=True)}</a>
  <ul class="nav__links" id="nav-links">{links}</ul>
  <a class="btn btn--gold nav__cta" href="contact.html">Let's Make a Strategy Call {ARROW}</a>
  <button class="nav__toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav-links">{ICON["menu"]}</button>
</div></header>'''
    css_version = (f"{VERSION}-impact-badges-ladder-v3" if page == "index" else
                   f"{VERSION}-services-layout-v8" if page == "services" else VERSION)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
{base}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#1F1F1F">
<meta property="og:type" content="website">
<meta property="og:site_name" content="BEINTOX Marketing Solutions">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/css/style.css?v={css_version}">
<script>document.documentElement.classList.add("js")</script>
{ld}
</head>
<body>
{GRAD_DEFS}
<a class="skip" href="#main">Skip to content</a>
{header}
<main id="main">
{body}
</main>
<footer class="footer"><span class="footer__watermark" aria-hidden="true">BEINTOX</span><div class="wrap">
  <div class="footer__main">
    <div class="footer__contact-cards" aria-label="Contact BEINTOX">
      <a class="footer__contact-card" href="mailto:{CONTACT["email"]}"><span class="footer__contact-icon">{ICON["mail"]}</span><span>{CONTACT["email"]}</span></a>
      <a class="footer__contact-card" href="tel:{CONTACT["tel"]}"><span class="footer__contact-icon">{ICON["phone"]}</span><span>{CONTACT["phone"]}</span></a>
      <a class="footer__contact-card" href="{CONTACT["map"]}" target="_blank" rel="noopener"><span class="footer__contact-icon">{ICON["pin"]}</span><span>{CONTACT["location"]}</span></a>
    </div>
    <div class="footer__columns">
      <nav class="footer__column" aria-label="Footer menu"><h4>Menu</h4><ul>{footer_nav}</ul></nav>
      <nav class="footer__column footer__column--services" aria-label="Footer services"><h4>Services</h4><ul>{svc_links}<li><a href="services.html">All services</a></li></ul></nav>
    </div>
  </div>
  <div class="footer__social"><h4>Follow us</h4><div class="footer__social-links">
    <a href="{CONTACT["fb"]}" target="_blank" rel="noopener" aria-label="BEINTOX on Facebook">{ICON["fb"]}</a>
    <a href="https://www.instagram.com/{CONTACT["ig"]}/" target="_blank" rel="noopener" aria-label="BEINTOX on Instagram">{ICON["ig"]}</a>
  </div></div>
  <div class="footer__bar"><span>© <span data-year>2026</span> BEINTOX Marketing Solutions</span><span>Being memorable is what makes brands grow.</span></div>
</div></footer>
<a class="wa" href="https://wa.me/{CONTACT["wa"]}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{ICON["wa"]}</a>
<dialog class="lb" id="lb" aria-label="Image viewer"><img alt=""><div class="lb__bar"><span></span>
  <button type="button" data-prev aria-label="Previous">{ICON["prev"]}</button><button type="button" data-next aria-label="Next">{ICON["next"]}</button><button type="button" data-close aria-label="Close">{ICON["close"]}</button></div></dialog>
<script src="assets/js/site.js?v={VERSION}-work-controls-v1" defer></script>
</body>
</html>
'''


# =====================================================================
# COMPONENTS
# =====================================================================

def case_card(c: dict, eager=False) -> str:
    tags = "".join(f'<span class="tag">{E(t)}</span>' for t in c["tags"][:4])
    return f'''<a class="case" href="case-study-{c["slug"]}.html">
  <div class="case__img">{img(c["cover"], f'{c["name"]} brand work by BEINTOX', eager)}</div>
  <div class="case__body"><h3 class="h3">{E(c["name"])}</h3><span class="case__sector">{E(c["sector"])}</span>
  <p>{E(c["summary"])}</p><div class="tags">{tags}</div></div></a>'''


def svc_card(sid: str, num: bool = True) -> str:
    s = svc_by_id(sid)
    n = f'<span class="card__n">{svc_num(s[0])}</span>' if num else ""
    return f'''<a class="card svc-card" href="services.html#{s[0]}">{n}
  <h3 class="h3">{E(s[1])}</h3><p>{E(s[2])}</p><span class="card__go">Learn more {ARROW}</span></a>'''


def post_grid(items, folder, cls="posts", link_case=None, group=True) -> str:
    out = []
    for it in items:
        key, cap = it.split(":", 1)
        rel = f"{folder}/{key}"
        if link_case:
            out.append(f'<a class="post" href="case-study-{link_case}.html" title="{E(cap)}">{img(rel, cap)}</a>')
        else:
            out.append(f'<a class="post" href="assets/img/{src(rel)}" data-lb="{E(cap)}">{img(rel, cap)}</a>')
    g = " data-lb-group" if group and not link_case else ""
    return f'<div class="{cls}"{g}>' + "".join(out) + "</div>"


def gallery(items, folder, cls="gallery") -> str:
    out = []
    for it in items:
        key, cap = it.split(":", 1)
        rel = f"{folder}/{key}"
        out.append(f'<figure class="shot"><a href="assets/img/{src(rel)}" data-lb="{E(cap)}">{img(rel, cap)}</a><figcaption>{E(cap)}</figcaption></figure>')
    return f'<div class="{cls}" data-lb-group>' + "".join(out) + "</div>"


# =====================================================================
# PAGES
# =====================================================================

def steps_html(steps=None) -> str:
    return '<div class="steps">' + "".join(
        f'<div class="step rv" style="--i:{i}"><span class="step__n">{i + 1:02d}</span><span class="step__k">Step {i + 1}</span><h3 class="h3">{t}</h3><p>{d}</p></div>'
        for i, (t, d) in enumerate(steps or STEPS)) + "</div>"


def why_html() -> str:
    return '<div class="feats">' + "".join(
        f'<div class="feat rv" style="--i:{i}"><span class="feat__n">{i + 1:02d}</span><h3 class="h3">{E(t)}</h3><p>{E(d)}</p><span class="feat__bg" aria-hidden="true">{i + 1:02d}</span></div>'
        for i, (t, d) in enumerate(WHY)) + "</div>"


BELIEFS = [
    ("Be seen", "Visibility is earned with design that stops the scroll and media placed where your customers already are.",
     '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3.2"/>'),
    ("Be understood", "A clear position and a simple message, so people know in seconds what you offer and why it matters.",
     '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>'),
    ("Be remembered", "Consistency builds memory. One look, one voice, repeated everywhere until your brand is the one they choose.",
     '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>'),
]


def beliefs_html() -> str:
    out = []
    for i, (t, d, ic) in enumerate(BELIEFS):
        out.append(f'''<article class="belief belief--{i + 1} rv" style="--i:{i}">
  <div class="belief__top"><span>{i + 1:02d}</span><i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true">{ic}</svg></i></div>
  <h3>{E(t)}</h3><p>{E(d)}</p></article>''')
    return '<div class="beliefs">' + "".join(out) + "</div>"


def plans_html() -> str:
    return '<div class="grid g3">' + "".join(
        f'''<div class="card plan{" plan--featured" if f else ""}"><span class="plan__k">{k}</span><h3 class="h3" style="font-size:21px">{t}</h3><p>{d}</p>{checks(items)}
        <a class="btn {"btn--dark" if f else "btn--line"} btn--s" href="contact.html">Discuss this {ARROW}</a></div>'''
        for k, t, d, items, f in PLANS) + "</div>"


def faq_html() -> str:
    return '<div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ) + "</div>"


# Client logos shown in the strip. Brands with a case study link to it; the rest are logo-only.
# size: "s" = wide wordmark, "l" = tall / round mark (gets more height so it reads at the same weight)
EXTRA_CLIENTS = [("Velvet Crunch", "logos/velvetcrunch.png", "xl"), ("Leatherifyy", "logos/leatherifyy.png", "l")]
LOGO_SIZE = {"tomgai": "s", "twenty-two": "s", "khyber-sajji": "l", "shehar-e-lazzat": "l"}

# Testimonials — PLACEHOLDER copy, replace with real client quotes before launch.
TESTIMONIALS = [
    ("Ahmed R.", "Founder, restaurant brand", "They didn't just design a logo, they gave us a brand our customers recognise from across the street. The launch campaign had people queuing before we opened."),
    ("Sana K.", "Owner, bakery & café", "Every piece, from the gift boxes to the Instagram feed, finally looks like it belongs to one brand. Our regulars noticed the difference straight away."),
    ("Bilal M.", "Director, fast-food chain", "Clear process, quick replies and a team that actually understood our customers. The packaging range alone paid for the project."),
    ("Hira Ali", "Co-founder, D2C snack brand", "BEINTOX handled strategy, design and our monthly content. One team, one voice. It's made growing the brand so much easier."),
    ("Usman T.", "Founder, leather goods", "Sharp, modern identity and a website that converts. They pushed us to define who we're for before touching a single colour."),
    ("Maryam S.", "Marketing lead, retail", "Our ads finally look premium and perform better. Monthly reports are clear, and we always know what's coming next."),
]


def logo_marquee() -> str:
    items = [(f'portfolio.html#{c["slug"]}', c["name"], c["logo"], LOGO_SIZE.get(c["slug"], "s")) for c in CASES]
    items += [(None, n, path, size) for n, path, size in EXTRA_CLIENTS]
    one = "".join(
        f'<a href="{h}" class="logo-{sz}" aria-label="{E(n)}">{img(p, n + " logo")}</a>' if h else
        f'<span class="logo-{sz}" role="img" aria-label="{E(n)}">{img(p, n + " logo")}</span>'
        for h, n, p, sz in items)
    half = one * 2
    dup = half.replace("<a ", '<a tabindex="-1" aria-hidden="true" ').replace('role="img" ', 'aria-hidden="true" ')
    return f'''<section class="clients" aria-label="Clients"><div class="wrap">
  <span class="clients__label">Brands we've built</span>
  <div class="marquee"><div class="marquee__track">{half}{dup}</div></div>
</div></section>'''


def stats_band() -> str:
    """Brand promise and four animated proof points for the home page."""
    metrics = [
        ("11", "", "Integrated Services", "Everything your brand needs, under one roof.", "M10 3v18M3 10h14l4 4v7H3zM7 14h6"),
        ("360", "°", "Brand Growth", "From logo design to building a complete brand.", "M4 17 9 12l4 3 7-9M14 6h6v6"),
        ("95", "%", "Client Retention Rate", "Built on trust, consistency, and results.", "M12 21s-8-4.5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 6.5-8 11-8 11Z"),
        ("500", "+", "Creative Assets Produced", "Ideas transformed into impactful creative work.", "M4 4h7v7H4zM14 4h7v7h-7zM4 14h7v7H4zM14 14h7v7h-7z"),
    ]
    badges = [
        '<span class="kpi-badge kpi-badge--social" aria-label="TikTok, Instagram, YouTube and LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 3v11.2a4.1 4.1 0 1 1-3.2-4V7.1c1.1 1.6 2.7 2.6 5.2 2.8V6.5c-1.2-.3-2-1.2-2-2.4V3Z"/></svg><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.7" cy="6.8" r=".8" class="fill"/></svg><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="4"/><path class="fill" d="m10 9 5 3-5 3z"/></svg><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="3"/><path class="fill" d="M7 10h3v8H7zm1.5-4a1.7 1.7 0 1 0 0 3.4 1.7 1.7 0 0 0 0-3.4M12 10h3v1.1c.5-.8 1.3-1.3 2.4-1.3 2.1 0 2.6 1.4 2.6 3.4V18h-3v-4.2c0-1-.1-1.8-1.2-1.8s-1.5.8-1.5 1.8V18H12z"/></svg></span>',
        '<span class="kpi-badge kpi-badge--people" aria-label="Brand growth"><i>A</i><i>B</i><i>C</i><b>+</b></span>',
        '<span class="kpi-badge kpi-badge--platforms"><span class="kpi-badge__meta">∞</span><span class="kpi-badge__tiktok">♪</span><b>Meta + TikTok</b></span>',
        '<span class="kpi-badge kpi-badge--live"><i></i><b>Live reporting</b></span>',
    ]
    cells = "".join(
        f'<article class="kpi rv" style="--i:{i}"><div class="kpi__meta">{badges[i]}</div><strong class="kpi__number"><span class="kpi__prefix">+</span><span data-count="{n}">{n}</span><sup>{suf}</sup></strong><h3>{title}</h3><p>{desc}</p></article>'
        for i, (n, suf, title, desc, icon) in enumerate(metrics))
    return f'''<section class="kband"><div class="wrap">
  <div class="kband__intro">
    <h2 class="h2 rv" style="--i:0"><span class="kband__headline-main">From an idea to a brand that</span><em>stands out.</em></h2>
    <p class="lead rv" style="--i:1">We turn ideas into powerful brand identities and transform businesses through creative strategy.</p>
  </div>
  <div class="kpis" aria-label="BEINTOX results">{cells}</div>
</div></section>

PROCESS_STEPS = [
    ("Discover & Strategize", "We take time to understand your business problems, target audience, market, and objectives. Through research and strategic planning, we identify opportunities and create a clear direction for your brand.",
     '<path class="icon-accent icon-chat" d="M28 22h60a8 8 0 0 1 8 8v28a8 8 0 0 1-8 8H61L46 78V66H28a8 8 0 0 1-8-8V30a8 8 0 0 1 8-8Z"/><path class="icon-accent icon-draw" d="M49 36v16M41 44h16"/><circle class="icon-muted" cx="34" cy="91" r="8"/><circle class="icon-muted" cx="60" cy="87" r="9"/><circle class="icon-muted" cx="87" cy="91" r="8"/><path class="icon-muted" d="M19 113c1-11 7-16 15-16s14 5 15 16M41 116c1-13 8-20 19-20s18 7 19 20M75 113c1-11 7-16 15-16s14 5 15 16"/>'),
    ("Design & Create", "Transform ideas into meaningful brand experiences through creative design, visual identity, engaging content, and digital solutions that reflect your brand's personality.",
     '<path class="icon-accent icon-chat" d="M22 23h48a7 7 0 0 1 7 7v21a7 7 0 0 1-7 7H49L37 69V58H22a7 7 0 0 1-7-7V30a7 7 0 0 1 7-7ZM61 40h38a7 7 0 0 1 7 7v20a7 7 0 0 1-7 7H88L77 84V74h-4"/><circle class="icon-muted" cx="43" cy="94" r="8"/><circle class="icon-muted" cx="72" cy="94" r="8"/><path class="icon-muted" d="M26 116c1-11 7-16 17-16s16 5 17 16M55 116c1-11 7-16 17-16s16 5 17 16"/>'),
    ("Launch & Execute", "Turn strategies into action by launching campaigns, managing digital platforms, producing creative content, and delivering solutions that connect your brand with the right audience.",
     '<rect class="icon-muted" x="17" y="23" width="90" height="70" rx="8"/><path class="icon-accent" d="M17 42h90M31 32h1M41 32h1M52 32h1"/><path class="icon-accent icon-draw" d="m36 76 18-17 14 10 25-25M81 44h12v12"/><path class="icon-muted" d="M48 105h28M62 93v12"/>'),
    ("Optimize & Grow", "We continuously monitor performance, analyze results, and refine our strategies to improve engagement, strengthen brand presence, and achieve sustainable business growth.",
     '<rect class="icon-muted" x="19" y="23" width="88" height="78" rx="7"/><path class="icon-muted" d="M19 43h88M39 23v78M58 23v78M77 23v78M19 62h88M19 82h88"/><path class="icon-accent icon-draw" d="m30 79 16-13 14 7 25-24 11 3M85 52l11-3-2 11"/><circle class="icon-accent" cx="35" cy="34" r="3"/>'),
]


def home_process_section() -> str:
    cards = "".join(
        f'''<article class="process-card rv" style="--i:{i}">
  <span class="process-card__index" aria-hidden="true">0{i + 1}</span>
  <span class="process-card__label">STEP 0{i + 1}</span>
  <div class="process-card__copy"><h3>{E(title)}</h3><p>{E(description)}</p></div>
</article>'''
        for i, (title, description, graphic) in enumerate(PROCESS_STEPS))
    return f'''<section class="sec home-process" aria-labelledby="home-process-title"><div class="wrap">
  <div class="home-process__intro">
    <span class="eyebrow home-process__eyebrow"><b>How can we help you?</b></span>
    <h2 class="h2" id="home-process-title"><span>Take Your Brand &amp;</span><span>Social Media to</span><em>New Heights</em></h2>
    <p class="lead">At Beintox, we make social media management stress-free.</p>
  </div>
  <div class="home-process__stack" aria-label="Our four-step process">{cards}</div>
</div></section>'''


# Service cards on the home page: colour + decorative shape per service.
SVC_LOOK = {
    "identity": ("#c0602f", "#4d1d0c", "rings"),
    "social": ("#33479a", "#0d1440", "tiles"),
    "ads": ("#7a3466", "#260b21", "bars"),
    "web": ("#55504a", "#151311", "browser"),
    "photo": ("#9a2533", "#33080f", "lens"),
    "seo": ("#2f7a6e", "#123630", "arcs"),
    "registration": ("#a57a34", "#33230b", "rings"),
}
SHAPES = {
    "rings": '<circle class="o" cx="110" cy="100" r="86"/><circle class="o" cx="110" cy="100" r="56"/><circle class="a" cx="110" cy="100" r="26"/>',
    "tiles": '<rect x="20" y="20" width="74" height="74" rx="14" class="o"/><rect x="106" y="20" width="74" height="74" rx="14" class="o"/><rect x="20" y="106" width="74" height="74" rx="14" class="o"/><rect class="a" x="106" y="106" width="74" height="74" rx="14"/>',
    "box": '<path class="o" d="M100 18 172 58v84l-72 40-72-40V58z"/><path class="o" d="M28 58l72 40 72-40M100 98v84"/><path class="a" d="M100 98l72-40v84l-72 40z"/>',
    "bars": '<rect class="o" x="24" y="120" width="30" height="60" rx="8"/><rect class="o" x="66" y="88" width="30" height="92" rx="8"/><rect class="o" x="108" y="54" width="30" height="126" rx="8"/><rect class="a" x="150" y="20" width="30" height="160" rx="8"/>',
    "browser": '<rect class="o" x="14" y="30" width="172" height="130" rx="14"/><path class="o" d="M14 58h172"/><rect class="a" x="32" y="76" width="80" height="66" rx="8"/><path class="o" d="M126 82h42M126 100h42M126 118h28"/>',
    "lens": '<circle class="o" cx="100" cy="100" r="84"/><path class="o" d="M100 16l44 72M184 100l-84 0M144 172l-44-72M56 172l44-72M16 100h84M56 28l44 72"/><circle class="a" cx="100" cy="100" r="34"/>',
    "arcs": '<circle class="a" cx="104" cy="100" r="84"/><path class="o" d="M26 66c48 26 108 26 156 0M26 134c48-26 108-26 156 0"/>',
    "x": '<path class="a" d="M30 176h34L176 24h-34z"/><path class="o" d="M34 24h36l32 32-20 20zM118 120l20-20 46 76h-36z"/>',
}


HOME_CARD_CONTENT = {
    "identity": ("Distinctive logos and cohesive brand identities that make your business recognizable.", ["Logo Design", "Brand Identity", "Brand Guidelines"]),
    "social": ("Engaging social media experiences through strategic content, consistent publishing, and community management.", ["Content Calendar", "Content Strategy", "Community Management"]),
    "ads": ("Data-driven advertising campaigns designed to generate quality leads, increase conversions, and accelerate business growth.", ["Paid Advertising", "Lead Generation", "Conversion Optimization", "Audit Management"]),
    "seo": ("Improving search visibility through strategic optimization that attracts relevant traffic and builds long-term growth.", ["Technical SEO", "On-Page SEO", "Search Optimization"]),
    "photo": ("We produce high-quality visual content that showcases your products, tells your story, and connects with your audience.", ["Product Photography", "Video Production", "Creative Shoots", "Photo & Video Editing", "AI & UGC Video Ads"]),
    "web": ("Design and develop responsive, user-friendly websites that strengthen your digital presence and turn visitors into customers.", ["UI/UX Design", "Web Development", "Responsive Websites"]),
    "registration": ("From guidance on trademark and copyright registration through documentation and case filing, we help businesses protect their brand identity.", ["Search Report", "Trademark & Copyright Registration", "Documentation", "Newspaper Ads"]),
}


def svc_feature(sid: str, i: int) -> str:
    s = svc_by_id(sid)
    description, card_tags = HOME_CARD_CONTENT[sid]
    c1, c2, shape = SVC_LOOK[sid]
    group = next(g[0] for g in GROUPS if sid in g[2])
    tags = "".join(f"<span>{E(t)}</span>" for t in card_tags)
    return f'''<a class="svcx rv" href="services.html#{sid}" style="--c1:{c1};--c2:{c2};--i:{i}">
  <div class="svcx__top"><span>Service {svc_num(sid)}</span><span>{group}</span></div>
  <svg class="svcx__art" viewBox="0 0 200 200" aria-hidden="true">{SHAPES[shape]}</svg>
  <div class="svcx__body"><h3>{E(s[1])}</h3><p>{E(description)}</p><div class="svcx__tags">{tags}</div></div>
  <span class="svcx__go" aria-hidden="true">{ARROW}</span>
</a>'''


def testimonials() -> str:
    stars = '<span class="tm__stars" aria-label="5 out of 5">★★★★★</span>'

    def cards(hidden: bool) -> str:
        h = ' aria-hidden="true"' if hidden else ""
        return "".join(
            f'''<figure class="tm"{h}>{stars}<blockquote>“{E(q)}”</blockquote>
  <figcaption><span class="tm__av">{"".join(w[0] for w in name.split()[:2])}</span><span><b>{E(name)}</b><small>{E(role)}</small></span></figcaption></figure>'''
            for name, role, q in TESTIMONIALS)
    return f'''<section class="sec tms"><div class="wrap">
  {head_block("<b>03</b> Testimonials", "In our clients' <em>own words.</em>", "Restaurants, bakeries, retail and D2C brands. Here's what working with one team feels like.")}
</div>
<div class="reel reel--tm" aria-label="Client testimonials"><div class="reel__track">{cards(False)}{cards(True)}</div></div>
</section>'''


def brand_reel() -> str:
    """Three client videos in a looping carousel with arrows and a full-screen player."""
    videos = [
        ("Khyber Sajji", "assets/videos/khyber-sajji-ai-reel-1.mp4", "assets/img/khyber/post-curtain.webp"),
        ("Khyber Sajji", "assets/videos/khyber-sajji-ai-reel-2.mp4", "assets/img/khyber/post-lahore.webp"),
        ("Nisa Sultan", "assets/videos/nisa-sultan-brand-film.mp4", "assets/img/posters/nisa-sultan-cover.jpeg"),
    ]

    def cards(clone: bool = False) -> str:
        rendered = []
        for brand, src, poster in videos:
            if clone:
                rendered.append(f'''<div class="rc rc--work rc--work-clone" aria-hidden="true">
  <img src="{poster}" alt="" width="1080" height="1920" loading="lazy" decoding="async">
  <span class="rc__top"><span>{E(brand)}</span></span>
  <span class="work-play" aria-hidden="true">{ICON["play"]}</span></div>''')
            else:
                rendered.append(f'''<button class="rc rc--work" type="button" data-work-video="{src}" data-work-poster="{poster}" aria-label="Play {E(brand)} brand film">
  <img src="{poster}" alt="" width="1080" height="1920" loading="lazy" decoding="async">
  <span class="rc__top"><span>{E(brand)}</span></span>
  <span class="work-play" aria-hidden="true">{ICON["play"]}</span></button>''')
        return "".join(rendered)

    return f'''<div class="work-reel" data-work-reel>
  <div class="work-reel__controls" aria-label="Video slider controls">
    <button type="button" data-work-prev aria-label="Previous video">{ICON["prev"]}</button>
    <button type="button" data-work-toggle aria-label="Pause video slider" aria-pressed="false"><span class="work-pause-icon">{ICON["pause"]}</span><span class="work-play-icon">{ICON["play"]}</span></button>
    <button type="button" data-work-next aria-label="Next video">{ICON["next"]}</button>
  </div>
  <div class="reel reel--work" aria-label="Selected video work"><div class="reel__track">{cards()}{cards(True)}</div></div>
  <dialog class="work-lightbox" aria-label="Brand film player">
    <button class="work-lightbox__close" type="button" data-work-close aria-label="Close video">{ICON["close"]}</button>
    <video controls controlsList="nodownload" playsinline preload="none" aria-label="Selected brand film"></video>
  </dialog>
</div>'''
# Hero creative wall: three columns scrolling in alternating directions. The supplied client posts replace the previous artwork.
WALL = [
    ["tomgai/home-creative-01.jpg", "twentytwo/home-creative-02.jpg", "shehar/home-creative-03.jpg", "khyber/home-creative-04.jpg", "tomgai/home-creative-05.jpg", "twentytwo/home-creative-06.jpg", "twentytwo/home-creative-07.jpg", "khyber/home-creative-08.jpg", "shehar/home-creative-09.jpg"],
    ["tomgai/home-creative-10.jpg", "shehar/home-creative-11.jpg", "khyber/home-creative-12.jpg", "khyber/home-creative-13.jpg", "shehar/home-creative-14.jpg", "tomgai/home-creative-15.jpg", "twentytwo/home-creative-16.jpg", "khyber/home-creative-17.jpg", "shehar/home-creative-18.jpg"],
    ["tomgai/home-creative-19.jpg", "tomgai/home-creative-20.jpg", "twentytwo/home-creative-21.jpg", "shehar/home-creative-22.jpg", "khyber/home-creative-23.jpg", "tomgai/home-creative-24.jpg", "twentytwo/home-creative-25.jpg", "twentytwo/home-creative-26.jpg"],
]
WALL_BRAND = {"tomgai": ("tomgai", "Tomgai"), "twentytwo": ("twenty-two", "Twenty Two"), "khyber": ("khyber-sajji", "Khyber Sajji"), "shehar": ("shehar-e-lazzat", "Shehar-e-Lazzat")}


def creative_wall() -> str:
    cols = []
    for ci, col in enumerate(WALL):
        def tile(rel: str, first: bool, hidden: bool) -> str:
            slug, name = WALL_BRAND[rel.split("/")[0]]
            attrs = ' tabindex="-1" aria-hidden="true"' if hidden else ""
            return f'<a class="wall__item" href="portfolio.html#{slug}"{attrs}>{img(rel, f"{name} creative by BEINTOX", eager=first)}<span>{name}</span></a>'
        a = "".join(tile(r, i < 3, False) for i, r in enumerate(col))
        b = "".join(tile(r, False, True) for r in col)
        cols.append(f'<div class="wall__col{" wall__col--down" if ci == 1 else ""}" style="--dur:{[64, 76, 58][ci]}s"><div class="wall__track">{a}{b}</div></div>')
    return f'<div class="hero__wall" aria-label="Creatives designed by BEINTOX">{"".join(cols)}</div>'


def page_home() -> str:
    mosaic_html = creative_wall()
    schema = {
        "@context": "https://schema.org", "@type": "ProfessionalService", "name": "BEINTOX Marketing Solutions",
        "description": "Logo design, social media management and digital marketing services.", "email": CONTACT["email"], "telephone": CONTACT["tel"],
        "address": {"@type": "PostalAddress", "addressCountry": "PK"}, "sameAs": [f"https://instagram.com/{CONTACT['ig']}"],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1]}} for s in SERVICES],
    }
    body = f'''
<section class="hero"><div class="wrap">
  <div class="hero__copy">
    <h1 class="h1">We Build Values<br><em>That Stand Out &amp; Grow.</em></h1>
    <p class="lead">From brand identity and creative design to digital marketing and web development, we help startups transform their ideas into powerful brands.</p>
    <div class="btns"><a class="btn btn--gold" href="contact.html">Let's Build Your Brand {ARROW}</a><a class="btn btn--ghost" href="services.html">Explore Our Services</a></div>
    <span class="eyebrow hero__signature"><b>BEINTOX</b> Your creative &amp; growth partner</span>
  </div>
  {mosaic_html}
</div></section>

{logo_marquee()}

{stats_band()}

{home_process_section()}

<section class="sec sec--white bt"><div class="wrap">
  {head_block("<b>02</b> Our Work", "<em>Ready</em> to see these kinds of results for your <em>brand?</em>", "Our approach combines strategy, execution, and consistency. We handle the planning, posting, and platform management so you can focus on running the business.", f'<div class="btns" style="gap:20px"><a class="link" href="case-studies.html">Read the case studies {ARROW}</a><a class="link" href="portfolio.html">Open the portfolio {ARROW}</a></div>')}
</div>
{brand_reel()}
</section>

{testimonials()}

{cta_band()}
'''
    return layout("index", "BEINTOX: Branding & Digital Marketing Agency | Social Media, SEO, Web",
                  "BEINTOX offers logo design and branding, social media management, performance marketing, SEO, photography and videography, website design and development, and brand registration.",
                  body, schema)


def svc_tile(sid: str, i: int = 0) -> str:
    s = svc_by_id(sid)
    m = SVC_IMG.get(sid)
    m = m[0] if isinstance(m, list) else m
    group = next(g[1] for g in GROUPS if sid in g[2])
    if s[5]:
        c = CASE[s[5]]
        see = f'<a class="svc3__see" href="case-study-{c["slug"]}.html">See it in {E(c["name"])} {ARROW}</a>'
    else:
        see = f'<a class="svc3__see" href="contact.html">Request a proposal {ARROW}</a>'
    items = "".join(f"<li>{E(d)}</li>" for d in s[4])
    return f'''<article class="svc3 rv" id="{s[0]}" style="--i:{i % 3}">
  <div class="svc3__img">{img(m, f"{s[1]}: example from our work")}
    <span class="svc3__num">{svc_num(s[0])}</span><span class="svc3__grp">{E(group)}</span></div>
  <div class="svc3__body">
    <div class="svc3__head"><h3 class="h3">{E(s[1])}</h3><span class="svc3__arrow" aria-hidden="true">{ARROW}</span></div>
    <p>{E(s[3])}</p>
    <ul class="svc3__list">{items}</ul>
    {see}
  </div>
</article>'''


def service_offering(item: tuple, i: int) -> str:
    sid, title, description, included = item
    image = SVC_IMG[sid]
    media = f'''<aside class="service-offering__visual" aria-label="Project investment information">
  <div class="service-offering__image">{img(image, f"{title}: BEINTOX portfolio work", cls="service-offering__photo")}
    <span class="service-offering__image-label">BEINTOX · SELECTED WORK</span></div>
  <div class="service-offering__investment"><span class="service-offering__investment-label">Project investment</span>
    <p>Every project is scoped around your goals, deliverables, and timeline. We’ll recommend the right approach before work begins.</p>
    <a class="btn btn--gold btn--s" href="contact.html">Discuss this service {ARROW}</a></div>
</aside>'''
    details = f'''<div class="service-offering__copy"><span class="service-offering__number">{i + 1:02d} <i>/</i> OUR SERVICES</span>
  <h2 class="h2">{E(title)}</h2><p class="lead">{E(description)}</p>
  <h3 class="service-offering__included-title">What’s included?</h3>
  <ul class="service-offering__included">{"".join(f"<li>{E(value)}</li>" for value in included)}</ul></div>'''
    content = f"{details}{media}" if i % 2 == 0 else f"{media}{details}"
    return f'<article class="service-offering rv" id="{E(sid)}" style="--i:{i % 2}">{content}</article>'


def industries_strip() -> str:
    colors = ["#3B5BFA", "#FF5A36", "#73C5B3", "#FFD479", "#3D5BD5", "#FFB5B5", "#6D9FDE", "#FF9F7B", "#E5A911"]
    items = "".join(f'<span class="industries-strip__item" style="--industry-color:{colors[i]}">{E(name)}<i aria-hidden="true">✳</i></span>' for i, name in enumerate(SERVICE_INDUSTRIES))
    return f'''<section class="industries-strip" aria-label="Industries we serve"><div class="wrap">
  <div class="industries-strip__frame"><p class="industries-strip__label">Industries<br>we serve</p><span class="sr-only">{E(', '.join(SERVICE_INDUSTRIES))}</span>
    <div class="industries-strip__viewport"><div class="industries-strip__track" aria-hidden="true">{items}{items}</div></div>
  </div>
</div></section>'''


def service_features_section() -> str:
    cards = "".join(f'''<article class="service-feature rv" style="--i:{i % 3}">
  <span class="service-feature__icon" aria-hidden="true"><svg viewBox="0 0 48 48" fill="none"><path d="{path}" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
  <h3>{E(title)}</h3><p>{E(copy)}</p></article>''' for i, (title, copy, path) in enumerate(SERVICE_FEATURES))
    return f'''<section class="sec service-features" aria-labelledby="service-features-title"><div class="wrap">
  <div class="service-features__heading"><span class="service-features__kicker">Features</span><h2 class="h2" id="service-features-title">Why Choose Us<br>for <em>Success?</em></h2><p class="lead">Discover how Beintox empowers your brand.</p></div>
  <div class="service-features__grid">{cards}</div>
  <div class="service-features__action"><a class="btn btn--dark" href="contact.html">Schedule a Call {ARROW}</a></div>
</div></section>'''


def service_comparison_section() -> str:
    other = "".join(f'<li><span aria-hidden="true">×</span>{E(text)}</li>' for text in SERVICE_COMPARISON["other"])
    beintox = "".join(f'<li><span aria-hidden="true">✓</span>{E(text)}</li>' for text in SERVICE_COMPARISON["beintox"])
    return f'''<section class="sec service-comparison" aria-labelledby="service-comparison-title"><div class="wrap">
  <h2 class="service-comparison__title" id="service-comparison-title">But, why would you<br>want to work <em>with us?</em></h2>
  <div class="service-comparison__grid"><article class="service-comparison__side service-comparison__side--other"><h3>Other Agencies</h3><ul>{other}</ul></article>
    <article class="service-comparison__side service-comparison__side--beintox"><h3>BEINTOX</h3><ul>{beintox}</ul></article></div>
</div></section>'''


def service_client_videos() -> str:
    def cards(clone: bool = False) -> str:
        rendered = []
        for i, (brand, poster) in enumerate(CLIENT_VIDEO_PREVIEWS):
            card_class = "client-video client-video--clone" if clone else "client-video rv"
            attrs = ' aria-hidden="true"' if clone else f' style="--i:{i}"'
            alt = "" if clone else f"{brand} project preview"
            rendered.append(f'''<article class="{card_class}"{attrs}>
  <div class="client-video__poster">{img(poster, alt, cls="client-video__image")}
    <span class="client-video__badge">VIDEO PREVIEW</span><span class="client-video__play" aria-hidden="true"><svg viewBox="0 0 20 20"><path d="M6 3.5 16 10 6 16.5z" fill="currentColor"/></svg></span>
    <div class="client-video__controls" aria-hidden="true"><span>▶</span><span>00:00</span><i></i><span>Replace with video</span></div></div>
  <div class="client-video__body"><span>CLIENT STORY</span><h3>{E(brand)}</h3><p>Video testimonial coming soon.</p></div>
</article>''')
        return "".join(rendered)

    return f'''<section class="sec client-videos" aria-labelledby="client-videos-title"><div class="wrap">
  <div class="client-videos__heading"><span class="client-videos__kicker">Our Clients</span><h2 class="h2" id="client-videos-title">Hear it directly from our <em>clients.</em></h2><p class="lead">Hear what our clients have to say. Our testimonials reflect the satisfaction our clients have in our services.</p></div>
  <div class="client-videos__viewport"><div class="client-videos__track"><div class="client-videos__set">{cards()}</div><div class="client-videos__set client-videos__set--clone" aria-hidden="true">{cards(True)}</div></div></div>
</div></section>'''

def page_services() -> str:
    offerings = "".join(service_offering(item, i) for i, item in enumerate(SERVICE_PAGE_COPY))
    body = f'''
{industries_strip()}
<section class="sec services-showcase"><div class="wrap">{offerings}</div></section>
{service_features_section()}
{service_client_videos()}
{service_comparison_section()}
<section class="sec sec--white bt" id="faq"><div class="wrap">
  <div class="split" style="align-items:start">
    <div><span class="eyebrow"><b>FAQ</b></span><h2 class="h2 mt-s">Asked <em>often.</em></h2><p class="lead mt-s">Something else on your mind? Message us on WhatsApp and we'll answer directly.</p>
    <div class="btns mt-m"><a class="btn btn--line" href="https://wa.me/{CONTACT["wa"]}" target="_blank" rel="noopener">Ask on WhatsApp</a></div></div>
    {faq_html()}
  </div>
</div></section>
{cta_band("Not sure which service you need?", "Tell us what you want to achieve and we'll recommend the right starting point.")}
'''
    return layout("services", "Services: Branding, Social Media, Performance Marketing, SEO & Web | BEINTOX",
                  "Logo design and branding, social media management, performance marketing, SEO, photography and videography, website design and development, and brand registration.", body)


VERIFIED = '<svg class="ig__tick" viewBox="0 0 40 40" aria-label="Verified"><path fill="#E8413C" d="M19.998 3.094 14.638 0l-2.972 5.15H5.432v6.354L0 14.64 3.094 20 0 25.359l5.432 3.137v5.905h5.975L14.638 40l5.36-3.094L25.358 40l3.232-5.6h6.162v-6.01L40 25.359 36.905 20 40 14.641l-5.248-3.03v-6.46h-6.419L25.358 0l-5.36 3.094Zm7.415 11.225 2.254 2.287-11.43 11.5-6.835-6.93 2.244-2.258 4.587 4.581 9.18-9.18Z"/></svg>'
IG_GRID = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="1" stroke="currentColor" stroke-width="1.8"/><path d="M9 3v18M15 3v18M3 9h18M3 15h18" stroke="currentColor" stroke-width="1.8"/></svg>'
IG_REEL = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="4" stroke="currentColor" stroke-width="1.8"/><path d="M3 8h18M8 3l3 5M14 3l3 5M10 12v5l4.5-2.5z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>'
IG_TAG = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="1.8"/><path d="M6.5 19c1-2.5 3-3.6 5.5-3.6s4.5 1.1 5.5 3.6" stroke="currentColor" stroke-width="1.8"/></svg>'


def ig_profile(c: dict) -> str:
    g = IG[c["slug"]]
    folder = c["cover"].split("/")[0]
    hl = "".join(f'<li><span class="ig__hl">{img(p, l)}</span><small>{E(l)}</small></li>' for p, l in g["highlights"])
    tiles = []
    for it in g["grid"]:
        key, cap = it.split(":", 1)
        rel = f"{folder}/{key}"
        tiles.append(f'<a class="ig__tile" href="assets/img/{src(rel)}" data-lb="{E(cap)}">{img(rel, cap)}<span>{E(cap)}</span></a>')
    return f'''<div class="ig" aria-label="{E(c["name"])} Instagram feed designed by BEINTOX">
  <div class="ig__bar"><b>{E(g["handle"])}</b>{VERIFIED}<span class="ig__dots" aria-hidden="true">•••</span></div>
  <div class="ig__head">
    <div class="ig__avatar">{img(c["logo"], c["name"] + " profile picture")}</div>
    <ul class="ig__stats"><li><b>{g["posts"]}</b><span>posts</span></li><li><b>{g["followers"]}</b><span>followers</span></li><li><b>{g["following"]}</b><span>following</span></li></ul>
  </div>
  <div class="ig__bio"><b>{E(g["name"])}</b><span class="ig__cat">{E(g["category"])}</span>{"".join(f"<span>{E(l)}</span>" for l in g["bio"])}<span class="ig__link">{E(g["link"])}</span></div>
  <div class="ig__btns"><span class="ig__btn ig__btn--blue">Follow</span><span class="ig__btn">Message</span><span class="ig__btn">Contact</span></div>
  <ul class="ig__hls">{hl}</ul>
  <div class="ig__tabs"><span class="is-on">{IG_GRID}</span><span>{IG_REEL}</span><span>{IG_TAG}</span></div>
  <div class="ig__grid" data-lb-group>{"".join(tiles)}</div>
</div>'''


def case_counts(c: dict) -> dict:
    n = {"identity": 0, "posts": 0, "applications": 0}
    for sid, _l, _t, _d, kind, items in c["sections"]:
        if kind == "posts":
            n["posts"] += len(items)
        elif sid == "identity":
            n["identity"] += len(items)
        else:
            n["applications"] += len(items)
    return n


def page_portfolio() -> str:
    blocks = []
    for i, c in enumerate(CASES):
        n = case_counts(c)
        sw = "".join(f'<i title="{E(nm)}" style="background:{h}"></i>' for h, nm in c["palette"])
        svc_links = "".join(f'<a class="tag" href="services.html#{sid}">{E(svc_by_id(sid)[1])}</a>' for sid in c["services"])
        fonts = f'{c["fonts"][0]} / {c["fonts"][1]}' if c["fonts"] else "Custom wordmark"
        g = IG[c["slug"]]
        blocks.append(f'''<section class="pf{" bt" if i else ""}" id="{c["slug"]}">
  <div class="pf__info">
    <span class="eyebrow"><b>{i + 1:02d}</b> {E(c["sector"])}</span>
    <h2 class="h2 mt-s"><a href="case-study-{c["slug"]}.html">{E(c["name"])}</a></h2>
    <p class="lead mt-s">{E(c["summary"])}</p>
    <dl class="spec mt-m">
      <div><dt>Instagram</dt><dd>@{E(g["handle"])} · {g["followers"]} followers</dd></div>
      <div><dt>Brand book</dt><dd>{n["identity"]} pages shown</dd></div>
      <div><dt>Social creatives</dt><dd>{n["posts"]} designed posts</dd></div>
      <div><dt>Applications</dt><dd>{n["applications"]} touchpoints</dd></div>
      <div><dt>Typography</dt><dd>{E(fonts)}</dd></div>
      <div><dt>Palette</dt><dd><span class="spec__sw">{sw}</span></dd></div>
    </dl>
    <span class="eyebrow" style="display:block;margin:22px 0 10px">Services delivered</span>
    <div class="tags" style="margin:0">{svc_links}</div>
    <div class="btns mt-m"><a class="btn btn--gold" href="case-study-{c["slug"]}.html">Read the case study {ARROW}</a><a class="btn btn--line" href="case-studies.html">All case studies</a></div>
  </div>
  {ig_profile(c)}
</section>''')
    filt = "".join(f'<li><a href="#{c["slug"]}">{img(c["logo"], "")}<span>{E(c["name"])}</span></a></li>' for c in CASES)
    body = f'''
<section class="phero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Portfolio</span></nav>
  <h1 class="h1">Brands we've <em>built.</em></h1>
  <p class="lead">Four complete brand systems: identity, guidelines, packaging, launch campaigns and the Instagram feeds we design and run.</p>
</div></section>
<nav class="subnav subnav--brands" aria-label="Brands"><div class="wrap"><ul>{filt}</ul></div></nav>
<section class="sec" style="padding-top:40px"><div class="wrap">
  {"".join(blocks)}
</div></section>
{cta_band("Your brand could be <em>next.</em>")}
'''
    return layout("portfolio", "Portfolio: Brand Identity, Packaging & Instagram Work | BEINTOX",
                  "Portfolio: Tomgai Chinese, Twenty Two, Khyber Sajji and Shehar-e-Lazzat. Brand identities, guidelines, packaging, launch campaigns and Instagram feeds.", body)


def page_case_studies() -> str:
    rows = []
    for i, c in enumerate(CASES):
        n = case_counts(c)
        delivered = "".join(f"<li>{ICON['check']}<span>{E(svc_by_id(sid)[1])}</span></li>" for sid in c["services"])
        rows.append(f'''<a class="cs" href="case-study-{c["slug"]}.html" style="--brand:#1F1F1F">
  <div class="cs__img">{img(c["cover"], f'{c["name"]} case study', eager=i == 0)}<span class="cs__logo">{img(c["logo"], c["name"] + " logo")}</span></div>
  <div class="cs__body">
    <div class="cs__top"><span class="eyebrow"><b>Case {i + 1:02d}</b> {E(c["sector"])}</span></div>
    <h2 class="h2">{E(c["name"])}</h2>
    <div class="cs__brief"><span class="eyebrow">The brief</span><p>{E(c["brief"])}</p></div>
    <div class="cs__cols">
      <div><span class="eyebrow">What we delivered</span><ul class="checks">{delivered}</ul></div>
      <dl class="cs__nums">
        <div><dt>{n["identity"]}</dt><dd>Brand book pages</dd></div>
        <div><dt>{n["posts"]}</dt><dd>Social creatives</dd></div>
        <div><dt>{n["applications"]}</dt><dd>Applications</dd></div>
      </dl>
    </div>
    <span class="btn btn--gold cs__btn">Read the case study {ARROW}</span>
  </div>
</a>''')
    body = f'''
<section class="phero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Case studies</span></nav>
  <h1 class="h1">How we built <em>each brand.</em></h1>
  <p class="lead">The brief, the idea and everything we delivered: identity, guidelines, packaging, campaigns and content. Pick a project to read the full story.</p>
</div></section>
<section class="sec"><div class="wrap"><div class="cs-list">{"".join(rows)}</div></div></section>
{cta_band("Want a case study <em>like these?</em>")}
'''
    return layout("case-studies", "Case Studies: Branding & Marketing Projects | BEINTOX",
                  "Case studies from BEINTOX: the brief, the idea and the full deliverables for Tomgai Chinese, Twenty Two, Khyber Sajji and Shehar-e-Lazzat.", body)


def page_case(c: dict) -> str:
    folder = c["cover"].split("/")[0]
    facts = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in c["facts"])
    sub = "".join(f'<li><a href="#{s[0]}">{s[1]}</a></li>' for s in c["sections"])
    tags = "".join(f'<span class="tag">{E(t)}</span>' for t in c["tags"])
    sw = "".join(f'<div class="swatch"><i style="background:{h}"></i>{E(n)}</div>' for h, n in c["palette"])
    fonts = ""
    if c["fonts"]:
        fonts = f'<div class="mt-m"><span class="eyebrow">Typography</span><p class="mt-s small"><b>{c["fonts"][0]}</b> primary · <b>{c["fonts"][1]}</b> secondary</p></div>'
    secs = []
    for i, (sid, label, title, lead, kind, items) in enumerate(c["sections"]):
        if kind == "posts":
            media = post_grid(items, folder, "posts posts--3" if len(items) in (6, 9) else "posts posts--4" if len(items) in (4, 8) else "posts")
        elif kind == "gallery2":
            media = gallery(items, folder, "gallery gallery--2")
        elif kind == "gallery4":
            media = gallery(items, folder, "gallery gallery--4")
        else:
            media = gallery(items, folder)
        bg = " sec--white bt" if i % 2 == 0 else ""
        secs.append(f'''<section class="sec{bg}" id="{sid}"><div class="wrap">
  {head_block(f"<b>{i + 2:02d}</b> {label}", title, lead)}
  {media}
</div></section>''')
    idx = CASES.index(c)
    nxt = CASES[(idx + 1) % len(CASES)]
    overview_media = f'<div class="ig-wrap">{ig_profile(c)}</div>'
    body = f'''
<section class="chero" style="--brand:#1F1F1F"><div class="wrap">
  <div class="chero__copy">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><a href="case-studies.html">Case studies</a><span>/</span><span>{E(c["name"])}</span></nav>
    <h1 class="h1">{E(c["name"])}</h1>
    <p class="lead">{E(c["summary"])}</p>
    <div class="tags" style="margin-top:18px">{tags}</div>
  </div>
  <div class="chero__img">{img(c["hero"], c["name"] + " brand applications", eager=True)}</div>
</div></section>
<div class="sec--white" style="border-bottom:1px solid var(--line)"><div class="wrap"><dl class="facts" style="border:0">{facts}</dl></div></div>
<nav class="subnav" aria-label="Case study sections"><div class="wrap"><ul><li><a href="#overview">Overview</a></li>{sub}</ul></div></nav>

<section class="sec" id="overview"><div class="wrap">
  <div class="split">
    <div><span class="eyebrow"><b>01</b> Overview</span><h2 class="h2 mt-s">The <em>idea.</em></h2>
      <div class="prose mt-m">{"".join(f"<p>{E(p)}</p>" for p in c["story"])}</div>
      <div class="mt-l"><span class="eyebrow">Colour</span><div class="palette">{sw}</div></div>{fonts}
    </div>
    {overview_media}
  </div>
</div></section>
{"".join(secs)}
<section class="sec--white bt"><div class="wrap next">
  <a class="link" href="case-studies.html">All case studies</a><span class="eyebrow">Next case study</span>
  <a class="h2" href="case-study-{nxt["slug"]}.html">{E(nxt["name"])} {ARROW}</a>
</div></section>
{cta_band()}
'''
    return layout(f"case:{c['slug']}", f"{c['name']}: {c['sector'].split(' · ')[0]} Branding Case Study | BEINTOX",
                  f"{c['name']} case study by BEINTOX: {', '.join(c['tags']).lower()}. {c['summary']}", body)


def team_html() -> str:
    n, role, photo, bio = FOUNDER
    members = []
    for name, r, ph in TEAM:
        face = img(ph, f"{name}, {r} at BEINTOX") if ph else f'<span class="member__ini" aria-hidden="true">{"".join(w[0] for w in name.split()[:2])}</span>'
        members.append(f'<li class="member rv" tabindex="0" style="--i:{len(members)}"><div class="member__ph">{face}</div><b>{E(name)}</b><span>{E(r)}</span></li>')
    socials = (
        ("Facebook", "https://www.facebook.com/ali.imtiaz.7564", ICON["fb"]),
        ("Instagram", "https://www.instagram.com/ali_imtiaz1122/?hl=en", ICON["ig"]),
        ("LinkedIn", "https://www.linkedin.com/in/ali-imtiaz-a683231b7/", ICON["linkedin"]),
    )
    social_links = "".join(f'<a href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Ali Imtiaz on {label}">{icon}</a>' for label, url, icon in socials)
    return f'''<div class="founder">
  <div class="founder__frame">
    <div class="founder__ring" aria-hidden="true"></div>
    <div class="founder__ph" tabindex="0" data-tilt>{img(photo, f"{n}, {role} of BEINTOX")}<span class="founder__shine" aria-hidden="true"></span></div>
    <span class="founder__badge"><i></i>{E(role)}</span>
  </div>
  <div class="founder__txt"><span class="eyebrow"><b>Leadership</b></span>
    <blockquote class="h2 mt-s">“{E(bio)}”</blockquote>
    <p class="founder__name"><b>{E(n)}</b><span>{E(role)}</span></p>
    <nav class="founder__socials" aria-label="Ali Imtiaz social profiles">{social_links}</nav>
  </div>
</div>
<ul class="team">{"".join(members)}</ul>'''


def page_about() -> str:
    body = f'''
<section class="phero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>About</span></nav>
  <h1 class="h1">Beyond ordinary. <em>Built to be noticed.</em></h1>
  <p class="lead">BEINTOX offers logo design and branding, social media management, performance marketing, SEO, photography and videography, website design and development, and brand registration.</p>
</div></section>

<section class="sec sec--white"><div class="wrap">
  <div class="split">
    <div>
      <span class="eyebrow"><b>01</b> The BEINTOX philosophy</span>
      <h2 class="h2 mt-s">A brand isn't made by a logo or a post. It's made by a <em>clear idea.</em></h2>
      <div class="prose mt-m">
        <p>A brand is a clear idea, a consistent look and a message people can trust. Being online isn't enough anymore: brands need to be seen, understood and remembered.</p>
        <p>We combine brand identity, social media, paid marketing, SEO, photography, web and brand registration so your brand can grow with one connected team.</p>
      </div>
    </div>
    <div class="split__media" style="aspect-ratio:4/3">{img("brand/chess-hand", "A hand moving a gold king on a chessboard", eager=True)}</div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  {head_block("<b>02</b> What we believe", "Be seen. Be understood. <em>Be remembered.</em>")}
  {beliefs_html()}
</div></section>

<section class="sec sec--white bt"><div class="wrap">
  <div class="split">
    <div class="split__media" style="aspect-ratio:16/10">{img("shehar/app-mockups", "Shehar-e-Lazzat brand mockups")}</div>
    <div>
      <span class="eyebrow"><b>03</b> What we're building</span>
      <h2 class="h2 mt-s">From “just another name” to a brand with <em>real presence.</em></h2>
      <div class="prose mt-m"><p>We help businesses turn ideas into identities, and identities into lasting customer relationships. We don't create content just for today. We build brands made to last.</p></div>
      {checks(["Logo design and branding", "Social media management", "Performance marketing and SEO", "Web, photography and brand registration"])}
      <div class="btns mt-m"><a class="btn btn--dark" href="portfolio.html">See the work {ARROW}</a><a class="btn btn--line" href="services.html">Our services</a></div>
    </div>
  </div>
</div></section>

<section class="sec" id="team"><div class="wrap">
  {head_block("<b>04</b> The team", "The people behind <em>the work.</em>", "Brand identity, social media, performance marketing, photo and video, and websites from one close team.")}
  {team_html()}
</div></section>

<section class="sec sec--white bt"><div class="wrap">
  {head_block("<b>05</b> Why BEINTOX", "Being memorable is what <em>makes brands grow.</em>", "Every day your customers see hundreds of brands, and most are forgotten in seconds. We shape how yours looks, sounds and feels, so people notice you, trust you and come back.")}
  {why_html()}
</div></section>

<section class="sec"><div class="wrap">
  {head_block("<b>06</b> How we work", "One team, one process, <em>no handoffs.</em>")}
  {steps_html([("Discover", "Business, audience and competitor research to find what makes you worth choosing."),
                ("Define", "Positioning, personality and messaging: the brief every design decision answers to."),
                ("Design", "Brand identity, social content and websites built as one connected system."),
                ("Grow", "Launch, measure and refine across social, ads and web.")])}
</div></section>
{cta_band()}
'''
    return layout("about", "About BEINTOX: Brand & Marketing Studio",
                  "BEINTOX offers logo design and branding, social media management, performance marketing, SEO, photography and videography, website design and development, and brand registration.", body)


def page_contact() -> str:
    chips = "".join(f'<label><input type="checkbox" name="services" value="{E(s[1])}"><span>{E(s[1])}</span></label>' for s in SERVICES)
    body = f'''
<section class="sec"><div class="wrap contact contact--talk">
  <div class="contact__intro">
    <span class="eyebrow">Contact us</span>
    <h2 class="contact__headline">Let's<br><em>Talk!</em></h2>
    <p class="lead">Tell us about your business and what you need. We'll reply with a few questions and a clear proposal.</p>
    <div class="contact__quick">
      <a href="https://wa.me/{CONTACT["wa"]}" target="_blank" rel="noopener">{ICON["wa"]} WhatsApp</a>
      <a href="mailto:{CONTACT["email"]}">{ICON["mail"]} Email us</a>
      <a href="tel:{CONTACT["tel"]}">{ICON["phone"]} Call us</a>
    </div>
  </div>
  <form class="card form" id="brief" data-wa="{CONTACT["wa"]}" data-email="{CONTACT["email"]}">
    <div class="field"><label for="f-name">Your name *</label><input id="f-name" name="name" required autocomplete="name"></div>
    <div class="field"><label for="f-biz">Business / brand</label><input id="f-biz" name="business" autocomplete="organization"></div>
    <div class="field field--full"><label for="f-contact">Phone or email *</label><input id="f-contact" name="contact" required autocomplete="email"></div>
    <div class="field field--full"><span style="font-size:13px;font-weight:600">What do you need?</span><div class="chips">{chips}</div></div>
    <div class="field field--full"><label for="f-time">Timeline</label><select id="f-time" name="timeline"><option>As soon as possible</option><option>Within 1 month</option><option>1–3 months</option><option>Just exploring</option></select></div>
    <div class="field field--full"><label for="f-msg">About the project</label><textarea id="f-msg" name="message" placeholder="Where is your brand today, and where do you want it to go?"></textarea></div>
    <div class="form__foot">
      <button class="btn btn--gold" type="submit" value="whatsapp">Send via WhatsApp {ARROW}</button>
      <button class="btn btn--line" type="submit" value="email">Send via email</button>
      <span class="form__note">Opens WhatsApp or your email app with your brief filled in.</span>
    </div>
  </form>
  <aside class="card contact__next"><span class="eyebrow">What happens next</span>
      <ol class="checks">{"".join(f"<li>{ICON['check']}<span>{t}</span></li>" for t in ["We read your brief and reply with a few questions.", "A short call to understand goals, audience and budget.", "You receive a scoped proposal with timeline and cost.", "Kick-off, and discovery begins."])}</ol>
  </aside>
</div></section>
'''
    return layout("contact", "Contact BEINTOX: Request a Proposal",
                  f"Request a proposal from BEINTOX. WhatsApp or call {CONTACT['phone']}, email {CONTACT['email']}.", body)


def page_404() -> str:
    body = f'''<section class="sec err"><div class="wrap"><span class="eyebrow">404</span><h1 class="h1 mt-s">This page <em>doesn't exist.</em></h1>
<p class="lead mt-s" style="margin-inline:auto">The link may be old or mistyped.</p><div class="btns mt-m" style="justify-content:center"><a class="btn btn--dark" href="index.html">Back to home</a><a class="btn btn--line" href="portfolio.html">See our work</a></div></div></section>'''
    return layout("404", "Page not found | BEINTOX", "Page not found.", body)


# =====================================================================
# BUILD
# =====================================================================

def main() -> None:
    pages = {"index": page_home(), "services": page_services(), "portfolio": page_portfolio(), "case-studies": page_case_studies(),
             "about": page_about(), "contact": page_contact(), "404": page_404()}
    for c in CASES:
        pages[f"case-study-{c['slug']}"] = page_case(c)
    for name, out in pages.items():
        (ROOT / f"{name}.html").write_text(out, encoding="utf-8")
    print(f"Built {len(pages)} pages: {', '.join(sorted(pages))}")


if __name__ == "__main__":
    main()

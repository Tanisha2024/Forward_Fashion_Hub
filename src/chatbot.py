from pathlib import Path
import os
import re

import pandas as pd
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq


# ==========================================
# 1. Project paths and environment
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")


# ==========================================
# 2. Load data
# ==========================================

faq = pd.read_csv(
    PROJECT_ROOT / "data" / "faq.csv"
)

products = pd.read_csv(
    PROJECT_ROOT / "data" / "products.csv"
)
print(
    products[
        (products["color"].str.lower() == "black") &
        (products["category"].str.lower().isin(["top", "t-shirt", "polo"]))
    ][["product_id", "name", "category", "price", "color"]]
)

# ==========================================
# 3. Load embedding model
# ==========================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==========================================
# 4. Groq client
# ==========================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
# ==========================================
# 5. Create FAQ documents
# ==========================================

faq_documents = []

for _, row in faq.iterrows():

    document = f"""
Question: {row['question']}

Answer: {row['answer']}
"""

    faq_documents.append(document.strip())


# ==========================================
# 6. Create product documents
# ==========================================

product_documents = []

for _, row in products.iterrows():

    document = f"""
Product: {row['name']}

Category: {row['category']}

Description: {row['description']}

Price: ₹{row['price']}

Color: {row['color']}

Available sizes: {row['size'].replace('|', ', ')}

Material: {row['material']}

Occasion: {row['occasion'].replace('|', ', ')}

Style: {row['style']}
"""

    product_documents.append(document.strip())


# ==========================================
# 7. Create embeddings
# ==========================================

faq_embeddings = model.encode(
    faq_documents
)

product_embeddings = model.encode(
    product_documents
)
# ==========================================
# 8. FAQ retrieval
# ==========================================

def retrieve_faq(query, top_k=3):

    query_embedding = model.encode(query)

    similarities = cosine_similarity(
        [query_embedding],
        faq_embeddings
    )[0]

    top_indices = similarities.argsort()[::-1][:top_k]

    results = []

    for index in top_indices:

        results.append({
            "document": faq_documents[index],
            "score": similarities[index]
        })

    return results


# ==========================================
# 9. Product retrieval
# ==========================================

def retrieve_products(query, top_k=3):

    query_embedding = model.encode(query)

    similarities = cosine_similarity(
        [query_embedding],
        product_embeddings
    )[0]

    top_indices = similarities.argsort()[::-1][:top_k]

    results = []

    for index in top_indices:
        print(
            products.iloc[index]["product_id"],
            products.iloc[index]["name"],
            "Score:",
            round(similarities[index], 4)
)

        results.append({
            "document": product_documents[index],
            "score": similarities[index],
            "index": index
        })

    return results
# ==========================================
# 10. Product filtering
# ==========================================

def filter_products(
    max_price=None,
    color=None,
    occasion=None,
    style=None,
    category=None
):

    filtered = products.copy()

    # Price
    if max_price is not None:
        filtered = filtered[
            filtered["price"] <= max_price
        ]

    # Color
    if color is not None:
        filtered = filtered[
            filtered["color"].str.lower() == color.lower()
        ]

    # Occasion
    if occasion is not None:
        filtered = filtered[
            filtered["occasion"].str.lower().str.contains(
                occasion.lower(),
                na=False
            )
        ]

    # Style
    if style is not None:
        filtered = filtered[
            filtered["style"].str.lower() == style.lower()
        ]

    # Category
    # Category
    if category is not None:

        if isinstance(category, list):
            filtered = filtered[
                filtered["category"].str.lower().isin(
                    [c.lower() for c in category]
            )
        ]

        else:
            filtered = filtered[
                filtered["category"].str.lower() == category.lower()
        ]

    return filtered


# ==========================================
# 11. Extract price
# ==========================================

def extract_max_price(query):

    query = query.lower()

    patterns = [
        r"under\s*₹?\s*(\d+)",
        r"below\s*₹?\s*(\d+)",
        r"less than\s*₹?\s*(\d+)",
        r"upto\s*₹?\s*(\d+)",
        r"up to\s*₹?\s*(\d+)"
    ]

    for pattern in patterns:

        match = re.search(pattern, query)

        if match:
            return int(match.group(1))

    return None


# ==========================================
# 12. Extract color
# ==========================================

def extract_color(query):

    query = query.lower()

    colors = products["color"].dropna().unique()

    for color in colors:

        if color.lower() in query:
            return color

    return None


# ==========================================
# 13. Extract occasion
# ==========================================

def extract_occasion(query):

    query = query.lower()

    occasions = [
        "casual",
        "college",
        "office",
        "formal",
        "summer",
        "vacation",
        "date",
        "party",
        "winter"
    ]

    for occasion in occasions:

        if occasion in query:
            return occasion.title()

    return None


# ==========================================
# 14. Extract style
# ==========================================

def extract_style(query):

    query = query.lower()

    styles = products["style"].dropna().unique()

    for style in styles:

        if style.lower() in query:
            return style

    return None


# ==========================================
# 15. Extract category
# ==========================================

def extract_category(query):

    query = query.lower()

    category_map = {
        "shirt": "Shirt",
        "shirts": "Shirt",
        "hoodie": "Hoodie",
        "hoodies": "Hoodie",
        "jeans": "Jeans",
        "trouser": "Trousers",
        "trousers": "Trousers",
        "dress": "Dress",
        "dresses": "Dress",
        "t-shirt": "T-Shirt",
        "t-shirts": "T-Shirt",
        "jacket": "Jacket",
        "jackets": "Jacket",
        "top": "Top",
        "tops": "Top",
        "shoe": "Shoes",
        "shoes": "Shoes",
        "pant": "Pants",
        "pants": "Pants",
        "polo": "Polo",
        "sweater": "Sweater",
        "sweaters": "Sweater",
        "blazer": "Blazer",
        "blazers": "Blazer",
        "skirt": "Skirt",
        "skirts": "Skirt"
    }

    for word, category in category_map.items():

        if word in query:
            return category

    return None


# ==========================================
# 16. Extract all filters
# ==========================================

def extract_filters(query):

    return {
        "max_price": extract_max_price(query),
        "color": extract_color(query),
        "occasion": extract_occasion(query),
        "style": extract_style(query),
        "category": extract_category(query)
    }
# ==========================================
# 17. Filtered product retrieval
# ==========================================

def retrieve_filtered_products(
    query,
    max_price=None,
    color=None,
    occasion=None,
    style=None,
    category=None,
    top_k=3
):

    filtered = filter_products(
        max_price=max_price,
        color=color,
        occasion=occasion,
        style=style,
        category=category
    )

    if filtered.empty:
        return []

    # If the user asks for "all", return every matching product
    if "all" in query.lower():
        results = []

        for index in filtered.index:

            results.append({
                "product_id": products.iloc[index]["product_id"],
                "name": products.iloc[index]["name"],
                "price": products.iloc[index]["price"],
                "color": products.iloc[index]["color"],
                "score": 1.0
            })

        return results

    # Normal filtered semantic retrieval
    filtered_indices = filtered.index.tolist()

    query_embedding = model.encode(query)

    similarities = cosine_similarity(
        [query_embedding],
        product_embeddings[filtered_indices]
    )[0]

    top_positions = similarities.argsort()[::-1][:top_k]

    results = []

    for position in top_positions:

        original_index = filtered_indices[position]

        results.append({
            "product_id": products.iloc[original_index]["product_id"],
            "name": products.iloc[original_index]["name"],
            "price": products.iloc[original_index]["price"],
            "color": products.iloc[original_index]["color"],
            "score": similarities[position]
        })

    return results

# ==========================================
# 18. Natural-language product search
# ==========================================

def search_products(query):

    filters = extract_filters(query)

    results = retrieve_filtered_products(
        query=query,
        max_price=filters["max_price"],
        color=filters["color"],
        occasion=filters["occasion"],
        style=filters["style"],
        category=filters["category"],
        top_k=3
    )

    return results
# ==========================================
# 19. Build FAQ context
# ==========================================

def build_faq_context(results):

    context = ""

    for result in results:

        context += f"""
{result['document']}
Similarity Score: {result['score']:.2f}

"""

    return context.strip()


# ==========================================
# 20. Build product context
# ==========================================

def build_product_context(results):

    context = ""

    for result in results:

        if "document" in result:

            context += f"""
{result['document']}
Similarity Score: {result['score']:.2f}

"""

        else:

            product = products[
                products["product_id"] == result["product_id"]
            ].iloc[0]

            context += f"""
Product ID: {product['product_id']}
Product: {product['name']}
Category: {product['category']}
Description: {product['description']}
Price: ₹{product['price']}
Color: {product['color']}
Available sizes: {product['size'].replace('|', ', ')}
Material: {product['material']}
Occasion: {product['occasion'].replace('|', ', ')}
Style: {product['style']}
Similarity Score: {result['score']:.2f}

"""

    return context.strip()


# ==========================================
# 21. RAG prompt
# ==========================================

def build_rag_prompt(query, context):

    prompt = f"""
You are an AI shopping assistant for Fashion Forward Hub.

Use ONLY the information provided in the context.

Answer the user's question naturally and helpfully.
Do not simply copy the context.
Do not mention similarity scores.
Do not invent product information.

If products are found, clearly mention:
- Product name
- Price
- Color
- Any other relevant information available in the context

User question:
{query}

Context:
{context}

Write a concise shopping-assistant response.
"""

    return prompt.strip()


# ==========================================
# 22. Generate LLM answer
# ==========================================

def generate_answer(prompt):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content
# ==========================================
# 23. FAQ answer
# ==========================================

def answer_faq(query):

    results = retrieve_faq(query, top_k=3)

    # Confidence guard
    if not results or results[0]["score"] < 0.60:
        return (
            "I don't have enough information about that "
            "in the store's FAQ."
        )

    context = build_faq_context(results)

    prompt = build_rag_prompt(
        query,
        context
    )

    return generate_answer(prompt)


# ==========================================
# 24. Product answer
# ==========================================

def answer_product(query):

    results = retrieve_products(
        query,
        top_k=3
    )

    # Confidence guard
    if not results or results[0]["score"] < 0.60:
        return (
            "I couldn't find a matching product "
            "in the current catalog."
        )

    context = build_product_context(results)

    prompt = build_rag_prompt(
        query,
        context
    )

    return generate_answer(prompt)


# ==========================================
# 25. Filtered product answer
# ==========================================

def answer_search(query):

    results = search_products(query)

    if not results:
        return (
            "I couldn't find any products matching "
            "your requirements."
        )

    context = build_product_context(results)

    prompt = build_rag_prompt(
        query,
        context
    )

    return generate_answer(prompt)
# ==========================================
# 26. Build outfit context
# ==========================================

def build_outfit_context(outfit_products):

    context = ""

    for _, product in outfit_products.iterrows():

        context += f"""
Product ID: {product['product_id']}
Product: {product['name']}
Category: {product['category']}
Price: ₹{product['price']}
Color: {product['color']}
Material: {product['material']}
Occasion: {product['occasion'].replace('|', ', ')}
Style: {product['style']}

"""

    return context.strip()


# ==========================================
# 27. Outfit prompt
# ==========================================

def build_outfit_prompt(query, products_context):

    prompt = f"""
You are an AI fashion shopping assistant for Fashion Forward Hub.

The user wants an outfit recommendation.

Use ONLY the products provided in the context.
Do not invent products, prices, colors, sizes, or other details.

Create a practical outfit by combining compatible products
from the available options.

For each recommended product, mention:
- Product name
- Price
- Color

Also give a short explanation of why the combination
works for the requested occasion or style.

User request:
{query}

Available products:
{products_context}

Give a concise and natural outfit recommendation.
"""

    return prompt.strip()


# ==========================================
# 28. Retrieve outfit products
# ==========================================

def retrieve_outfit_products(
    occasion=None,
    style=None,
    max_price=None
):

    filtered = products.copy()

    # Occasion is a hard requirement
    if occasion is not None:

        filtered = filtered[
            filtered["occasion"].str.lower().str.contains(
                occasion.lower(),
                na=False
            )
        ]

    # Budget is a hard requirement
    if max_price is not None:

        filtered = filtered[
            filtered["price"] <= max_price
        ]

    if filtered.empty:
        return filtered

    # Style is a preference
    if style is not None:

        filtered["style_match"] = (
            filtered["style"].str.lower()
            == style.lower()
        )

        filtered = filtered.sort_values(
            "style_match",
            ascending=False
        )

    selected = []

    # Dresses can be complete outfits
    dresses = filtered[
        filtered["category"] == "Dress"
    ]

    if not dresses.empty:

        selected.append(dresses.iloc[0])

        return pd.DataFrame(selected)

    # Tops
    tops = filtered[
        filtered["category"].isin(
            [
                "Shirt",
                "T-Shirt",
                "Hoodie",
                "Polo",
                "Top"
            ]
        )
    ]

    # Bottoms
    bottoms = filtered[
        filtered["category"].isin(
            [
                "Jeans",
                "Pants",
                "Trousers",
                "Skirt"
            ]
        )
    ]

    # Shoes
    shoes = filtered[
        filtered["category"] == "Shoes"
    ]

    # Layers
    layers = filtered[
        filtered["category"].isin(
            [
                "Jacket",
                "Blazer"
            ]
        )
    ]

    # Find top + bottom
    if not tops.empty and not bottoms.empty:

        found_combination = False

        for _, top in tops.iterrows():

            for _, bottom in bottoms.iterrows():

                total = (
                    top["price"]
                    + bottom["price"]
                )

                if (
                    max_price is None
                    or total <= max_price
                ):

                    selected = [
                        top,
                        bottom
                    ]

                    found_combination = True
                    break

            if found_combination:
                break

    # Add shoes if budget allows
    if selected and not shoes.empty:

        current_total = sum(
            product["price"]
            for product in selected
        )

        for _, shoe in shoes.iterrows():

            if (
                max_price is None
                or current_total + shoe["price"]
                <= max_price
            ):

                selected.append(shoe)
                break

    # Add layer if budget allows
    if selected and not layers.empty:

        current_total = sum(
            product["price"]
            for product in selected
        )

        for _, layer in layers.iterrows():

            if (
                max_price is None
                or current_total + layer["price"]
                <= max_price
            ):

                selected.append(layer)
                break

    result = pd.DataFrame(selected)

    if "style_match" in result.columns:

        result = result.drop(
            columns=["style_match"]
        )

    return result


# ==========================================
# 29. Generate outfit answer
# ==========================================

def answer_outfit(
    query,
    occasion=None,
    style=None,
    max_price=None
):

    outfit_products = retrieve_outfit_products(
        occasion=occasion,
        style=style,
        max_price=max_price
    )

    if outfit_products.empty:

        return (
            "I couldn't find enough products "
            "for this outfit."
        )

    context = build_outfit_context(
        outfit_products
    )

    prompt = build_outfit_prompt(
        query,
        context
    )

    return generate_answer(prompt)
# ==========================================
# 30. Detect user intent
# ==========================================

def detect_intent(query):

    query = query.lower()

    # Recommendation / outfit requests
    recommendation_keywords = [
        "outfit",
        "look",
        "dress me",
        "style me",
        "suggest",
        "recommend",
        "recommendation"
    ]

    faq_keywords = [
        "return",
        "exchange",
        "shipping",
        "delivery",
        "payment",
        "cancel",
        "refund",
        "discount",
        "track order"
    ]

    search_keywords = [
        "show me",
        "find",
        "looking for",
        "under",
        "below",
        "upto",
        "up to",
        "less than"
    ]

    # Check recommendation requests first
    for keyword in recommendation_keywords:

        if keyword in query:
            return "outfit"

    # FAQ
    for keyword in faq_keywords:

        if keyword in query:
            return "faq"

    # Product search
    for keyword in search_keywords:

        if keyword in query:
            return "search"

    # Default
    return "product"



# ==========================================
# 31. Main chatbot with basic context
# ==========================================

last_outfit_products = None
# ==========================================
# Product compatibility engine
# ==========================================

def find_compatible_footwear(outfit_products):
    if outfit_products is None or outfit_products.empty:
        return []

    outfit_occasions = set()
    outfit_styles = set()

    for _, product in outfit_products.iterrows():
        occasions = str(product["occasion"]).split("|")

        for occasion in occasions:
            outfit_occasions.add(occasion.strip().lower())

        outfit_styles.add(
            str(product["style"]).strip().lower()
        )

    footwear_categories = [
        "Shoes",
        "Heels",
        "Boots",
        "Sandals"
    ]

    footwear = products[
        products["category"].isin(footwear_categories)
    ].copy()

    if footwear.empty:
        return []

    scored_products = []

    for _, shoe in footwear.iterrows():

        score = 0

        shoe_occasions = {
            x.strip().lower()
            for x in str(shoe["occasion"]).split("|")
        }

        shoe_style = str(
            shoe["style"]
        ).strip().lower()

        # Occasion compatibility
        occasion_matches = (
            outfit_occasions & shoe_occasions
        )

        score += len(occasion_matches) * 3

        # Same style
        if shoe_style in outfit_styles:
            score += 2

        # Party outfit → party footwear
        if (
            "party" in outfit_occasions
            and shoe_style == "partywear"
        ):
            score += 4

        # Party outfit → heels/party sandals
        if (
            "party" in outfit_occasions
            and shoe["category"] in ["Heels", "Sandals"]
        ):
            score += 2

        # Formal outfit → formal/classic footwear
        formal_styles = {
            "formal",
            "classic",
            "smart casual"
        }

        if (
            "formal" in outfit_occasions
            and shoe_style in formal_styles
        ):
            score += 2

        # Casual outfit → minimal footwear
        if (
            "casual" in outfit_occasions
            and shoe_style == "minimal"
        ):
            score += 2

        scored_products.append({
            "product_id": shoe["product_id"],
            "name": shoe["name"],
            "category": shoe["category"],
            "price": shoe["price"],
            "color": shoe["color"],
            "score": score
        })

    scored_products.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scored_products

def chat(query):

    global last_outfit_products

    intent = detect_intent(query)

    # --------------------------------------
    # Follow-up footwear question
    # --------------------------------------

    footwear_keywords = [
    "footwear",
    "shoes",
    "shoe",
    "sneakers",
    "loafers",
    "heels",
    "heel",
    "boots",
    "boot",
    "sandals",
    "sandal"
]

    follow_up_words = [
        "with it",
        "with this",
        "go with it",
        "go with this",
        "wear with it",
        "wear with this"
    ]

    is_footwear_followup = (
        any(word in query.lower()
            for word in footwear_keywords)
        and
        any(word in query.lower()
            for word in follow_up_words)
    )

    if is_footwear_followup and last_outfit_products is not None:

        compatible_shoes = find_compatible_footwear(
    last_outfit_products
)

# Respect the footwear type requested by the user
        query_lower = query.lower()

        if "sneaker" in query_lower or "shoe" in query_lower:
            compatible_shoes = [
                shoe for shoe in compatible_shoes
                if shoe["category"] == "Shoes"
    ]

        elif "heel" in query_lower:
            compatible_shoes = [
                shoe for shoe in compatible_shoes
                if shoe["category"] == "Heels"
    ]

        elif "boot" in query_lower:
            compatible_shoes = [
                shoe for shoe in compatible_shoes
                if shoe["category"] == "Boots"
    ]

        elif "sandal" in query_lower:
            compatible_shoes = [
                shoe for shoe in compatible_shoes
                if shoe["category"] == "Sandals"
    ]

        if not compatible_shoes:
            return "I couldn't find suitable footwear in the current catalog."

    # Take the best 2 compatible footwear options
        top_shoes = compatible_shoes[:2]

        footwear_context = ""

        for shoe in top_shoes:
            footwear_context += f"""
    Product ID: {shoe['product_id']}
    Product: {shoe['name']}
    Category: {shoe['category']}
    Price: ₹{shoe['price']}
    Color: {shoe['color']}
    Compatibility Score: {shoe['score']}
    """

        footwear_prompt = f"""
    You are an AI fashion shopping assistant for Fashion Forward Hub.

    The user previously received an outfit recommendation.

    Now they are asking what footwear would go with that outfit.

    Use ONLY the footwear options provided below.

    Do not invent footwear.
    Do not mention compatibility scores.

    For each option, mention:
    - Product name
    - Price
    - Color
    - Why it works with the outfit

    User question:
    {query}

    Compatible footwear:
    {footwear_context}

    Give a concise and natural recommendation.
    """

        return generate_answer(footwear_prompt)

    # --------------------------------------
    # Normal product question
    # --------------------------------------

    if intent == "faq":
        return answer_faq(query)

    elif intent == "search":
        return answer_search(query)

    elif intent == "outfit":
        filters = extract_filters(query)

        outfit_products = retrieve_outfit_products(
            occasion=filters["occasion"],
            style=filters["style"],
            max_price=filters["max_price"]
    )

        if outfit_products.empty:
            return "I couldn't find enough products for this outfit."

    # Save the outfit for future follow-up questions
        last_outfit_products = outfit_products

        context = build_outfit_context(outfit_products)

        prompt = build_outfit_prompt(
            query,
            context
    )

        return generate_answer(prompt)

    else:
        return answer_product(query)
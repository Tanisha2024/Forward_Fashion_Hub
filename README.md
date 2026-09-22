# 👗 Fashion Forward Hub — AI-Powered Fashion RAG Chatbot

Fashion Forward Hub is an **AI-powered fashion shopping assistant** built using **Retrieval-Augmented Generation (RAG)**.

The application helps users find fashion products, answer store-related questions, and provide context-aware responses by combining **semantic search, metadata filtering, and an LLM**.

Instead of allowing the language model to generate answers from its own knowledge, the system first retrieves relevant information from the available fashion data and then provides that information to the LLM as context.

---

## 🚀 Features

### 🔎 1. FAQ Retrieval

The chatbot can answer frequently asked questions related to:

* Shipping
* Returns
* Exchanges
* Delivery
* Payments
* Store policies
* Other fashion-store FAQs

The system searches the FAQ dataset using **semantic similarity** and retrieves the most relevant information.

---

### 👕 2. Product Retrieval

Users can search for fashion products using natural language.

For example:

> "Show me black casual t-shirts"

The system retrieves products that are semantically similar to the user's query.

Product information includes:

* Product ID
* Product name
* Price
* Color
* Available sizes
* Material
* Category
* Style
* Description

---

### 🎯 3. Metadata Filtering

The system can filter products based on structured attributes such as:

* Color
* Size
* Category
* Material
* Style
* Price

For example:

> "Show me black T-shirts in size M"

The system can first apply metadata filters and then perform semantic retrieval on the filtered products.

---

### 🧠 4. Filtered Semantic Retrieval

The project combines:

**Metadata Filtering + Semantic Similarity**

This makes product retrieval more accurate than using only keyword or semantic search.

Example:

```text
User Query
    ↓
Extract / Apply Filters
    ↓
Filter Product Dataset
    ↓
Semantic Similarity Search
    ↓
Retrieve Relevant Products
    ↓
Send Context to LLM
```

---

### 🤖 5. Retrieval-Augmented Generation

The project follows a RAG architecture.

Instead of directly asking the LLM to answer a question:

```text
User → LLM → Answer
```

the system follows:

```text
User
  ↓
Query
  ↓
Retriever
  ↓
Relevant Context
  ↓
LLM
  ↓
Grounded Answer
```

This helps reduce hallucinations and keeps responses grounded in the available fashion-store information.

---

### 🔐 6. Grounded Responses

The chatbot is instructed to answer only using the retrieved context.

If the required information is not available, the chatbot responds:

> "I don't have enough information to answer that."

This prevents the model from inventing product or store information.

---

## 🏗️ Project Architecture

```text
                    ┌──────────────────┐
                    │      User        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   User Query     │
                    └────────┬─────────┘
                             │
                             ▼
              ┌────────────────────────────┐
              │ Query Understanding        │
              │ & Metadata Filtering       │
              └─────────────┬──────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
        ┌───────────────┐       ┌────────────────┐
        │ FAQ Retrieval │       │ Product Search │
        └───────┬───────┘       └───────┬────────┘
                │                       │
                ▼                       ▼
        ┌───────────────┐       ┌────────────────┐
        │ Similarity    │       │ Metadata +     │
        │ Search        │       │ Semantic Search│
        └───────┬───────┘       └───────┬────────┘
                │                       │
                └───────────┬───────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Retrieved       │
                   │ Context         │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Groq LLM        │
                   │ GPT-OSS-20B     │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Grounded Answer │
                   └─────────────────┘
```

---

## 🧰 Tech Stack

| Technology             | Purpose                         |
| ---------------------- | ------------------------------- |
| Python                 | Core programming language       |
| Pandas                 | Dataset processing              |
| NumPy                  | Numerical operations            |
| Scikit-learn           | Similarity calculation          |
| TF-IDF / Vectorization | Text representation             |
| Cosine Similarity      | Semantic similarity retrieval   |
| Groq API               | LLM inference                   |
| GPT-OSS-20B            | Generative AI model             |
| python-dotenv          | Environment variable management |
| Git                    | Version control                 |
| GitHub                 | Project hosting                 |

---

## 📂 Project Structure

```text
Fashion-Forward-Hub/
│
├── data/
│   ├── faq.csv
│   └── products.csv
│
├── rag.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> `.env` should never be uploaded to GitHub because it contains the API key.

---

# 📊 Dataset

The project uses fashion-related structured data containing two major information sources.

## FAQ Dataset

The FAQ dataset contains questions and answers related to store policies.

Example:

```text
Question:
How long does shipping take?

Answer:
Orders are usually delivered within the specified delivery period.
```

The user's query is compared against FAQ questions to retrieve the most relevant answer.

---

## Product Dataset

The product dataset contains information about available fashion products.

Example:

```text
Product ID: P006
Product: Black Slim Fit T-Shirt
Price: ₹799
Color: Black
Sizes: S, M, L, XL
Material: Cotton
Category: Casual
Style: College Minimal
```

---

# 🔍 How Retrieval Works

## Step 1 — User Query

The user enters a natural-language query.

Example:

```text
I want a black casual t-shirt in size M
```

---

## Step 2 — Metadata Filtering

The system identifies structured requirements such as:

```text
Color = Black
Size = M
Category = Casual
```

The product dataset is filtered according to these attributes.

---

## Step 3 — Semantic Similarity

The remaining products are compared with the user's query.

The system calculates similarity using **cosine similarity**.

Conceptually:

```text
Similarity(Query, Product)
        ↓
Cosine Similarity
        ↓
Similarity Score
```

The products with the highest similarity scores are selected.

---

## Step 4 — Context Creation

The retrieved products or FAQs are converted into context for the language model.

Example:

```text
Product:
Black Slim Fit T-Shirt

Price:
₹799

Color:
Black

Sizes:
S, M, L, XL

Material:
Cotton
```

---

## Step 5 — LLM Generation

The retrieved context is passed to the Groq-hosted LLM.

The model generates a natural-language response using the supplied information.

---

## Step 6 — Grounded Answer

The chatbot returns an answer based on the retrieved information.

Example:

```text
The Black Slim Fit T-Shirt is available for ₹799
and comes in sizes S, M, L, and XL.
It is made from cotton and is suitable for casual wear.
```

---

# 🧠 RAG Pipeline

The complete RAG pipeline can be represented as:

```text
                 USER QUERY
                     │
                     ▼
              Query Processing
                     │
                     ▼
          ┌─────────────────────┐
          │ Determine Query Type│
          └──────────┬──────────┘
                     │
             ┌───────┴───────┐
             │               │
             ▼               ▼
          FAQ Query      Product Query
             │               │
             ▼               ▼
       FAQ Retrieval    Metadata Filter
                             │
                             ▼
                    Semantic Retrieval
                             │
             ┌───────────────┘
             ▼
       Retrieved Context
             │
             ▼
          Groq LLM
             │
             ▼
      Grounded Response
```

---

# 📐 Similarity Search

The project uses cosine similarity to determine how closely a query matches available information.

The cosine similarity formula is:

```text
              A · B
Similarity = ─────────
             ||A|| ||B||
```

Where:

* `A` = query vector
* `B` = document/product vector

A higher score indicates greater similarity between the query and the retrieved information.

Example:

```text
Query:
black casual t-shirt

Product:
Black Slim Fit T-Shirt

Similarity:
0.79
```

---

# 🤖 LLM

The project uses the **Groq API** for fast LLM inference.

The model used in the project is:

```text
openai/gpt-oss-20b
```

The LLM is responsible for:

* Understanding retrieved context
* Generating natural-language responses
* Following grounding instructions
* Combining retrieved information into a useful answer

The LLM is **not responsible for searching the product database**.

Retrieval is handled separately before generation.

---

# 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit this file to GitHub.

Add it to `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
.venv/
venv/
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/yourusername/Fashion-Forward-Hub.git
```

Move into the project directory:

```bash
cd Fashion-Forward-Hub
```

---

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure API Key

Create:

```text
.env
```

Add:

```env
GROQ_API_KEY=your_api_key
```

---

## 5. Run the project

```bash
python rag.py
```

---

# 📦 Requirements

Example `requirements.txt`:

```text
pandas
numpy
scikit-learn
python-dotenv
groq
```

---

# 💡 Example Queries

### FAQ Queries

```text
How long does shipping take?
```

```text
What is the exchange policy?
```

```text
Can I return my order?
```

---

### Product Queries

```text
Show me black t-shirts
```

```text
I need a casual cotton t-shirt
```

```text
Find a black t-shirt in size M
```

```text
Show me college-style clothing
```

---

# 🧪 Example Retrieval

For a query such as:

```text
I want a black casual t-shirt
```

The system may retrieve:

```text
Product ID: P006
Product: Black Slim Fit T-Shirt
Price: ₹799
Color: Black
Sizes: S, M, L, XL
Material: Cotton
Category: Casual
Style: College Minimal

Similarity Score: 0.79
```

The retrieved product is then passed to the LLM as context.

---

# 🛡️ Hallucination Control

One of the important goals of this project is reducing unsupported LLM responses.

The system uses a grounding instruction such as:

```text
Answer only using the provided context.

If the information is not available in the context,
say: "I don't have enough information to answer that."
```

This creates a simple but important RAG guardrail.

---

# 📈 Key Concepts Demonstrated

This project demonstrates practical understanding of:

* Retrieval-Augmented Generation
* Information retrieval
* Semantic search
* Vector representations
* Cosine similarity
* Metadata filtering
* Hybrid retrieval
* Query processing
* Context construction
* Prompt engineering
* LLM inference
* Hallucination control
* Environment variable management
* Git/GitHub
* Python data processing

---

# 🎯 Why This Project Matters

Traditional chatbots generally depend on predefined responses.

A pure LLM chatbot can generate fluent responses but may provide information that does not exist in the application's database.

Fashion Forward Hub combines the two approaches:

```text
Structured Data
      +
Information Retrieval
      +
LLM
      =
Grounded AI Assistant
```

This makes the project a practical example of how **RAG systems can connect LLMs with domain-specific data**.

---

# 🔮 Future Improvements

The current project provides a foundation for a more advanced production-grade RAG system.

Possible improvements include:

### 1. Vector Database

Replace basic similarity search with a vector database such as:

* FAISS
* Chroma
* Qdrant
* Pinecone

---

### 2. Better Embedding Models

Use dedicated embedding models instead of basic TF-IDF representations.

Examples include:

* Sentence Transformers
* BGE embeddings
* E5 embeddings

---

### 3. Advanced Chunking

For larger product descriptions and policy documents, implement:

* Fixed-size chunking
* Recursive chunking
* Semantic chunking
* Overlapping chunks

---

### 4. RAG Evaluation

Add evaluation metrics such as:

* Retrieval Precision
* Retrieval Recall
* Context Relevance
* Faithfulness
* Answer Relevance

---

### 5. Reranking

Add a reranker after initial retrieval:

```text
Query
  ↓
Retriever
  ↓
Top-K Documents
  ↓
Reranker
  ↓
Best Documents
  ↓
LLM
```

---

### 6. Conversation Memory

Allow the assistant to understand previous user messages.

Example:

```text
User:
Show me black t-shirts.

Assistant:
...

User:
Show me one under ₹1000.

Assistant:
...
```

The second query can use context from the first interaction.

---

### 7. Streamlit Interface

A complete Streamlit interface could provide:

* Chat interface
* Product cards
* Filters
* Product recommendations
* FAQ assistant
* Conversation history

---

### 8. Production Deployment

The application could eventually be deployed using:

* Streamlit Cloud
* Docker
* FastAPI
* Cloud platforms

---

# 🧑‍💻 Skills Demonstrated

This project demonstrates practical skills in:

```text
Python
   ↓
Data Processing
   ↓
Information Retrieval
   ↓
Semantic Search
   ↓
RAG
   ↓
LLM Integration
   ↓
Prompt Engineering
   ↓
AI Application Development
```

---

# 📌 Project Highlights

* Built an AI-powered fashion shopping assistant
* Implemented FAQ retrieval
* Implemented product retrieval
* Added metadata-based filtering
* Combined filtering with semantic similarity
* Integrated Groq LLM inference
* Implemented grounded generation
* Added hallucination-control instructions
* Worked with structured fashion-product data
* Built the project using Python

---

# 👩‍💻 Author

**Tanisha**

B.Tech Computer Science Engineering

### Interests

* Artificial Intelligence
* Machine Learning
* Generative AI
* RAG Systems
* Agentic AI
* AI Engineering

---

# ⭐ Future Vision

Fashion Forward Hub can evolve from a basic RAG chatbot into a complete **AI shopping assistant** capable of:

```text
Product Search
      ↓
Personalized Recommendations
      ↓
Conversational Shopping
      ↓
Order Assistance
      ↓
Customer Support
      ↓
Agentic Shopping Workflows
```

The long-term goal is to demonstrate how **Generative AI + Retrieval + Structured Data + Agents** can be combined to build practical AI applications.

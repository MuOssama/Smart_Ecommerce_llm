# app.py
from flask import Flask, render_template, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize LangChain with Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=os.getenv('GOOGLE_API_KEY'),
    temperature=0.7
)

# Initialize conversation chain with memory
conversation = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory()
)

def init_db():
    """Initialize the SQLite database and create products table if it doesn't exist"""
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         price REAL NOT NULL,
         description TEXT)
    ''')
    conn.commit()
    conn.close()

def get_products():
    """Retrieve all products from the database"""
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    products = c.fetchall()
    conn.close()
    return products

@app.route('/')
def home():
    """Render the home page with all products"""
    products = get_products()
    return render_template('index.html', products=products)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat interactions with the LLM"""
    user_input = request.json.get('message', '')

    # Get product context from database
    products = get_products()
    product_context = "Available products:\n"
    for product in products:
        product_context += f"- {product[1]}: ${product[2]} - {product[3]}\n"

    # Combine user input with product context
    full_prompt = f"Context: {product_context}\nUser question: {user_input}\nPlease help with product recommendations or questions."

    # Get response from LangChain conversation
    response = conversation.predict(input=full_prompt)

    return jsonify({'response': response})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
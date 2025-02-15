
## Overview
This is repo introduces Ecommerce website that make chats with users and handle their requests by llm (large language model) to process complex quires.
This is a Flask-based e-commerce website that uses Google's Gemini 1.5 Pro LLM through LangChain to provide intelligent product recommendations and answer customer questions. The application features a product catalog stored in SQLite and a chat interface for customer interactions.

## Project Structure
```
llm-ecommerce/
├── app.py
├── templates/
│   └── index.html
├── ecommerce.db
├── init_db.py
├── requirements.txt
└── .env
```

## Local Setup

### Prerequisites
- Python 3.8 or higher
- Google Cloud API key with Gemini API access

### Installation Steps
1. Clone the repository
```bash
git clone <repository-url>
cd llm-ecommerce
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

5. Create the project structure:
```bash
mkdir templates
```

6. Place the HTML file:
- Create `templates` folder in your project root if it doesn't exist
- Save the `index.html` file inside the `templates` folder
- Flask will look for templates in this folder by default

7. Initialize the database by creating a file named `init_db.py`:
```python
# init_db.py
import sqlite3

def init_database():
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()

    # Create products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         price REAL NOT NULL,
         description TEXT)
    ''')

    # Add sample products
    sample_products = [
        ('Laptop', 999.99, 'High-performance laptop with 16GB RAM'),
        ('Smartphone', 699.99, 'Latest model with 5G capability'),
        ('Headphones', 199.99, 'Noise-cancelling wireless headphones')
    ]

    # Check if products already exist
    c.execute('SELECT COUNT(*) FROM products')
    count = c.fetchone()[0]

    # Only insert sample products if table is empty
    if count == 0:
        c.executemany('INSERT INTO products (name, price, description) VALUES (?, ?, ?)', 
                      sample_products)
        print("Sample products added successfully!")
    else:
        print("Products already exist in the database.")

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully!")
```

8. Initialize the database by running:
```bash
python init_db.py
```

9. Run the application:
```bash
python app.py
```

10. Visit `http://localhost:5000` in your web browser

## Adding New Products
You can add new products using Python or SQLite command line:

### Using Python
```python
import sqlite3

def add_product(name, price, description):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('INSERT INTO products (name, price, description) VALUES (?, ?, ?)',
              (name, price, description))
    conn.commit()
    conn.close()

# Example usage:
add_product('Tablet', 499.99, 'Large screen tablet with stylus support')
```

### Using SQLite Command Line
```bash
sqlite3 ecommerce.db
```
Then in SQLite prompt:
```sql
INSERT INTO products (name, price, description) VALUES ('Tablet', 499.99, 'Large screen tablet with stylus support');
```

## Replit Deployment

1. Create a new Replit project
2. Create the following folder structure in Replit:
```
.
├── app.py
├── init_db.py
├── templates/
│   └── index.html
└── requirements.txt
```

3. In the Replit sidebar, create a new secret named `GOOGLE_API_KEY` with your API key
4. Create a `.replit` file with the following content:
```
language = "python3"
run = "python init_db.py && python app.py"
```

5. Install packages:
   - Click on "Shell"
   - Run: `pip install -r requirements.txt`

6. Click "Run" to start the application


### Important Notes for Replit
- The SQLite database will be created in the project directory
- The application will be accessible via the URL provided by Replit
- Make sure to keep your API key secret by using Replit's Secrets management

## Usage Guide

### Adding Products
To add new products to the database, you can use the SQLite command line or create a management script:

```python
import sqlite3

def add_product(name, price, description):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('INSERT INTO products (name, price, description) VALUES (?, ?, ?)',
              (name, price, description))
    conn.commit()
    conn.close()
```

### Using the Chat Interface
1. Browse the available products displayed on the main page
2. Use the chat interface to:
   - Ask about specific products
   - Get product recommendations
   - Inquire about prices and features
   - Ask for comparisons between products

### Example Chat Interactions
- "What's your best laptop under $1000?"
- "Can you compare the features of your smartphones?"
- "I need noise-cancelling headphones for travel, what do you recommend?"

## Troubleshooting

### Common Issues
1. Database Connection Error
   - Ensure the database file has proper permissions
   - Check if SQLite is installed properly

2. API Key Issues
   - Verify the API key is correctly set in the `.env` file
   - Check if the API key has proper permissions for Gemini

3. Chat Not Responding
   - Check the browser console for JavaScript errors
   - Verify the Flask server is running
   - Ensure the API key is valid and has sufficient quota

## Maintenance

### Database Backup
Regularly backup your SQLite database:
```bash
sqlite3 ecommerce.db .dump > backup.sql
```

### Updating Dependencies
Periodically update the dependencies:
```bash
pip install --upgrade -r requirements.txt
```

## Security Considerations
- Keep your `.env` file secure and never commit it to version control
- Regularly update dependencies for security patches
- Implement rate limiting for the chat endpoint in production
- Sanitize user input before processing

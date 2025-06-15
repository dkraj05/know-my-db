# 🗃️ Database Chat Assistant

An AI-powered chatbot that helps you query and understand your PostgreSQL database using natural language. Built with Streamlit, OpenAI Assistants API, and PostgreSQL.

## ✨ Features

- **Natural Language Queries**: Ask questions about your database in plain English
- **OpenAI Assistants API**: Uses GPT-4o with function calling (MCP) for intelligent database interactions
- **Secure Query Execution**: Only SELECT queries allowed, results limited to 5 rows
- **Real-time Database Connection**: Live connection to PostgreSQL with sample data
- **Interactive UI**: Clean Streamlit interface with conversation history
- **Docker Support**: Fully containerized with docker-compose

## 🚀 Quick Start

### Option 1: Run with Docker (Recommended)

1. **Clone and setup**:
   ```bash
   git clone <your-repo>
   cd know-my-db
   ```

2. **Create environment file**:
   ```bash
   # Create .env file with your configuration
   cat > .env << EOF
   OPENAI_API_KEY=your_openai_api_key_here
   PG_HOST=postgres
   PG_PORT=5432
   PG_USER=postgres
   PG_PASS=password
   PG_DB=knowmydb
   EOF
   ```

3. **Start the application**:
   ```bash
   docker-compose up --build
   ```

4. **Access the app**: Open http://localhost:8501

### Option 2: Run Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup PostgreSQL** (if not using Docker):
   - Install PostgreSQL locally
   - Create database and run `db/init.sql`

3. **Configure environment**:
   ```bash
   # Create .env file
   OPENAI_API_KEY=your_openai_api_key_here
   PG_HOST=localhost
   PG_PORT=5432
   PG_USER=postgres
   PG_PASS=your_password
   PG_DB=knowmydb
   ```

4. **Run the app**:
   ```bash
   streamlit run app/main.py
   ```

## 📊 Sample Data

The database includes three tables with sample data:

- **users**: 8 sample users with names, emails, ages, and cities
- **products**: 8 sample products across different categories
- **orders**: 12 sample orders linking users and products

## 💬 Example Questions

Try asking these questions to the assistant:

- "What tables are available in the database?"
- "Show me the structure of the users table"
- "How many users are there?"
- "What are the top 5 most expensive products?"
- "Show me recent orders"
- "Which city has the most users?"
- "What's the total revenue from completed orders?"

## 🛠️ Project Structure

```
project/
├── docker-compose.yml          # Docker services configuration
├── Dockerfile                  # Streamlit app container
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables (create this)
├── db/
│   └── init.sql              # PostgreSQL initialization script
└── app/
    ├── main.py               # Streamlit UI application
    ├── mcp_agent.py          # OpenAI Assistants API integration
    └── tools/
        ├── __init__.py
        ├── db_query.py       # SQL query execution tool
        ├── get_table_names.py # Table listing tool
        └── summarize_table.py # Table schema and sample data tool
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `PG_HOST` | PostgreSQL host | `localhost` |
| `PG_PORT` | PostgreSQL port | `5432` |
| `PG_USER` | PostgreSQL username | `postgres` |
| `PG_PASS` | PostgreSQL password | `password` |
| `PG_DB` | PostgreSQL database name | `knowmydb` |

### OpenAI API Key

Get your API key from [OpenAI Platform](https://platform.openai.com/account/api-keys).

## 🔒 Security Features

- **Query Restriction**: Only SELECT queries are allowed
- **Result Limiting**: Maximum 5 rows returned per query
- **SQL Injection Protection**: Parameterized queries and input validation
- **Environment Variables**: Sensitive data stored in .env file

## 🐳 Docker Services

- **postgres**: PostgreSQL 15 database with sample data
- **streamlit**: Python application with Streamlit UI

## 🛠️ Development

### Adding New Tools

1. Create a new tool function in `app/tools/`
2. Register it in `app/mcp_agent.py`
3. Update the assistant instructions

### Customizing Sample Data

Edit `db/init.sql` to modify the sample tables and data.

## 📝 TODO Tracking

- ✅ Project structure setup
- ✅ PostgreSQL database with sample data
- ✅ OpenAI Assistants API integration with MCP tools
- ✅ Streamlit UI with chat interface
- ✅ Docker containerization
- ✅ Security measures and query restrictions
- ✅ Environment variable configuration
- ✅ Comprehensive documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ using Streamlit, OpenAI Assistants API, and PostgreSQL**

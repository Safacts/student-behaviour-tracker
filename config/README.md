# Configuration

This directory contains configuration files for the application.

## Files

- **.env.example** - Example environment variables template
- **.env.production** - Production environment configuration

## Environment Variables

Copy `.env.example` to `.env` and configure the following variables:

```bash
# API Keys
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# SMTP Configuration (for email sending)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

## Usage

1. Copy the example file:
```bash
cp config/.env.example .env
```

2. Edit `.env` with your actual values

3. The application will automatically load environment variables from `.env` using `python-dotenv`

## Security

- Never commit `.env` files to version control
- Add `.env` to `.gitignore`
- Use different configurations for development and production
- Rotate API keys regularly

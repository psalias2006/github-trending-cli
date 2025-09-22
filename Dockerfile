FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY github_trending/ ./github_trending/
COPY setup.py .
COPY README.md .

# Install the package
RUN pip install -e .

# Run the CLI
ENTRYPOINT ["github-trending"]

FROM python:3.11-slim

# Define the working directory
WORKDIR /app

# Install necessary system dependencies (as you had)
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    gcc \
    python3-dev \
    netcat-openbsd \
    # Add tini to handle signal forwarding and reap zombie processes safely (good practice)
    tini \ 
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Copy the wait script and give execute permissions
# The wait_for_db.sh will now contain the entire start sequence.
COPY wait_for_db.sh /usr/local/bin/wait_for_db.sh
RUN chmod +x /usr/local/bin/wait_for_db.sh

# Expose the listening port
EXPOSE 8000

# Use Tini as the entrypoint for proper signal handling
ENTRYPOINT ["/usr/bin/tini", "--"]

# CMD executes the wait script, which handles the database check and app start
CMD ["wait_for_db.sh"]
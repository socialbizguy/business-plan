FROM python:3.9-slim

WORKDIR /app

# Add src to Python path
ENV PYTHONPATH=/app/src

# Install bash for better shell support
RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

# Set bash as the default shell
SHELL ["/bin/bash", "-c"]

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Handle environment variables using bash
RUN if [ -f .env ]; then \
    mkdir -p /etc/profile.d && \
    touch /etc/profile.d/app_env.sh && \
    while IFS= read -r line; do \
        if [[ -n "$line" && ! "$line" =~ ^# ]]; then \
            echo "export $line" >> /etc/profile.d/app_env.sh; \
        fi; \
    done < .env; \
    fi

# Make the environment variables available to all shells
RUN chmod +x /etc/profile.d/app_env.sh

ENTRYPOINT ["/bin/bash", "-c", "source /etc/profile.d/app_env.sh && python src/slt_planning.py"] 
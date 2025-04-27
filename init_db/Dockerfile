# Use the official PostgreSQL image as the base
FROM postgres:latest@sha256:fe3f571d128e8efadcd8b2fde0e2b73ebab6dbec33f6bfe69d98c682c7d8f7bd

# Copy the init.sql script to the container's entrypoint directory
COPY ./init.sql /docker-entrypoint-initdb.d/init.sql

# Ensure the script is executable (optional, just to be sure)
RUN chmod +x /docker-entrypoint-initdb.d/init.sql
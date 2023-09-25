# first stage
FROM python:3.10 AS builder
COPY ./requirements.txt .

RUN pip install --upgrade pip

# install dependances
RUN pip install --user -r requirements.txt

# second stage
FROM python:3.10-slim

RUN pip install fastapi uvicorn

# copy only needed dependances
COPY --from=builder /root/.local /root/.local
COPY ./api_file.py .
COPY ./.env .
COPY ./orm_file.py .
COPY ./crypto_engine.py .
COPY ./main.py .
COPY ./BC_engine.py .
COPY ./table.py .


# update PATH
ENV PATH=/root/.local:$PATH
ENV PATH=/root/.local/bin:$PATH

# Expose the required port (default is 8000 for FastAPI)
EXPOSE 8000

# Run the FastAPI application with Uvicorn when the container starts
CMD ["uvicorn", "api_file:api", "--host", "0.0.0.0", "--port", "8000"]
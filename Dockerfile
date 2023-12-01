FROM mcr.microsoft.com/playwright/python:v1.39.0-jammy

WORKDIR /app

ARG HTTP_PROXY

COPY requirements.txt /app/
RUN if [ -n "${HTTP_PROXY}" ]; then \
      pip3 install --proxy "${HTTP_PROXY}" -r requirements.txt; \
    else \
      pip3 install -r requirements.txt; \
    fi
COPY . /app/

ENV PYTHONUNBUFFERED 1

RUN chmod +x entrypoint.sh
CMD [ "./entrypoint.sh" ]
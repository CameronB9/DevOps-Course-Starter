FROM python:3.12.0-bookworm as base
    WORKDIR /app/todo-app/
    RUN curl -sSL https://install.python-poetry.org | python3 -
    ENV PATH="/root/.local/bin/:/app/todo-app/.venv/bin:${PATH}"


FROM base as development
    COPY poetry* /app/todo-app/
    COPY pyproject.toml /app/todo-app/
    RUN poetry install
    ENTRYPOINT ["poetry", "run", "flask", "run"]

FROM development as debug
    ENTRYPOINT [ "tail", "-f", "/dev/null" ]

FROM development as test
    RUN apt update -qqy && apt install -qqy wget gnupg unzip
    RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \  
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \  
    && apt update -qqy \  
    && apt -qqy install google-chrome-stable \  
    && rm /etc/apt/sources.list.d/google-chrome.list \  
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
    ENTRYPOINT ["poetry", "run", "pytest-watch", "--poll"]

FROM base as production
    COPY / /app/todo-app/
    RUN poetry install
    ENTRYPOINT ["poetry", "run", "gunicorn", "--bind", "0.0.0.0", "todo_app.app:create_app()"]
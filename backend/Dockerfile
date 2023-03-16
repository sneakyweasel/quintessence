FROM python:3.8

RUN pip install pipenv

ENV PROJECT_DIR /backend

ENV OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ENV IONQ_API_KEY = 1234657890

COPY . /${PROJECT_DIR}
WORKDIR ${PROJECT_DIR}

RUN pipenv install --system --deploy

CMD ["gunicorn", "--graceful-timeout", "5", "--chdir", ".", "main:app",  "-w", "4", "-b", "0.0.0.0:8080"]

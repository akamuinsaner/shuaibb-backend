FROM python:3.10-alpine

ARG PORT=${PORT}
ARG ENV=${ENV}
ARG WORKDIR="/web"
ARG MANAGEFILE="${WORKDIR}/shuaibb/manage.py"

COPY . ${WORKDIR}
ADD /home/lighthouse/secret/.env.txcloud ${WORKDIR}

WORKDIR ${WORKDIR}

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && python ${MANAGEFILE} makemigrations \
    && python ${MANAGEFILE} migrate

ENV ENV=${ENV}
ENV PYTHONUNBUFFERED=1


EXPOSE ${PORT}



ENTRYPOINT ["python", "/web/shuaibb/manage.py", "runserver", "0.0.0.0:8000"]


FROM python:3.10-alpine

ARG PORT
ARG ENV
ARG DB_PWD
ARG DB_HOST
ARG WORKDIR="/web"
ARG MANAGEFILE="${WORKDIR}/shuaibb/manage.py"

ENV DB_HOST=${DB_HOST}

COPY . ${WORKDIR}

WORKDIR ${WORKDIR}

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN export ENV=${ENV}
RUN python ${MANAGEFILE} makemigrations
RUN python ${MANAGEFILE} migrate

EXPOSE ${PORT}


CMD ["python", ${MANAGEFILE}, "runserver", ${PORT}]


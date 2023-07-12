FROM python:3.10
RUN mkdir /it_school
WORKDIR /it_school
COPY requirements.txt /it_school/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /it_school/
CMD ["uvicorn", "--host", "0.0.0.0", "it_school:app"]
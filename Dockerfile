FROM python:3.9

WORKDIR /usr/src/app

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

COPY . .

# For debugging purposes and control group
RUN ls -la && find .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8050

CMD ["python", "./Dashboard/app/main/app.py"]

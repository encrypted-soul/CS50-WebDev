import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for id, title, author, year in reader:
        db.execute("INSERT INTO books (id, title, author, year) VALUES (:id, :title, :author, :year)",
                   {"id": id, "title": title, "author": author, "year": year})
        print(f"Added the book {title} from {author}")
    db.commit()

if __name__ == "__main__":
    main()
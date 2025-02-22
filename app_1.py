from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# ✅ Use relative paths for portability
BASE_DIR = r"C:\Users\neoli\OneDrive\Desktop\Recommender_System"

# ✅ Load the models
with open(os.path.join(BASE_DIR, "pt.pkl"), "rb") as f:
    pt = pickle.load(f)

with open(os.path.join(BASE_DIR, "similarity.pkl"), "rb") as f:
    cosine_sim = pickle.load(f)

with open(os.path.join(BASE_DIR, "books.pkl"), "rb") as f:
    books = pickle.load(f)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def recommend():
    book_name = request.form.get("book_name").strip()
    print(f"🔍 User entered book name: {book_name}")  # Debug print

    # ✅ Find the exact book title in the dataset
    book_info = books[books['Book-Title'].str.lower() == book_name.lower()]

    if book_info.empty:
        print("❌ Book not found in dataset!")
        return render_template("recommendation.html", books=[], error="Book not found in database.")

    # ✅ Get book details
    book_title = book_info.iloc[0]['Book-Title']
    book_author = book_info.iloc[0]['Book-Author']
    book_year = book_info.iloc[0]['Year-Of-Publication']
    book_image = book_info.iloc[0]['Image-URL-L'] if 'Image-URL-L' in book_info else "static/no_image.png"

    print(f"✅ Found Book: {book_title}, Author: {book_author}, Year: {book_year}")

    # ✅ Check if the book exists in pivot table `pt`
    if book_title not in pt.index:
        print("❌ Book title not found in pivot table!")
        return render_template("recommendation.html", books=[], error="No recommendations found for this book.")

    # ✅ Get similarity scores
    idx = pt.index.get_loc(book_title)
    scores = list(enumerate(cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]  # Top 5 recommendations

    # ✅ Prepare recommended books list
    recommended_books = []
    for i, s in scores:
        book_details = books[books["Book-Title"] == pt.index[i]]
        if not book_details.empty:
            recommended_books.append({
                "Title": pt.index[i],
                "Author": book_details.iloc[0]['Book-Author'],
                "Year": book_details.iloc[0]['Year-Of-Publication'],
                "Image": book_details.iloc[0]['Image-URL-L'] if 'Image-URL-L' in book_details else "static/no_image.png",
                "score": round(float(s), 4)
            })

    print(f"📚 Recommended Books: {recommended_books}")  # Debug print

    return render_template("recommendation.html", books=recommended_books, error=None)

if __name__ == "__main__":
    app.run(debug=True)

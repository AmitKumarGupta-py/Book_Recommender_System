from flask import Flask, render_template
import pickle

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
cosine_sim = pickle.load(open('similarity.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_rating'].values),
                           rating = list(popular_df['average_rating'].values)
                           )

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')


@app.route('/recommendation_books', methods=['POST'])
def recommendation_books():
    book_name = request.form.get('book_name')
    book_name = book_name.lower()
    book_name = book_name.title()
    if book_name not in books:
        return render_template('recommend.html', error = 'Book not found in the database')
    else:
        recommended_books = pt[book_name].sort_values(ascending=False)[1:6]
        recommended_books = recommended_books.index
        recommended_books = [books[i] for i in recommended_books]
        return render_template('recommend.html', book_name = book_name, recommended_books = recommended_books)

if __name__ == '__main__':
    app.run(debug=True)
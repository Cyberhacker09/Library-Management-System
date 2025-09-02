// Start with empty array
let booksData = [];

// Function to display books
function displayBooks(books) {
    const bookList = document.getElementById('bookList');
    bookList.innerHTML = ""; // Clear existing books

    if (books.length === 0) {
        bookList.innerHTML = "<p style='color: #666;'>No books available yet.</p>";
        return;
    }

    books.forEach(book => {
        const bookDiv = document.createElement('div');
        bookDiv.classList.add('book');

        bookDiv.innerHTML = `
            <img src="${book.img}" alt="${book.title}">
            <h4>${book.title}</h4>
            <p>Author: ${book.author}</p>
        `;

        bookList.appendChild(bookDiv);
    });
}

// Initial display (empty)
displayBooks(booksData);

// Search function
function searchBooks() {
    const input = document.getElementById('searchInput').value.toLowerCase();
    const filteredBooks = booksData.filter(book =>
        book.title.toLowerCase().includes(input) ||
        book.author.toLowerCase().includes(input)
    );

    displayBooks(filteredBooks);
}

// Example function to add a new book dynamically
function addBook(title, author, img) {
    booksData.push({ title, author, img });
    displayBooks(booksData);
}

// Example: later you can call addBook like this:
// addBook("New Book Title", "Author Name", "https://via.placeholder.com/200x250");

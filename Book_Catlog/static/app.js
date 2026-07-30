const apiBase = '/books';
const form = document.getElementById('book-form');
const titleInput = document.getElementById('title');
const authorInput = document.getElementById('author');
const genreInput = document.getElementById('genre');
const statusInput = document.getElementById('status');
const idInput = document.getElementById('book-id');
const booksBody = document.getElementById('books-body');
const submitButton = form.querySelector('button');

function resetForm() {
  form.reset();
  idInput.value = '';
  submitButton.textContent = 'Add Book';
}

async function loadBooks() {
  const response = await fetch(apiBase);
  const books = await response.json();
  booksBody.innerHTML = '';

  books.forEach((book) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${book.id}</td>
      <td>${book.title}</td>
      <td>${book.author}</td>
      <td>${book.genre || ''}</td>
      <td>${book.status}</td>
      <td class="actions">
        <button data-action="edit" data-id="${book.id}">Edit</button>
        <button data-action="toggle" data-id="${book.id}">Toggle Status</button>
        <button data-action="delete" data-id="${book.id}">Delete</button>
      </td>
    `;
    booksBody.appendChild(row);
  });
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const payload = {
    title: titleInput.value,
    author: authorInput.value,
    genre: genreInput.value || null,
    status: statusInput.value,
  };

  const method = idInput.value ? 'PUT' : 'POST';
  const url = idInput.value ? `${apiBase}/${idInput.value}` : apiBase;

  await fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  resetForm();
  loadBooks();
});

booksBody.addEventListener('click', async (event) => {
  const button = event.target.closest('button');
  if (!button) return;

  const { action, id } = button.dataset;
  if (action === 'delete') {
    await fetch(`${apiBase}/${id}`, { method: 'DELETE' });
    loadBooks();
    return;
  }

  if (action === 'edit') {
    const response = await fetch(`${apiBase}/${id}`);
    const book = await response.json();
    idInput.value = book.id;
    titleInput.value = book.title;
    authorInput.value = book.author;
    genreInput.value = book.genre || '';
    statusInput.value = book.status;
    submitButton.textContent = 'Update Book';
    return;
  }

  if (action === 'toggle') {
    const response = await fetch(`${apiBase}/${id}`);
    const book = await response.json();
    const nextStatus = book.status === 'available' ? 'borrowed' : 'available';
    await fetch(`${apiBase}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: nextStatus }),
    });
    loadBooks();
  }
});

loadBooks();

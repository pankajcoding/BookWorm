const endpoint = '/getbooks';
const books = [];
fetch(endpoint)
  .then(blob => blob.json())
  .then(data => books.push(...data));
function findMatches(wordToMatch, books) {
  return books.filter(book => {
    // here we need to figure out if the city or state matches what was searched
    const regex = new RegExp(wordToMatch, 'gi');
    return book.title.match(regex) || book.author.match(regex)
  });
}
function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}
function displayMatches() {
  if (this.value==""){
    suggestions.innerHTML = '';
    return;
  }
  const matchArray = findMatches(this.value, books);
  const html = matchArray.map(book => {
    const regex = new RegExp(this.value, 'gi');
    const cityName = book.title.replace(regex, `<span class="hl">${this.value}</span>`);
    const stateName = book.author.replace(regex, `<span class="hl">${this.value}</span>`);
    return `
      
    <a href="book/${book.id}"/><li style="display:flex;">

        <span class="name">${cityName}</span>
        <span class="author"> ${stateName}</span>
        
      </li>
      </a>
    `;
  }).join('');
  suggestions.innerHTML = html;
}
const searchInput = document.querySelector('.search');
const suggestions = document.querySelector('.suggestions');
searchInput.addEventListener('change', displayMatches);
searchInput.addEventListener('keyup', displayMatches);
(function () {
  const listRoot = document.getElementById('blog-list-root');
  const filterRoot = document.getElementById('blog-category-filters');
  const searchInput = document.getElementById('blog-search');
  const tagRoot = document.getElementById('blog-tags-root');

  const state = { category: 'All', query: '', tag: 'All' };
  const posts = [...window.BLOG_POSTS].sort((a, b) => new Date(b.date) - new Date(a.date));
  const categories = ['All', ...new Set(posts.map(p => p.category))];
  const tags = ['All', ...new Set(posts.flatMap(p => p.tags))];

  const readingTime = post => Math.max(1, Math.ceil(post.content.join(' ').split(/\s+/).length / 180));

  function render() {
    const q = state.query.trim().toLowerCase();
    const filtered = posts.filter(post => {
      const inCategory = state.category === 'All' || post.category === state.category;
      const inTag = state.tag === 'All' || post.tags.includes(state.tag);
      const inQuery = !q || [post.title, post.summary, post.tags.join(' ')].join(' ').toLowerCase().includes(q);
      return inCategory && inTag && inQuery;
    });

    listRoot.innerHTML = filtered.length ? '' : '<p class="meta">No posts found. Update filters or add new posts in <code>data/site-data.js</code>.</p>';
    filtered.forEach(post => {
      const article = document.createElement('article');
      article.className = 'blog-card page-enter';
      article.innerHTML = `
        <img src="${post.coverImage}" alt="${post.title}" loading="lazy"/>
        <div class="card-body">
          <div class="meta">${post.category} · ${new Date(post.date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })} · ${readingTime(post)} min read</div>
          <h3>${post.title}</h3>
          <p>${post.summary}</p>
          <div class="tags">${post.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
          <div class="links-row"><a class="btn btn-primary" href="post.html?slug=${post.slug}">Read Article</a></div>
        </div>`;
      listRoot.appendChild(article);
    });
  }

  categories.forEach(category => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = `filter-btn${category === 'All' ? ' active' : ''}`;
    btn.textContent = category;
    btn.addEventListener('click', () => {
      filterRoot.querySelectorAll('button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.category = category;
      render();
    });
    filterRoot.appendChild(btn);
  });

  tags.forEach(tag => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = `filter-btn${tag === 'All' ? ' active' : ''}`;
    btn.textContent = tag;
    btn.addEventListener('click', () => {
      tagRoot.querySelectorAll('button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.tag = tag;
      render();
    });
    tagRoot.appendChild(btn);
  });

  searchInput.addEventListener('input', (event) => {
    state.query = event.target.value;
    render();
  });

  render();
})();

(function () {
  const params = new URLSearchParams(window.location.search);
  const slug = params.get('slug');
  const post = window.BLOG_POSTS.find(item => item.slug === slug);

  const progressBar = document.getElementById('reading-progress');
  const articleRoot = document.getElementById('post-root');
  const relatedRoot = document.getElementById('related-posts');

  if (!post) {
    articleRoot.innerHTML = '<h1>Post not found</h1><p class="meta">Return to <a href="index.html">blog list</a>.</p>';
    return;
  }

  const minutes = Math.max(1, Math.ceil(post.content.join(' ').split(/\s+/).length / 180));
  document.title = `${post.title} | Mehmet Akif ÇAKIR`;
  articleRoot.innerHTML = `
    <img src="${post.coverImage}" alt="${post.title}" loading="lazy"/>
    <h1>${post.title}</h1>
    <p class="meta">${post.category} · ${new Date(post.date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })} · ${minutes} min read${post.placeholder ? ' · Placeholder article' : ''}</p>
    <div class="tags">${post.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}</div>
    ${post.content.map(paragraph => `<p>${paragraph}</p>`).join('')}
  `;

  const related = window.BLOG_POSTS
    .filter(item => item.slug !== post.slug && (item.category === post.category || item.tags.some(tag => post.tags.includes(tag))))
    .slice(0, 3);

  related.forEach(item => {
    const card = document.createElement('article');
    card.className = 'blog-card';
    card.innerHTML = `
      <img src="${item.coverImage}" alt="${item.title}" loading="lazy"/>
      <div class="card-body">
        <div class="meta">${item.category}</div>
        <h3>${item.title}</h3>
        <a class="btn btn-ghost" href="post.html?slug=${item.slug}">Read</a>
      </div>`;
    relatedRoot.appendChild(card);
  });

  const updateProgress = () => {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - window.innerHeight;
    const progress = height > 0 ? Math.min(100, (scrollTop / height) * 100) : 0;
    progressBar.style.width = `${progress}%`;
  };

  updateProgress();
  window.addEventListener('scroll', updateProgress, { passive: true });
})();

(function () {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const root = document.documentElement;
  const themeBtn = document.getElementById('theme-toggle');
  const menuBtn = document.getElementById('menu-toggle');
  const navLinks = document.getElementById('nav-links');

  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    root.dataset.theme = savedTheme;
  } else if (window.matchMedia('(prefers-color-scheme: light)').matches) {
    root.dataset.theme = 'light';
  }
  const updateThemeIcon = () => themeBtn.setAttribute('aria-label', `Switch to ${root.dataset.theme === 'light' ? 'dark' : 'light'} mode`);
  updateThemeIcon();
  themeBtn.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', root.dataset.theme);
    updateThemeIcon();
  });

  menuBtn.addEventListener('click', () => {
    const expanded = menuBtn.getAttribute('aria-expanded') === 'true';
    menuBtn.setAttribute('aria-expanded', String(!expanded));
    navLinks.classList.toggle('open');
  });
  navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    menuBtn.setAttribute('aria-expanded', 'false');
    navLinks.classList.remove('open');
  }));

  const { profile, social, contact, cvPath } = window.SITE_DATA;
  document.getElementById('hero-name').textContent = profile.name;
  document.getElementById('hero-role').textContent = profile.role;
  document.getElementById('hero-tagline').textContent = profile.tagline;
  document.getElementById('hero-status').lastChild.textContent = ` ${profile.status}`;
  document.querySelectorAll('.github-link').forEach(el => el.href = social.github);
  document.querySelectorAll('.linkedin-link').forEach(el => el.href = social.linkedin);
  document.querySelectorAll('.email-link').forEach(el => {
    el.href = `mailto:${contact.email}`;
    el.textContent = contact.email;
  });
  document.querySelectorAll('.cv-link').forEach(el => el.href = cvPath);
  document.getElementById('year').textContent = '2026';

  const skillsRoot = document.getElementById('skills-root');
  window.SKILLS_DATA.forEach(group => {
    const card = document.createElement('article');
    card.className = 'card reveal';
    card.innerHTML = `<h3>${group.category}</h3>${group.items.map(item => `<div class="skill-item"><span>${item.name}</span><span class="level">${item.level}</span></div>`).join('')}`;
    skillsRoot.appendChild(card);
  });

  const projectRoot = document.getElementById('projects-root');
  const projectFilters = document.getElementById('project-filters');
  const categories = ['All', 'Robotics', 'Software', 'Electronics', 'Engineering', 'AI'];

  const renderProjects = (category = 'All') => {
    projectRoot.innerHTML = '';
    window.PROJECTS_DATA
      .filter(p => category === 'All' || p.category === category)
      .forEach(project => {
        const card = document.createElement('article');
        card.className = 'project-card reveal';
        card.innerHTML = `
          <img src="${project.image}" alt="${project.title}" loading="lazy"/>
          <div class="card-body">
            <div class="meta">${project.category}${project.placeholder ? ' · Placeholder' : ''}</div>
            <h3>${project.title}</h3>
            <p>${project.description}</p>
            <div class="tags">${project.technologies.map(t => `<span class="tag">${t}</span>`).join('')}</div>
            <div class="links-row">
              <a class="btn btn-ghost" href="${project.github}" target="_blank" rel="noreferrer">GitHub</a>
              <a class="btn btn-ghost" href="${project.demo}" ${project.demo === '#' ? 'aria-disabled="true"' : 'target="_blank" rel="noreferrer"'}>Demo</a>
              <a class="btn btn-primary" href="#projects">View Project</a>
            </div>
          </div>`;
        projectRoot.appendChild(card);
      });
    activateReveal();
  };

  categories.forEach(cat => {
    const btn = document.createElement('button');
    btn.className = `filter-btn${cat === 'All' ? ' active' : ''}`;
    btn.type = 'button';
    btn.textContent = cat;
    btn.addEventListener('click', () => {
      projectFilters.querySelectorAll('button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderProjects(cat);
    });
    projectFilters.appendChild(btn);
  });

  const featured = window.PROJECTS_DATA.find(project => project.featured);
  if (featured) {
    document.getElementById('featured-body').innerHTML = `
      <h3>${featured.title}</h3>
      <p>${featured.description}</p>
      <div class="tags">${featured.technologies.map(t => `<span class="tag">${t}</span>`).join('')}</div>
      <div class="links-row">
        <a class="btn btn-primary" href="${featured.github}" target="_blank" rel="noreferrer">GitHub</a>
      </div>`;
  }

  const blogPreview = document.getElementById('blog-preview-root');
  window.BLOG_POSTS.slice(0, 3).forEach(post => {
    const mins = Math.max(1, Math.ceil(post.content.join(' ').split(/\s+/).length / 180));
    const card = document.createElement('article');
    card.className = 'blog-card reveal';
    card.innerHTML = `
      <img src="${post.coverImage}" alt="${post.title}" loading="lazy"/>
      <div class="card-body">
        <div class="meta">${post.category} · ${mins} min read</div>
        <h3>${post.title}</h3>
        <p>${post.summary}</p>
        <a class="btn btn-ghost" href="blog/post.html?slug=${post.slug}">Read Article</a>
      </div>`;
    blogPreview.appendChild(card);
  });

  const sectionMap = new Map();
  document.querySelectorAll('.nav-links a[href^="#"]').forEach(link => {
    const section = document.querySelector(link.getAttribute('href'));
    if (section) sectionMap.set(section, link);
  });
  if ('IntersectionObserver' in window) {
    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          sectionMap.forEach(link => link.classList.remove('active'));
          const active = sectionMap.get(entry.target);
          if (active) active.classList.add('active');
        }
      });
    }, { threshold: .45 });
    sectionMap.forEach((_, section) => sectionObserver.observe(section));
  }

  function activateReveal() {
    if (reduceMotion || !('IntersectionObserver' in window)) {
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
      return;
    }
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: .16 });
    document.querySelectorAll('.reveal:not(.in)').forEach(el => observer.observe(el));
  }

  renderProjects();
  activateReveal();
})();

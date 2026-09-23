# Mehmet Akif ÇAKIR Portfolio + Technical Blog

Dark-first, responsive, GitHub Pages-ready personal portfolio and blog for **Mehmet Akif ÇAKIR** (Mechatronics Engineering Student).

## Run locally

This project is static HTML/CSS/JS, so any static server works.

```bash
cd /home/runner/work/ma_cakr/ma_cakr
python -m http.server 8000
# open http://localhost:8000
```

## Build

No build step required.

## Frequently edited files

- `/data/site-data.js` → personal profile, social links, skills, projects, blog posts
- `/index.html` → section structure/content
- `/blog/index.html` + `/blog/post.html` → blog list and article route templates
- `/css/style.css` → design/theme/responsive styles
- `/public/images/projects/*` + `/public/images/blog/*` → project/blog images
- `/public/cv.pdf` → your real CV file

## Add a new project

Edit `window.PROJECTS_DATA` in `/data/site-data.js`:

```js
{
  id: 'project-id',
  title: 'Project title',
  description: 'Short summary',
  technologies: ['Tech1', 'Tech2'],
  category: 'Robotics',
  image: '/public/images/projects/your-image.svg',
  github: 'https://github.com/your-user/your-repo',
  demo: 'https://your-demo-url'
}
```

Valid categories used by filters: `Robotics`, `Software`, `Electronics`, `Engineering`, `AI`.

## Add a new blog post

Edit `window.BLOG_POSTS` in `/data/site-data.js`:

```js
{
  slug: 'your-post-slug',
  title: 'Post title',
  date: '2026-09-23',
  category: 'Programming',
  tags: ['Tag1', 'Tag2'],
  coverImage: '/public/images/blog/your-cover.svg',
  summary: 'Card summary',
  content: ['Paragraph 1', 'Paragraph 2'],
  placeholder: false
}
```

## Change personal information

Update `window.SITE_DATA` in `/data/site-data.js`:
- name/role/tagline
- GitHub + LinkedIn URLs
- contact email (`your-email@example.com` placeholder)

## Add your CV

Replace `/public/cv.pdf` with your actual PDF using the same filename.

## Replace images

- Project images: `/public/images/projects/`
- Blog images: `/public/images/blog/`
- OG preview image: `/public/images/profile/og-preview.svg`

## GitHub Pages deployment

1. Push repository to GitHub.
2. In repository settings, enable **Pages** from the target branch (root).
3. Ensure these files stay in root:
   - `CNAME`
   - `sitemap.xml`
   - `robots.txt`

## Custom domain setup

1. Replace `YOUR-DOMAIN.com` in:
   - `/CNAME`
   - canonical/OG URLs in `/index.html`, `/blog/index.html`, `/blog/post.html`
   - `/sitemap.xml` and `/robots.txt`
2. Configure DNS records at your domain provider for GitHub Pages.
3. Re-deploy and verify HTTPS in GitHub Pages settings.

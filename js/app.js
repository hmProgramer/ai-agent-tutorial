/**
 * AI Agent Tutorial - Application Logic
 */

// ========== State ==========
const state = {
  currentPage: null,
  sidebarOpen: false,
  searchQuery: '',
};

// ========== Page Routing ==========
function getPageId() {
  const hash = window.location.hash.slice(1);
  return hash || 'ai-agent-tutorial';
}

function navigateTo(pageId, pushState = true) {
  if (pushState) {
    window.location.hash = pageId;
    return; // hash change event will call renderPage
  }
  renderPage(pageId);
}

function renderPage(pageId) {
  state.currentPage = pageId;
  const page = PAGE_DATA[pageId];

  if (!page) {
    document.getElementById('articleContent').innerHTML = `
      <h1>404 - 页面未找到</h1>
      <p>抱歉，找不到页面 "${pageId}"。</p>
      <a href="#ai-agent-tutorial">返回首页</a>
    `;
    return;
  }

  // Update title
  document.title = page.title + ' | AI Agent 教程';

  // Render content
  const contentEl = document.getElementById('articleContent');
  contentEl.innerHTML = renderArticle(page);

  // Update sidebar active
  updateSidebarActive(pageId);

  // Scroll to top
  window.scrollTo(0, 0);

  // Close mobile sidebar
  closeSidebar();
}

function renderArticle(page) {
  const prevLink = page.prev ? `
    <a href="#${page.prev.id}" onclick="navigateTo('${page.prev.id}')">
      <i class="fas fa-arrow-left"></i> ${page.prev.title}
    </a>` : '<span></span>';

  const nextLink = page.next ? `
    <a href="#${page.next.id}" onclick="navigateTo('${page.next.id}')">
      ${page.next.title} <i class="fas fa-arrow-right"></i>
    </a>` : '<span></span>';

  return `
    ${page.content}
    <div class="page-nav">
      ${prevLink}
      ${nextLink}
    </div>
  `;
}

// ========== Sidebar ==========
function buildSidebar() {
  const nav = document.getElementById('sidebarNav');
  let html = '';

  SIDEBAR_DATA.forEach(section => {
    html += `<div class="sidebar-section">`;
    html += `<div class="sidebar-category">${section.title}</div>`;
    section.items.forEach(item => {
      html += `<a href="#${item.id}" data-page="${item.id}">${item.title}</a>`;
    });
    html += `</div>`;
  });

  nav.innerHTML = html;

  // Add click handlers
  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const pageId = this.dataset.page;
      navigateTo(pageId);
    });
  });
}

function updateSidebarActive(pageId) {
  const nav = document.getElementById('sidebarNav');
  nav.querySelectorAll('a').forEach(link => {
    link.classList.toggle('active', link.dataset.page === pageId);
  });
}

// ========== Mobile Sidebar ==========
function toggleSidebar() {
  if (state.sidebarOpen) {
    closeSidebar();
  } else {
    openSidebar();
  }
}

function openSidebar() {
  state.sidebarOpen = true;
  document.getElementById('sidebar').classList.add('open');
  document.getElementById('sidebarOverlay').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeSidebar() {
  state.sidebarOpen = false;
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('sidebarOverlay').classList.remove('open');
  document.body.style.overflow = '';
}

// ========== Search ==========
function initSearch() {
  const searchInput = document.getElementById('searchInput');
  let debounceTimer;

  searchInput.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      performSearch(this.value);
    }, 300);
  });

  // Build search index
  buildSearchIndex();
}

let searchIndex = [];

function buildSearchIndex() {
  searchIndex = [];
  for (const [id, page] of Object.entries(PAGE_DATA)) {
    // Strip HTML tags for search
    const textContent = page.content.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ');
    searchIndex.push({
      id: id,
      title: page.title,
      text: textContent.toLowerCase(),
    });
  }
}

function performSearch(query) {
  state.searchQuery = query.trim().toLowerCase();
  const nav = document.getElementById('sidebarNav');
  const allLinks = nav.querySelectorAll('a');

  if (!state.searchQuery) {
    // Show all
    allLinks.forEach(link => {
      link.style.display = '';
    });
    nav.querySelectorAll('.sidebar-category').forEach(cat => {
      cat.style.display = '';
    });
    return;
  }

  // Search through index
  const matchedIds = new Set();
  searchIndex.forEach(item => {
    if (item.title.toLowerCase().includes(state.searchQuery) ||
        item.text.includes(state.searchQuery)) {
      matchedIds.add(item.id);
    }
  });

  // Show/hide links based on search
  allLinks.forEach(link => {
    const pageId = link.dataset.page;
    if (matchedIds.has(pageId)) {
      link.style.display = '';
      link.style.background = 'rgba(59, 130, 246, 0.15)';
    } else {
      link.style.display = 'none';
      link.style.background = '';
    }
  });

  // Hide empty categories
  nav.querySelectorAll('.sidebar-section').forEach(section => {
    const visibleLinks = section.querySelectorAll('a[style*="display: none"], a:not([style*="display"])');
    let hasVisible = false;
    section.querySelectorAll('a').forEach(a => {
      if (a.style.display !== 'none') hasVisible = true;
    });
    const cat = section.querySelector('.sidebar-category');
    if (cat) cat.style.display = hasVisible ? '' : 'none';
  });
}

// ========== Theme ==========
function initTheme() {
  const toggle = document.getElementById('themeToggle');
  const icon = document.getElementById('themeIcon');
  const text = document.getElementById('themeText');

  // Load saved theme
  const savedTheme = localStorage.getItem('ai-tutorial-theme') || 'light';
  applyTheme(savedTheme);

  toggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    localStorage.setItem('ai-tutorial-theme', next);
  });
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  const icon = document.getElementById('themeIcon');
  const text = document.getElementById('themeText');
  if (icon && text) {
    if (theme === 'dark') {
      icon.className = 'fas fa-sun';
      text.textContent = '亮色';
    } else {
      icon.className = 'fas fa-moon';
      text.textContent = '暗色';
    }
  }
}

// ========== Init ==========
function init() {
  buildSidebar();
  initTheme();
  initSearch();
  renderPage(getPageId());

  // Sidebar toggle (mobile)
  document.getElementById('sidebarToggle').addEventListener('click', toggleSidebar);
  document.getElementById('sidebarOverlay').addEventListener('click', closeSidebar);

  // Hash change
  window.addEventListener('hashchange', () => {
    renderPage(getPageId());
  });

  // Keyboard shortcut: Ctrl+K for search
  document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      document.getElementById('searchInput').focus();
    }
  });
}

// Start
document.addEventListener('DOMContentLoaded', init);

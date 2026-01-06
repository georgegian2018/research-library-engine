const API = ""; // same origin (served by FastAPI)

let selectedPaperId = null;
let selectedPaperTitle = null;

function $(id) { return document.getElementById(id); }

function setStatus(el, msg) {
  el.textContent = msg || "";
}

async function apiGet(path) {
  const res = await fetch(API + path);
  if (!res.ok) throw new Error(`GET ${path} -> ${res.status}`);
  return res.json();
}

async function apiPost(path, body) {
  // send as query params for simple FastAPI function params
  const url = new URL(API + path, window.location.origin);
  Object.entries(body || {}).forEach(([k, v]) => url.searchParams.set(k, v));
  const res = await fetch(url.toString(), { method: "POST" });
  if (!res.ok) throw new Error(`POST ${path} -> ${res.status}`);
  return res.json();
}

function switchView(view) {
  document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
  document.querySelector(`.tab[data-view="${view}"]`).classList.add("active");

  ["papers", "projects", "dedup"].forEach(v => {
    const el = document.getElementById(`view-${v}`);
    el.classList.toggle("hidden", v !== view);
  });
}

function renderPapersTable(rows) {
  const tbody = $("papersTbody");
  tbody.innerHTML = "";
  for (const r of rows) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${escapeHtml(r.title || "")}</td>
      <td>${escapeHtml(String(r.year || ""))}</td>
      <td>${escapeHtml(r.venue || "")}</td>
      <td>${escapeHtml(r.doi || "")}</td>
      <td><code>${escapeHtml(r.id || "")}</code></td>
    `;
    tr.addEventListener("click", () => selectPaper(r.id, r.title));
    tbody.appendChild(tr);
  }
}

function escapeHtml(s) {
  return (s || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

async function loadPapers() {
  setStatus($("papersStatus"), "Loading papers...");
  try {
    const rows = await apiGet("/papers?limit=200&offset=0");
    renderPapersTable(rows);
    setStatus($("papersStatus"), `Loaded ${rows.length} papers.`);
  } catch (e) {
    setStatus($("papersStatus"), `Error: ${e.message}`);
  }
}

async function searchPapers() {
  const q = $("searchInput").value.trim();
  if (!q) return loadPapers();

  setStatus($("papersStatus"), "Searching...");
  try {
    const rows = await apiGet(`/search?q=${encodeURIComponent(q)}&limit=100`);
    renderPapersTable(rows);
    setStatus($("papersStatus"), `Found ${rows.length} hits.`);
  } catch (e) {
    setStatus($("papersStatus"), `Error: ${e.message}`);
  }
}

async function selectPaper(paperId, title) {
  selectedPaperId = paperId;
  selectedPaperTitle = title || "";
  $("selectedPaperBox").classList.remove("muted");
  $("selectedPaperBox").innerHTML = `
    <div><strong>${escapeHtml(selectedPaperTitle)}</strong></div>
    <div class="status">Paper ID: <code>${escapeHtml(selectedPaperId)}</code></div>
  `;

  await loadTags();
  await loadNote();
}

async function loadTags() {
  if (!selectedPaperId) return;
  try {
    const tags = await apiGet(`/papers/${selectedPaperId}/tags`);
    const box = $("tagsList");
    box.innerHTML = "";
    for (const t of tags) {
      const pill = document.createElement("span");
      pill.className = "pill";
      pill.textContent = t;
      box.appendChild(pill);
    }
  } catch (e) {
    $("tagsList").innerHTML = `<span class="status">Error loading tags: ${escapeHtml(e.message)}</span>`;
  }
}

async function addTag() {
  const tag = $("tagInput").value.trim();
  if (!selectedPaperId || !tag) return;
  try {
    await apiPost(`/papers/${selectedPaperId}/tags`, { tag });
    $("tagInput").value = "";
    await loadTags();
  } catch (e) {
    $("tagsList").innerHTML = `<span class="status">Error adding tag: ${escapeHtml(e.message)}</span>`;
  }
}

async function loadNote() {
  if (!selectedPaperId) return;
  setStatus($("noteStatus"), "Loading note...");
  try {
    const data = await apiGet(`/papers/${selectedPaperId}/note`);
    $("noteArea").value = data.content_md || "";
    setStatus($("noteStatus"), "Loaded.");
  } catch (e) {
    setStatus($("noteStatus"), `Error: ${e.message}`);
  }
}

async function saveNote() {
  if (!selectedPaperId) return;
  setStatus($("noteStatus"), "Saving...");
  try {
    const content_md = $("noteArea").value;
    await apiPost(`/papers/${selectedPaperId}/note`, { content_md });
    setStatus($("noteStatus"), "Saved.");
  } catch (e) {
    setStatus($("noteStatus"), `Error: ${e.message}`);
  }
}

async function loadProjects() {
  setStatus($("projectsStatus"), "Loading projects...");
  try {
    const projects = await apiGet("/projects");
    const tbody = $("projectsTbody");
    tbody.innerHTML = "";
    for (const p of projects) {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><code>${escapeHtml(String(p.id))}</code></td>
        <td>${escapeHtml(p.name || "")}</td>
        <td>${escapeHtml(p.description || "")}</td>
      `;
      tbody.appendChild(tr);
    }
    setStatus($("projectsStatus"), `Loaded ${projects.length} projects.`);
  } catch (e) {
    setStatus($("projectsStatus"), `Error: ${e.message}`);
  }
}

async function createProject() {
  const name = $("projectName").value.trim();
  const description = $("projectDesc").value.trim();
  if (!name) return;
  setStatus($("projectsStatus"), "Creating project...");
  try {
    await apiPost("/projects", { name, description });
    $("projectName").value = "";
    $("projectDesc").value = "";
    await loadProjects();
    setStatus($("projectsStatus"), "Created.");
  } catch (e) {
    setStatus($("projectsStatus"), `Error: ${e.message}`);
  }
}

async function loadProjectPapers() {
  const projectId = $("projectIdForPapers").value.trim();
  if (!projectId) return;
  setStatus($("projectPapersStatus"), "Loading project papers...");
  try {
    const papers = await apiGet(`/projects/${encodeURIComponent(projectId)}/papers`);
    const ul = $("projectPapersList");
    ul.innerHTML = "";
    for (const p of papers) {
      const li = document.createElement("li");
      li.textContent = p.title || p.id;
      ul.appendChild(li);
    }
    setStatus($("projectPapersStatus"), `Loaded ${papers.length} papers.`);
  } catch (e) {
    setStatus($("projectPapersStatus"), `Error: ${e.message}`);
  }
}

async function runDedup() {
  const raw = $("dedupThreshold").value.trim();
  const threshold = raw ? Number(raw) : 0.85;
  setStatus($("dedupStatus"), "Running dedup report...");
  try {
    const rows = await apiGet(`/dedup/report?threshold=${encodeURIComponent(threshold)}`);
    const tbody = $("dedupTbody");
    tbody.innerHTML = "";
    for (const r of rows) {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><code>${escapeHtml(String(r.score))}</code></td>
        <td>${escapeHtml(r.paper_1_title || "")}</td>
        <td>${escapeHtml(r.paper_2_title || "")}</td>
      `;
      tbody.appendChild(tr);
    }
    setStatus($("dedupStatus"), `Found ${rows.length} possible duplicate pairs.`);
  } catch (e) {
    setStatus($("dedupStatus"), `Error: ${e.message}`);
  }
}

// Wire UI events
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".tab").forEach(btn => {
    btn.addEventListener("click", () => switchView(btn.dataset.view));
  });

  $("searchBtn").addEventListener("click", searchPapers);
  $("reloadPapersBtn").addEventListener("click", loadPapers);

  $("addTagBtn").addEventListener("click", addTag);
  $("loadNoteBtn").addEventListener("click", loadNote);
  $("saveNoteBtn").addEventListener("click", saveNote);

  $("reloadProjectsBtn").addEventListener("click", loadProjects);
  $("createProjectBtn").addEventListener("click", createProject);
  $("loadProjectPapersBtn").addEventListener("click", loadProjectPapers);

  $("runDedupBtn").addEventListener("click", runDedup);

  // initial load
  loadPapers();
});

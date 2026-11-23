import { useEffect, useMemo, useState } from 'react';
import { api, geometryPayload } from './api/client.js';

const bridgeTypes = [
  { value: 'plate_girder', label: 'Plate girder' },
  { value: 'box_girder', label: 'Box girder' },
  { value: 'truss', label: 'Truss' },
];

function typeLabel(value) {
  return bridgeTypes.find((item) => item.value === value)?.label || value;
}

function App() {
  const [user, setUser] = useState(null);
  const [projects, setProjects] = useState([]);
  const [page, setPage] = useState('home');
  const [activeId, setActiveId] = useState(null);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [showCreate, setShowCreate] = useState(false);

  const activeProject = useMemo(
    () => projects.find((item) => String(item.id) === String(activeId)) || null,
    [projects, activeId],
  );

  async function refreshProjects() {
    const next = await api.projects();
    setProjects(next);
    return next;
  }

  useEffect(() => {
    let mounted = true;
    api.profile()
      .then(async (profile) => {
        if (!mounted) return;
        setUser(profile);
        await refreshProjects();
        if (mounted) setPage('dashboard');
      })
      .catch((err) => {
        if (mounted && err.status !== 401 && err.status !== 403) setError(err.message);
      })
      .finally(() => mounted && setBusy(false));
    return () => { mounted = false; };
  }, []);

  function flash(message) {
    setNotice(message);
    window.setTimeout(() => setNotice(''), 3200);
  }

  async function handleAuthenticated(profile) {
    setUser(profile);
    setError('');
    setPage('dashboard');
    await refreshProjects();
  }

  async function handleLogout() {
    try {
      await api.logout();
      setUser(null);
      setProjects([]);
      setActiveId(null);
      setPage('home');
      flash('You are signed out.');
    } catch (err) {
      setError(err.message);
    }
  }

  async function saveProject(form, existing = null) {
    setError('');
    const geometry = geometryPayload(form.span_m, form.width_m);
    try {
      await api.validateGeometry(form.bridge_type, geometry);
      const payload = {
        name: form.name.trim(),
        bridge_type: form.bridge_type,
        location: form.location.trim(),
        description: form.description.trim(),
        configuration: {
          ...(existing?.configuration || {}),
          geometry,
        },
      };
      const saved = existing
        ? await api.updateProject(existing.id, payload)
        : await api.createProject(payload);
      await refreshProjects();
      setActiveId(saved.id);
      setPage('project');
      setShowCreate(false);
      flash(existing ? 'Project inputs saved.' : 'Project created and saved to your account.');
    } catch (err) {
      setError(err.message || 'Could not save this project.');
    }
  }

  async function deleteProject(project) {
    if (!window.confirm(`Delete “${project.name}”? This removes its saved project inputs.`)) return;
    try {
      await api.deleteProject(project.id);
      setProjects((previous) => previous.filter((item) => item.id !== project.id));
      if (String(activeId) === String(project.id)) {
        setActiveId(null);
        setPage('dashboard');
      }
      flash('Project deleted.');
    } catch (err) {
      setError(err.message);
    }
  }

  async function exportProject(project) {
    try {
      const blob = await api.exportProject(project.id);
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement('a');
      anchor.href = url;
      anchor.download = `osdagbridge-project-${project.id}.json`;
      anchor.click();
      URL.revokeObjectURL(url);
      flash('Saved project inputs exported as JSON.');
    } catch (err) {
      setError(err.message);
    }
  }

  async function saveProfile(values) {
    try {
      const updated = await api.updateProfile(values);
      setUser(updated);
      flash('Profile updated.');
      setPage('dashboard');
    } catch (err) {
      setError(err.message);
    }
  }

  if (busy) return <div className="boot-screen"><span className="brand-mark">O</span><p>Opening engineering workspace…</p></div>;

  if (!user) {
    if (page === 'login' || page === 'register') {
      return <AuthPage mode={page} onMode={setPage} onAuthenticated={handleAuthenticated} error={error} clearError={() => setError('')} />;
    }
    return <Landing onLogin={() => { setError(''); setPage('login'); }} onRegister={() => { setError(''); setPage('register'); }} />;
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <button className="brand" onClick={() => setPage('dashboard')} aria-label="OsdagBridge dashboard">
          <span className="brand-mark">O</span><span>Osdag<span className="brand-light">Bridge</span></span>
        </button>
        <div className="workspace-label">WORKSPACE</div>
        <nav className="side-nav" aria-label="Workspace navigation">
          <button className={page === 'dashboard' ? 'nav-item active' : 'nav-item'} onClick={() => setPage('dashboard')}><span>▦</span> Projects</button>
          <button className={page === 'settings' ? 'nav-item active' : 'nav-item'} onClick={() => setPage('settings')}><span>⚙</span> Profile settings</button>
        </nav>
        <div className="sidebar-bottom">
          <div className="sidebar-note"><span className="status-dot" /> Project records are private to your account.</div>
          <button className="nav-item signout" onClick={handleLogout}><span>↗</span> Sign out</button>
        </div>
      </aside>
      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumb"><span>Workspace</span><b>/</b><strong>{page === 'project' ? (activeProject?.name || 'Project') : page === 'settings' ? 'Profile settings' : 'Projects'}</strong></div>
          <div className="user-chip"><span className="avatar">{(user.first_name || user.username || 'U').slice(0, 1).toUpperCase()}</span><span>{user.first_name || user.username}</span></div>
        </header>
        {error && <div className="alert error-alert" role="alert"><span>{error}</span><button onClick={() => setError('')} aria-label="Dismiss">×</button></div>}
        {notice && <div className="toast" role="status">{notice}</div>}
        {page === 'dashboard' && <Dashboard projects={projects} onCreate={() => setShowCreate(true)} onOpen={(item) => { setActiveId(item.id); setPage('project'); }} onDelete={deleteProject} />}
        {page === 'project' && activeProject && <ProjectEditor key={activeProject.id} project={activeProject} onSave={(values) => saveProject(values, activeProject)} onExport={() => exportProject(activeProject)} onDelete={() => deleteProject(activeProject)} />}
        {page === 'settings' && <ProfileSettings user={user} onSave={saveProfile} />}
        {showCreate && <ProjectDialog onClose={() => setShowCreate(false)} onSave={(values) => saveProject(values)} />}
      </main>
    </div>
  );
}

function Landing({ onLogin, onRegister }) {
  return (
    <div className="landing">
      <header className="landing-nav"><div className="brand"><span className="brand-mark">O</span><span>Osdag<span className="brand-light">Bridge</span></span></div><div className="nav-actions"><button className="button ghost" onClick={onLogin}>Sign in</button><button className="button primary" onClick={onRegister}>Create account <span>↗</span></button></div></header>
      <section className="hero">
        <div className="hero-copy"><div className="eyebrow"><span className="status-dot" /> PROJECT WORKSPACE · EARLY ACCESS</div><h1>Bridge design starts with <em>clear inputs.</em></h1><p>Organize bridge project records, geometry inputs and design context in one private workspace. Structural analysis is not yet available in this web application.</p><div className="hero-actions"><button className="button primary large" onClick={onRegister}>Create your workspace <span>→</span></button><button className="button text-button" onClick={onLogin}>I already have an account</button></div><div className="hero-meta"><span>01&nbsp; Projects</span><span>02&nbsp; Geometry records</span><span>03&nbsp; Input export</span></div></div>
        <div className="hero-visual" aria-label="Abstract bridge line illustration"><div className="visual-tag">MODEL INPUTS <span>01 — 03</span></div><svg viewBox="0 0 620 390" role="img" aria-label="Line drawing of a bridge span"><defs><linearGradient id="bridgeFade" x1="0" x2="1"><stop offset="0" stopColor="#36b3a2" stopOpacity=".16"/><stop offset="1" stopColor="#36b3a2" stopOpacity=".75"/></linearGradient></defs><path d="M34 274H586" stroke="#547184" strokeWidth="2"/><path d="M72 255H548M94 255L116 274M154 255L176 274M214 255L236 274M274 255L296 274M334 255L356 274M394 255L416 274M454 255L476 274M514 255L536 274" stroke="#82a5ae" strokeWidth="2"/><path d="M100 254Q310 68 520 254" fill="none" stroke="url(#bridgeFade)" strokeWidth="5"/><path d="M100 254L100 175M160 254L160 130M220 254L220 101M280 254L280 88M340 254L340 90M400 254L400 105M460 254L460 135M520 254L520 176" stroke="#36b3a2" strokeOpacity=".58" strokeWidth="1.5" strokeDasharray="4 7"/><circle cx="310" cy="88" r="5" fill="#f3b65c"/><circle cx="100" cy="254" r="4" fill="#36b3a2"/><circle cx="520" cy="254" r="4" fill="#36b3a2"/><path d="M100 304H520M100 296V312M520 296V312" stroke="#d69a43" strokeWidth="1.5"/><text x="310" y="328" textAnchor="middle" fill="#bdced2" fontSize="12" letterSpacing="3">PROJECT GEOMETRY</text><path d="M50 85h38M69 66v38M550 105h32M566 89v32" stroke="#547184" strokeWidth="1"/><circle cx="69" cy="85" r="2" fill="#f3b65c"/></svg><div className="visual-caption"><span>RECORDS BEFORE RESULTS</span><span>OsdagBridge / 0.1</span></div></div>
      </section>
      <section className="feature-strip"><article><span className="feature-index">01</span><h3>Private project records</h3><p>Each account can access only its own saved bridge projects.</p></article><article><span className="feature-index">02</span><h3>Inputs with context</h3><p>Store project metadata and basic geometry values with units.</p></article><article><span className="feature-index">03</span><h3>Honest status</h3><p>Input validation is not analysis; unsupported calculations stay unavailable.</p></article></section>
      <footer className="landing-footer"><span>OSDAGBRIDGE · ENGINEERING WORKSPACE</span><span>Analysis and design services are not yet connected to the web application.</span></footer>
    </div>
  );
}

function AuthPage({ mode, onMode, onAuthenticated, error, clearError }) {
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const [busy, setBusy] = useState(false);
  const [localError, setLocalError] = useState('');
  const isRegister = mode === 'register';

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setLocalError('');
    clearError();
    try {
      const profile = isRegister ? await api.register(form) : await api.login(form);
      await onAuthenticated(profile);
    } catch (err) {
      const detail = err.payload && typeof err.payload === 'object'
        ? Object.values(err.payload).flat().join(' ')
        : err.message;
      setLocalError(detail || err.message);
    } finally {
      setBusy(false);
    }
  }

  return <div className="auth-page"><div className="auth-aside"><button className="brand" onClick={() => onMode('home')}><span className="brand-mark">O</span><span>Osdag<span className="brand-light">Bridge</span></span></button><div className="auth-aside-copy"><span className="eyebrow">PROJECT WORKSPACE</span><h1>Engineering records, kept in context.</h1><p>Sign in to create and manage your private bridge project inputs.</p></div><span className="auth-aside-foot">OSDAGBRIDGE · 0.1</span></div><main className="auth-main"><button className="back-link" onClick={() => onMode('home')}>← Back to overview</button><div className="auth-card"><div className="eyebrow">{isRegister ? 'NEW WORKSPACE' : 'ACCOUNT ACCESS'}</div><h2>{isRegister ? 'Create your account' : 'Sign in'}</h2><p className="muted">{isRegister ? 'Save your bridge project records securely.' : 'Continue to your engineering workspace.'}</p>{(localError || error) && <div className="alert error-alert" role="alert">{localError || error}</div>}<form onSubmit={submit} className="form-stack">{isRegister && <label>Email address<input type="email" autoComplete="email" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></label>}<label>Username<input autoComplete="username" required value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} /></label><label>Password<input type="password" autoComplete={isRegister ? 'new-password' : 'current-password'} minLength={isRegister ? 8 : undefined} required value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />{isRegister && <small>At least 8 characters; Django password strength checks apply.</small>}</label><button className="button primary full" disabled={busy}>{busy ? 'Please wait…' : isRegister ? 'Create account' : 'Sign in'} <span>→</span></button></form><div className="auth-switch">{isRegister ? 'Already registered?' : 'New to OsdagBridge?'} <button onClick={() => { setLocalError(''); onMode(isRegister ? 'login' : 'register'); }}>{isRegister ? 'Sign in' : 'Create account'}</button></div><div className="auth-security">Session-based sign-in · Your projects are owner-scoped</div></div></main></div>;
}

function Dashboard({ projects, onCreate, onOpen, onDelete }) {
  return <section className="page-content"><div className="page-heading"><div><div className="eyebrow">PROJECT OVERVIEW</div><h1>Your bridge projects</h1><p>Saved project inputs and records. No structural analysis has been run.</p></div><button className="button primary" onClick={onCreate}>＋ New project</button></div><div className="stat-row"><div className="stat-card"><span>PROJECTS</span><strong>{projects.length}</strong><small>Saved to your account</small></div><div className="stat-card"><span>ANALYSIS</span><strong className="stat-unavailable">Not connected</strong><small>No web solver results available</small></div><div className="stat-card"><span>DATA ACCESS</span><strong className="stat-private">Private</strong><small>Projects are scoped to your user</small></div></div><div className="section-title"><div><h2>Project register</h2><p>Most recently updated records</p></div><span className="record-count">{projects.length} {projects.length === 1 ? 'record' : 'records'}</span></div>{projects.length === 0 ? <div className="empty-state"><div className="empty-icon">＋</div><h3>No projects yet</h3><p>Create a project to save its name, bridge type, location and geometry inputs.</p><button className="button secondary" onClick={onCreate}>Create first project</button></div> : <div className="project-list">{projects.map((project) => <article className="project-row" key={project.id}><div className="project-type-icon">{project.bridge_type === 'truss' ? '△' : project.bridge_type === 'box_girder' ? '▱' : '═'}</div><div className="project-main"><button className="project-name" onClick={() => onOpen(project)}>{project.name}</button><div className="project-sub">{typeLabel(project.bridge_type)}{project.location ? ` · ${project.location}` : ''}</div></div><div className="project-span">{project.configuration?.geometry?.span_m ? `${project.configuration.geometry.span_m} m span` : 'Geometry not entered'}</div><div className="project-status"><span className="status-dot muted-dot" /> Inputs saved</div><button className="icon-button danger-on-hover" onClick={() => onDelete(project)} aria-label={`Delete ${project.name}`}>⌫</button><button className="icon-button open-arrow" onClick={() => onOpen(project)} aria-label={`Open ${project.name}`}>↗</button></article>)}</div>}</section>;
}

function ProjectDialog({ onClose, onSave }) {
  return <ProjectForm title="Create bridge project" subtitle="Start with project context and optional geometry measurements." onClose={onClose} onSave={(values) => onSave(values)} submitLabel="Create project" />;
}

function ProjectEditor({ project, onSave, onExport, onDelete }) {
  const form = {
    name: project.name || '', bridge_type: project.bridge_type || 'plate_girder',
    location: project.location || '', description: project.description || '',
    span_m: project.configuration?.geometry?.span_m ?? '',
    width_m: project.configuration?.geometry?.width_m ?? '',
  };
  const [values, setValues] = useState(form);
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState('');
  async function submit(event) {
    event.preventDefault();
    setSaving(true); setSaveError('');
    try { await onSave(values); } catch (err) { setSaveError(err.message); }
    finally { setSaving(false); }
  }
  function field(key, value) { setValues((current) => ({ ...current, [key]: value })); }
  return <section className="page-content"><div className="page-heading"><div><div className="eyebrow">PROJECT {project.id} · INPUT RECORD</div><h1>{project.name}</h1><p>Update project metadata and basic geometry. Saving does not run analysis.</p></div><div className="heading-actions"><button className="button secondary" onClick={onExport}>↓ Export inputs</button><button className="button danger" onClick={onDelete}>Delete</button></div></div><form className="editor-layout" onSubmit={submit}><div className="editor-main"><div className="panel"><div className="panel-heading"><div><h2>Project details</h2><p>Account-owned project metadata</p></div><span className="panel-step">01</span></div><div className="field-grid"><label className="wide">Project name<input required maxLength={180} value={values.name} onChange={(e) => field('name', e.target.value)} /></label><label>Bridge type<select value={values.bridge_type} onChange={(e) => field('bridge_type', e.target.value)}>{bridgeTypes.map((item) => <option key={item.value} value={item.value}>{item.label}</option>)}</select></label><label>Location<input maxLength={180} value={values.location} onChange={(e) => field('location', e.target.value)} placeholder="Optional" /></label><label className="wide">Description<textarea rows="3" value={values.description} onChange={(e) => field('description', e.target.value)} placeholder="Project notes and design context" /></label></div></div><div className="panel"><div className="panel-heading"><div><h2>Geometry inputs</h2><p>Positive finite values are checked as data only.</p></div><span className="panel-step">02</span></div><div className="field-grid"><label>Span <span className="unit">m</span><input type="number" min="0.001" step="any" value={values.span_m} onChange={(e) => field('span_m', e.target.value)} placeholder="Optional" /></label><label>Overall width <span className="unit">m</span><input type="number" min="0.001" step="any" value={values.width_m} onChange={(e) => field('width_m', e.target.value)} placeholder="Optional" /></label></div><div className="inline-note"><span>i</span><p>These fields are not a complete bridge model. No engineering design check or solver result is generated.</p></div></div><div className="panel analysis-panel"><div className="analysis-mark">∿</div><div><h2>Structural analysis</h2><p>Analysis services are not yet connected to this web workspace. This action is intentionally unavailable.</p></div><button type="button" className="button disabled" disabled>Not available</button></div>{saveError && <div className="alert error-alert">{saveError}</div>}</div><aside className="editor-aside"><div className="panel sticky-panel"><div className="eyebrow">RECORD STATUS</div><div className="status-large"><span className="status-dot" /> Inputs saved</div><p>Created {new Date(project.created_at).toLocaleDateString()}</p><p>Last updated {new Date(project.updated_at).toLocaleString()}</p><div className="aside-divider" /><div className="eyebrow">CURRENT SCOPE</div><ul className="scope-list"><li className="scope-done">Project metadata</li><li className="scope-done">Input persistence</li><li>Materials & sections</li><li>Loads & combinations</li><li>Analysis & design results</li><li>Engineering reports</li></ul><button className="button primary full" disabled={saving}>{saving ? 'Saving…' : 'Save project inputs'}</button></div></aside></form></section>;
}

function ProjectForm({ title, subtitle, onClose, onSave, submitLabel }) {
  const [values, setValues] = useState({ name: '', bridge_type: 'plate_girder', location: '', description: '', span_m: '', width_m: '' });
  const [saving, setSaving] = useState(false);
  const [formError, setFormError] = useState('');
  async function submit(event) {
    event.preventDefault(); setSaving(true); setFormError('');
    try { await onSave(values); } catch (err) { setFormError(err.message); }
    finally { setSaving(false); }
  }
  const field = (key, value) => setValues((current) => ({ ...current, [key]: value }));
  return <div className="modal-backdrop" onMouseDown={(event) => event.target === event.currentTarget && onClose()}><div className="modal" role="dialog" aria-modal="true" aria-labelledby="project-dialog-title"><div className="modal-heading"><div><div className="eyebrow">NEW PROJECT RECORD</div><h2 id="project-dialog-title">{title}</h2><p>{subtitle}</p></div><button className="icon-button" onClick={onClose} aria-label="Close dialog">×</button></div><form onSubmit={submit} className="form-stack"><label>Project name<input required maxLength={180} autoFocus value={values.name} onChange={(e) => field('name', e.target.value)} placeholder="e.g. River crossing — Phase 1" /></label><label>Bridge type<select value={values.bridge_type} onChange={(e) => field('bridge_type', e.target.value)}>{bridgeTypes.map((item) => <option key={item.value} value={item.value}>{item.label}</option>)}</select></label><div className="field-grid"><label>Span <span className="unit">m</span><input type="number" min="0.001" step="any" value={values.span_m} onChange={(e) => field('span_m', e.target.value)} placeholder="Optional" /></label><label>Overall width <span className="unit">m</span><input type="number" min="0.001" step="any" value={values.width_m} onChange={(e) => field('width_m', e.target.value)} placeholder="Optional" /></label></div><label>Location<input maxLength={180} value={values.location} onChange={(e) => field('location', e.target.value)} placeholder="Optional" /></label><label>Description<textarea rows="2" value={values.description} onChange={(e) => field('description', e.target.value)} placeholder="Project notes" /></label>{formError && <div className="alert error-alert">{formError}</div>}<div className="modal-actions"><button type="button" className="button ghost" onClick={onClose}>Cancel</button><button className="button primary" disabled={saving}>{saving ? 'Saving…' : submitLabel}</button></div></form></div></div>;
}

function ProfileSettings({ user, onSave }) {
  const [values, setValues] = useState({ email: user.email || '', first_name: user.first_name || '', last_name: user.last_name || '', organization: user.organization || '', job_title: user.job_title || '' });
  const [saving, setSaving] = useState(false);
  async function submit(event) { event.preventDefault(); setSaving(true); await onSave(values); setSaving(false); }
  return <section className="page-content narrow-content"><div className="page-heading"><div><div className="eyebrow">ACCOUNT</div><h1>Profile settings</h1><p>Update the contact and workspace details associated with your account.</p></div></div><form className="panel form-stack" onSubmit={submit}><div className="panel-heading"><div><h2>Personal details</h2><p>Username: {user.username} · not editable</p></div></div><label>Email address<input required type="email" value={values.email} onChange={(e) => setValues({ ...values, email: e.target.value })} /></label><div className="field-grid"><label>First name<input value={values.first_name} onChange={(e) => setValues({ ...values, first_name: e.target.value })} /></label><label>Last name<input value={values.last_name} onChange={(e) => setValues({ ...values, last_name: e.target.value })} /></label><label>Organization<input value={values.organization} onChange={(e) => setValues({ ...values, organization: e.target.value })} /></label><label>Role / title<input value={values.job_title} onChange={(e) => setValues({ ...values, job_title: e.target.value })} /></label></div><div className="align-right"><button className="button primary" disabled={saving}>{saving ? 'Saving…' : 'Save profile'}</button></div></form></section>;
}

export default App;

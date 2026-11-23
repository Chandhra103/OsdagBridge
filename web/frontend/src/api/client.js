const API_BASE = (import.meta.env?.VITE_API_BASE || '/api').replace(/\/$/, '');
let csrfToken = '';

export function geometryPayload(span, width) {
  const geometry = {};
  if (span !== '') geometry.span_m = Number(span);
  if (width !== '') geometry.width_m = Number(width);
  return geometry;
}

export class ApiError extends Error {
  constructor(message, status, payload) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.payload = payload;
  }
}

async function decode(response) {
  if (response.status === 204) return null;
  const type = response.headers.get('content-type') || '';
  if (type.includes('application/json')) return response.json();
  return response.text();
}

async function csrf() {
  if (csrfToken) return csrfToken;
  const response = await fetch(`${API_BASE}/auth/csrf/`, { credentials: 'include' });
  const payload = await decode(response);
  if (!response.ok) throw new ApiError('Could not initialize the secure session.', response.status, payload);
  csrfToken = payload.csrfToken;
  return csrfToken;
}

async function request(path, options = {}) {
  const method = (options.method || 'GET').toUpperCase();
  const headers = new Headers(options.headers || {});
  headers.set('Accept', 'application/json');
  let body = options.body;
  if (body !== undefined && !(body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
    body = JSON.stringify(body);
  }
  if (!['GET', 'HEAD', 'OPTIONS', 'TRACE'].includes(method)) {
    headers.set('X-CSRFToken', await csrf());
  }
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    method,
    headers,
    body,
    credentials: 'include',
  });
  const payload = await decode(response);
  if (!response.ok) {
    if (response.status === 403) csrfToken = '';
    const message = payload?.detail || payload?.message || `Request failed (${response.status}).`;
    throw new ApiError(message, response.status, payload);
  }
  return payload;
}

export const api = {
  profile: () => request('/auth/me/'),
  async login(values) {
    const profile = await request('/auth/login/', { method: 'POST', body: values });
    csrfToken = '';
    return profile;
  },
  async register(values) {
    const profile = await request('/auth/register/', { method: 'POST', body: values });
    csrfToken = '';
    return profile;
  },
  logout: () => request('/auth/logout/', { method: 'POST' }),
  updateProfile: (values) => request('/auth/me/', { method: 'PATCH', body: values }),
  async projects() {
    const result = await request('/projects/');
    return Array.isArray(result) ? result : (result?.results || []);
  },
  createProject: (values) => request('/projects/', { method: 'POST', body: values }),
  updateProject: (id, values) => request(`/projects/${id}/`, { method: 'PATCH', body: values }),
  deleteProject: (id) => request(`/projects/${id}/`, { method: 'DELETE' }),
  validateGeometry: (bridgeType, geometry) => request('/geometry/validate/', {
    method: 'POST', body: { bridge_type: bridgeType, geometry },
  }),
  async exportProject(id) {
    const response = await fetch(`${API_BASE}/projects/${id}/export/`, { credentials: 'include' });
    if (!response.ok) throw new ApiError('Project export failed.', response.status, await decode(response));
    return response.blob();
  },
};

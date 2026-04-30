// API utility with retry logic and error handling
const MAX_RETRIES = 3;
const RETRY_DELAY = 1000; // 1 second
const BASE_URL = '/api';

/**
 * Sleep utility for retry delays
 */
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Sanitize user input to prevent XSS
 */
export const sanitizeInput = (input) => {
  if (typeof input !== 'string') return input;
  return input
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;');
};

/**
 * Fetch with retry logic
 */
export const fetchWithRetry = async (url, options = {}, retries = MAX_RETRIES) => {
  try {
    const response = await fetch(`${BASE_URL}${url}`, options);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response;
  } catch (error) {
    if (retries > 0) {
      console.warn(`Retrying... (${MAX_RETRIES - retries + 1}/${MAX_RETRIES})`, error.message);
      await sleep(RETRY_DELAY);
      return fetchWithRetry(url, options, retries - 1);
    }
    throw error;
  }
};

/**
 * Generic API GET request
 */
export const apiGet = async (endpoint, options = {}) => {
  const response = await fetchWithRetry(endpoint, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });
  return response.json();
};

/**
 * Generic API POST request
 */
export const apiPost = async (endpoint, data, options = {}) => {
  const response = await fetchWithRetry(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    body: JSON.stringify(data),
    ...options,
  });
  return response.json();
};

/**
 * Generic API PUT request
 */
export const apiPut = async (endpoint, data, options = {}) => {
  const response = await fetchWithRetry(endpoint, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    body: JSON.stringify(data),
    ...options,
  });
  return response.json();
};

/**
 * Generic API DELETE request
 */
export const apiDelete = async (endpoint, options = {}) => {
  const response = await fetchWithRetry(endpoint, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });
  return response.json();
};

/**
 * Get authentication token
 */
export const getAuthToken = () => {
  return localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token');
};

/**
 * Set authentication token
 */
export const setAuthToken = (token) => {
  localStorage.setItem('auth_token', token);
};

/**
 * Clear authentication token
 */
export const clearAuthToken = () => {
  localStorage.removeItem('auth_token');
  sessionStorage.removeItem('auth_token');
};

/**
 * API request with authentication
 */
export const authenticatedRequest = async (method, endpoint, data = null) => {
  const token = getAuthToken();
  const options = {
    headers: {},
  };

  if (token) {
    options.headers['Authorization'] = `Bearer ${token}`;
  }

  switch (method.toUpperCase()) {
    case 'GET':
      return apiGet(endpoint, options);
    case 'POST':
      return apiPost(endpoint, data, options);
    case 'PUT':
      return apiPut(endpoint, data, options);
    case 'DELETE':
      return apiDelete(endpoint, options);
    default:
      throw new Error(`Unsupported method: ${method}`);
  }
};

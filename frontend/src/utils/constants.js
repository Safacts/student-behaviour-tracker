// Application constants
export const API_CONFIG = {
  BASE_URL: '/api',
  MAX_RETRIES: 3,
  RETRY_DELAY: 1000,
  TIMEOUT: 30000,
};

export const UI_CONFIG = {
  DEBOUNCE_DELAY: 300,
  TOAST_DURATION: 3000,
  LOADING_TIMEOUT: 10000,
};

export const STUDENT_BEHAVIOR_TAGS = {
  EXCELLENT: 'Excellent',
  GOOD: 'Good',
  AVERAGE: 'Average',
  NEEDS_IMPROVEMENT: 'Needs Improvement',
  AT_RISK: 'At Risk',
};

export const MARKS_THRESHOLDS = {
  EXCELLENT: 75,
  GOOD: 60,
  AVERAGE: 50,
  POOR: 40,
};

export const DISTRACTION_THRESHOLDS = {
  LOW: 3,
  MEDIUM: 5,
  HIGH: 7,
};

export const TIME_THRESHOLDS = {
  MINUTES_PER_WEEK: 300,
  MINUTES_PER_DAY: 60,
};

export const ROLES = {
  DEVELOPER: 'developer',
  STUDENT: 'student',
  FACULTY: 'faculty',
  PARENT: 'parent',
  PRINCIPAL: 'principal',
};

export const CHAT_ROLES = {
  SYSTEM: 'system',
  USER: 'user',
  ASSISTANT: 'assistant',
};

export const WORKFLOW_NODE_TYPES = {
  DATA_QUERY: 'data_query',
  AI_PROCESS: 'ai_process',
  EMAIL_SEND: 'email_send',
  CONDITION: 'condition',
  LOOP: 'loop',
  WEBHOOK: 'webhook',
};

export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
};

export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  USER_PREFERENCES: 'user_preferences',
  WORKFLOW_CONFIGS: 'workflow_configs',
};

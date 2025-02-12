import http from 'k6/http';
import { check } from 'k6';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';

const host = "localhost"

export const options = {
  scenarios: {
    fixed_iterations: {
      executor: 'per-vu-iterations',
      vus: 1000, // Número de usuários virtuais simultâneos
      iterations: 100, // Número de iterações por VU
      maxDuration: '1h', // Tempo máximo permitido para o teste
    },
  },
};

const endpoints = [
  '/',
  '/productpage',
  '/api/v1/products',
  '/api/v1/products/1',
  '/api/v1/products/1/reviews',
  '/api/v1/products/1/ratings',
];

function checkResponse(res) {
  check(res, { 'status was 200': (r) => r.status === 200 });
}

export default function () {
  for (const endpoint of endpoints) {
    const res = http.get(`http://${host}${endpoint}`);
    checkResponse(res);
  }
}

export function handleSummary(data) {
  return {
    'raw-data.json': JSON.stringify(data),
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
  };
}

import http from 'k6/http';
import { check } from 'k6';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';

// Obtendo valores de variáveis de ambiente ou usando padrões
const VUS = parseInt(__ENV.VUS) || 500; // Número de usuários virtuais simultâneos
const OUTPUT = __ENV.OUTPUT || 'raw-data.json'; // Nome do arquivo de saída

export const options = {
  scenarios: {
    fixed_iterations: {
      executor: 'per-vu-iterations',
      vus: VUS, // Número de usuários virtuais simultâneos
      iterations: 10, // Número de iterações por VU
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
    const res = http.get(`http://localhost${endpoint}`);
    checkResponse(res);
  }
}

export function handleSummary(data) {
  return {
    [OUTPUT]: JSON.stringify(data), // Usa o nome do arquivo especificado em OUTPUT
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
  };
}

//k6 run --env VUS=300 script_10iterations_env.js
//k6 run --env VUS=300 --env OUTPUT='resultados.json' script_10iterations_env.js

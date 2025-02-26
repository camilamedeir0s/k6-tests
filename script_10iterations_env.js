import http from 'k6/http';
import { check } from 'k6';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';

// Obtendo valores de variáveis de ambiente ou usando padrões
const VUS = parseInt(__ENV.VUS) || 500; // Número de usuários virtuais simultâneos
const OUTPUT = __ENV.OUTPUT || 'raw-data.json'; // Nome do arquivo de saída
const HOST = "internal-a9d21652a0ae6439484cd3cd87dd5e93-185456715.us-east-1.elb.amazonaws.com"

// Iterations de acordo com o valor de VUS
let iterations = 0;
switch (VUS) {
  case 50:
    iterations = 840;
    break;
  case 100:
    iterations = 550;
    break;
  case 150:
    iterations = 450;
    break;
  case 200:
    iterations = 400;
    break;
  default:
    throw new Error(`VUS ${VUS} não suportado.`);
}

// export const options = {
//   scenarios: {
//     fixed_iterations: {
//       executor: 'per-vu-iterations',
//       vus: VUS, // Número de usuários virtuais simultâneos
//       iterations: iterations, // Número de iterações por VU
//       maxDuration: '1h', // Tempo máximo permitido para o teste
//     },
//   },
// };

export const options = {
  scenarios: {
    fixed_iterations: {
      executor: "shared-iterations",
      vus: VUS,
      iterations: VUS * 500,
      maxDuration: "5m",
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
    const res = http.get(`http://${HOST}${endpoint}`);
    checkResponse(res);
  }
}

export function handleSummary(data) {
  return {
    [OUTPUT]: JSON.stringify(data), // Usa o nome do arquivo especificado em OUTPUT
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
  };
}

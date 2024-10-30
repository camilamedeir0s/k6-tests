import http from 'k6/http';
import { sleep } from 'k6';
import { check } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
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
    const res = http.get(`http://localhost:12345${endpoint}`);
    checkResponse(res);
  }
}

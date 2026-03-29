// Location: frontend/public/sw.js
// Service Worker for offline support

const CACHE_NAME = 'agroai-v1'
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/locales/hi.json',
  '/locales/en.json',
]

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  )
  self.skipWaiting()
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  )
})

self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/api/')) {
    // Network first for API calls, cache as fallback
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const clone = response.clone()
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone))
          return response
        })
        .catch(() => caches.match(event.request))
    )
  } else {
    // Cache first for static assets
    event.respondWith(
      caches.match(event.request).then(cached => cached || fetch(event.request))
    )
  }
})

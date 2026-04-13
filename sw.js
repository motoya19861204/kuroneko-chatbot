self.addEventListener('install', (e) => {
    self.skipWaiting();
});

self.addEventListener('fetch', (e) => {
    // ネットワークへのリクエストをそのまま通す（オフラインキャッシュはとりあえずしない）
});

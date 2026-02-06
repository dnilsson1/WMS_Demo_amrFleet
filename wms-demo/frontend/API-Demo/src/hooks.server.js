const INTERNAL_API_BASE = process.env.INTERNAL_API_BASE || 'http://backend:8000';

export async function handle({ event, resolve }) {
	const { url, request } = event;

	if (url.pathname.startsWith('/api')) {
		const targetPath = url.pathname.replace(/^\/api/, '') || '/';
		const targetUrl = new URL(`${targetPath}${url.search}`, INTERNAL_API_BASE);

		const headers = new Headers(request.headers);
		headers.delete('host');

		const proxyRequest = new Request(targetUrl, {
			method: request.method,
			headers,
			body: request.body,
			duplex: 'half'
		});

		return fetch(proxyRequest);
	}

	return resolve(event);
}
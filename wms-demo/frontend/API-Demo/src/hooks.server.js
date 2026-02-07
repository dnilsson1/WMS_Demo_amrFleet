import { redirect } from '@sveltejs/kit';

const INTERNAL_API_BASE = process.env.INTERNAL_API_BASE || 'http://backend:8000';
const PROTECTED_PATHS = ['/settings', '/orders', '/receiving'];

export async function handle({ event, resolve }) {
	const { url, request } = event;
	const token = event.cookies.get('access_token');

	if (PROTECTED_PATHS.some((path) => url.pathname.startsWith(path))) {
		if (!token) {
			throw redirect(303, '/login');
		}
	}

	if (url.pathname.startsWith('/api')) {
		const targetPath = url.pathname.replace(/^\/api/, '') || '/';
		const targetUrl = new URL(`${targetPath}${url.search}`, INTERNAL_API_BASE);

		const headers = new Headers(request.headers);
		headers.delete('host');
		if (token && !headers.has('authorization')) {
			headers.set('authorization', `Bearer ${token}`);
		}

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
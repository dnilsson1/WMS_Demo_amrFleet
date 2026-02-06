import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
	const env = loadEnv(mode, process.cwd(), '');
	const hmrHost = env.VITE_HMR_HOST || undefined;
	const hmrProtocol = env.VITE_HMR_PROTOCOL || undefined;
	const hmrClientPort = env.VITE_HMR_CLIENT_PORT
		? Number(env.VITE_HMR_CLIENT_PORT)
		: 5173;

	return {
		plugins: [sveltekit()],
		server: {
			host: true,
			port: 5173,
			strictPort: true,
			hmr: {
				host: hmrHost,
				protocol: hmrProtocol,
				clientPort: hmrClientPort
			},
			proxy: {
				'/api': {
					target: 'http://backend:8000',
					changeOrigin: true,
					rewrite: (path) => path.replace(/^\/api/, '')
				}
			}
		}
	};
});

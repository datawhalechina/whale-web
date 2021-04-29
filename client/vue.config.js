const api_port = process.env.API_PORT || '8000'; // default django port
const api_host = process.env.API_HOST || 'localhost';
console.log(`API server: http://${api_host}:${api_port}`);

module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: `http://${api_host}:${api_port}`,
        changeOrigin: true,
      },
    },
  },
  transpileDependencies: [
    'vuetify',
  ],
  lintOnSave: false,
};

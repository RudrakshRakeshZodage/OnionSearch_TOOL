module.exports = {
  apps: [
    {
      name: 'onion-hidden-site',
      script: 'hidden_server.js',
      cwd: 'C:\\Users\\Rudraksh\\Desktop\\Tor_scrap\\OnionSearch',
      watch: false,
      restart_delay: 3000,
      max_restarts: 20,
      log_file: 'C:\\Users\\Rudraksh\\Desktop\\Tor_scrap\\OnionSearch\\logs\\hidden-site.log',
      error_file: 'C:\\Users\\Rudraksh\\Desktop\\Tor_scrap\\OnionSearch\\logs\\hidden-site-error.log',
      env: {
        NODE_ENV: 'production'
      }
    },
    {
      name: 'onion-search-ui',
      script: 'server.js',
      cwd: 'C:\\Users\\Rudraksh\\Desktop\\Tor_scrap\\OnionSearch',
      watch: false,
      restart_delay: 3000,
      max_restarts: 20,
      log_file: 'C:\\Users\\Rudraksh\\Desktop\\Tor_scrap\\OnionSearch\\logs\\search-ui.log',
      error_file: 'C:\\Users\\Rudraksh\\Desktop\\Tor_scrap\\OnionSearch\\logs\\search-ui-error.log',
      env: {
        NODE_ENV: 'production'
      }
    }
  ]
};

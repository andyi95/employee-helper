module.exports = {
    chainWebpack: config => {
        config.module
            .rule('vue')
            .use('vue-loader')
            // .loader('vue-loader')
            .tap(options => {
                options.complierOptions = {whitespace: 'preserve'};
                // options.prettify = false;
                return options;
            });
    },
    devServer: {
        host: 'localhost',
        port: 4000,
        allowedHosts: [
            'frontend',
            'localhost',
            'lk-employee.dev.andyi95.com'
        ],
        client: {
            webSocketURL: 'auto://0.0.0.0:0/ws'
        }
    }
}

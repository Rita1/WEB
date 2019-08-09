module.exports = {
  // 1
  entry: __dirname + '/static/js/index.jsx',
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },
  // 2
  output: {
    path: __dirname + '/static',
    //publicPath: '/',
    filename: 'bundle.js'
  },
  // 3
  //devServer: {
  //  contentBase: './templates'
  //}
};

console.log(module.exports);

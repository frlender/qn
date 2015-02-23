var express = require('express');
var app = express();
var bodyParser = require('body-parser');

var  rubik = require('app/handlers.js');

app.use('/rubik',express.static(__dirname + '/public'));
app.use(bodyParser.urlencoded({limit:'50mb',extended:true}));
app.use(bodyParser.json({limit:'2mb',extended:true}));
// app.use(bodyParser.urlencoded({ extended: false }))
// app.use(json());


// API
app.post('/rubik/visualize',rubik.visualize);
app.get('/rubik/downloadSvg',rubik.downloadSvg);

console.log('listen at:',8080)
app.listen(8080);
'use strict';
var yeoman = require('yeoman-generator');
var chalk = require('chalk');
var yosay = require('yosay');

module.exports = yeoman.generators.Base.extend({
  initializing: function () {
    this.pkg = require('../package.json');
  },

  prompting: function () {
    var done = this.async();

    // Have Yeoman greet the user.
    this.log(yosay(
      'Welcome to the primo' + chalk.red('Qn') + ' generator!'
    ));

    var prompts = [{
      name: 'appName',
      message: "what's your app name?"
    },{
      type: 'confirm',
      name: 'addBackbone',
      message: 'Would you like to enable add backbone?',
      default: true
    }];

    this.prompt(prompts, function (props) {
      this.addBackbone = props.addBackbone;
      this.appName  = props.appName;

      done();
    }.bind(this));
  },

  writing: {
    app: function () {
      this.fs.copyTpl(
        this.templatePath('_package.json'),
        this.destinationPath('package.json'),
        {appName:'new'}
      );
      this.fs.copyTpl(
        this.templatePath('_bower.json'),
        this.destinationPath('bower.json'),
        {addBackbone:this.addBackbone}
      );
      this.fs.copy(
        this.templatePath('_.bowerrc'),
        this.destinationPath('.bowerrc')
      );
      this.fs.copy(
        this.templatePath('Gruntfile.js'),
        this.destinationPath('Gruntfile.js')
      );
      this.fs.copy(
        this.templatePath('views/_index.jade'),
        this.destinationPath('views/index.jade')
      );
      this.fs.copy(
        this.templatePath('_index.js'),
        this.destinationPath('index.js')
      );
      this.fs.copy(
        this.templatePath('.gitignore'),
        this.destinationPath('.gitignore')
      );
      this.bulkDirectory(
        'public','public'
      );
      // this.fs.copy(
      //   this.templatePath('views/_index.jade'),
      //   this.destinationPath('views/index.jade'),
      // );
    },

    projectfiles: function () {
      this.fs.copy(
        this.templatePath('editorconfig'),
        this.destinationPath('.editorconfig')
      );
      this.fs.copy(
        this.templatePath('jshintrc'),
        this.destinationPath('.jshintrc')
      );
    }
  },

  install: function () {
    this.installDependencies({
      skipInstall: true
    });
  }
});

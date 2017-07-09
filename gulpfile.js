// requirements

var gulp = require('gulp');
var gulpBrowser = require("gulp-browser");
var reactify = require('reactify');
var del = require('del');
var size = require('gulp-size');


gulp.task('transform', function () {
  var stream = gulp.src('./tv_trivia/static/scripts/jsx/*.js')
    .pipe(gulpBrowser.browserify({transform: ['reactify']}))
    .pipe(gulp.dest('./tv_trivia/static/scripts/js/'))
    .pipe(size());
  return stream;
});

gulp.task('del', function () {
  // add task
});

gulp.task('default', function() {
  gulp.start('transform');
});
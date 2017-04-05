var exec = require('child_process').exec, child;

function runAllTests(){
  exec('pytest -s ../../../test_crud.py',
  function (error, stdout, stderr) {
      console.log('stdout: ' + stdout);
      console.log('stderr: ' + stderr);
      if (error !== null) {
           console.log('exec error: ' + error);
      }
  });
}

runAllTests();

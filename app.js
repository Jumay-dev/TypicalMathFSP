const express = require('express')
const path = require('path')
const { json } = require('express')
const app = express()

//Python connection modules
const spawn = require("child_process").spawn;

debug = true;

// const mul = 2;
// const pythonProcess = spawn('python',["./model/test.py", mul]);
// pythonProcess.stdout.on('data', (data) => {
//   console.log("Data from py script", data.toString());
// });

// Start values for example
let SVALUE = {
  x: '1',
  y: '2',
  z: '3',
  vx: '4',
  vy: '5',
  vz: '7',
  tstart: '8',
  dt: '9',
  tend: '10'
}


// Values after calculating by backend logic
let CVALUE = {}

app.use(express.json())

// GET
app.get('/api/contacts', (req, res) => {
  debug && console.log('GET request recieved')
  res.status(200).json(SVALUE)
})

// POST
app.post('/api/contacts', (req, res) => {
  debug && console.log('POST request recieved')
  let val = {...req.body}
  SVALUE = val

  async function handleValues(SVALUE) { 
    result = await setTimeout(anyF, 1000)
    
    function anyF() {
      const mul = 2;
      const pythonProcess = spawn('python',["./model/test.py", mul]);
      pythonProcess.stdout.on('data', (data) => {
        resValue = data.toString();
        console.log("Data from py script", resValue);
        res.status(200).json(resValue);
      });
    }
  }

  handleValues()

})


app.use(express.static(path.resolve(__dirname, 'client')))

app.get('*', (req, res) => {
  res.sendFile(path.resolve(__dirname, '@/client', 'index.html'))
})

app.listen(3000, () => console.log('Server has been started on port 3000'))
